from fastapi import APIRouter
from schema.chat_schema import ChatRequest
from graph.graph import build_graph
from services.redis import get_history, save_message
from services.pincone import retrieve_context
from schema.save_to_db import save_booking
from core.database import session_local

router = APIRouter()
graph = build_graph()

@router.post("/chat")
def chat(payload: ChatRequest):
    session_id = payload.session_id
    query = payload.query
    
    print(f"\n=== NEW CHAT REQUEST ===")
    print(f"Session ID: {session_id}")
    print(f"User Query: {query}")


    save_message(session_id, "user", query)


    history = get_history(session_id)
    print(f"Chat History ({len(history)} messages):")
    for msg in history:
        print(f"  - {msg}")

    context = retrieve_context(query)
    print(f"Retrieved context length: {len(context)} chars")

    # Run LangGraph
    result = graph.invoke({
        "query": query,
        "history": history,
        "context": context
    })

    # Handle booking
    if result.get("booking"):
        booking = result["booking"]
        missing = [k for k, v in booking.items() if not v]
        if missing:
            reply = f"Please provide: {', '.join(missing)}"
            save_message(session_id, "assistant", reply)
            return {"message": reply, "status": "incomplete"}

        # Save booking in PostgreSQL
        try:
            db = session_local()
            saved_booking = save_booking(booking, db)
            db.close()
            reply = "Your interview has been booked successfully!"
            save_message(session_id, "assistant", reply)
            return {
                "message": reply,
                "status": "booked",
                "booking_id": saved_booking.id,
                "booking_details": {
                    "id": saved_booking.id,
                    "name": saved_booking.name,
                    "email": saved_booking.email,
                    "date": saved_booking.date.isoformat() if saved_booking.date else None,
                    "time": saved_booking.time,
                    "created_at": saved_booking.created_at.isoformat() if saved_booking.created_at else None
                }
            }
        except Exception as e:
            print(f"Error saving booking: {e}")
            reply = "Booking details received, but error saving to database. Please try again."
            save_message(session_id, "assistant", reply)
            return {"message": reply, "status": "error", "details": booking}

    # Normal RAG answer
    answer = result["answer"]
    save_message(session_id, "assistant", answer)
    return {"answer": answer, "status": "answered"}
