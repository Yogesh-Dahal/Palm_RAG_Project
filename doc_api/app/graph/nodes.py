import json
import re
from langchain_core.messages import HumanMessage
from services.ai_services import llm
from prompts.prompts import (
    INTENT_PROMPT,
    RAG_PROMPT,
    BOOKING_PROMPT
)


def extract_json(text: str) -> str:
    """
    Extract JSON from markdown code blocks if present.
    Handles: ```json ... ``` or just raw JSON
    """
    # Try to extract from markdown code blocks
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    return text.strip()


def intent_node(state):
    prompt = INTENT_PROMPT.format(query=state["query"])
    res = llm.invoke([HumanMessage(content=prompt)])
    try:
        json_str = extract_json(res.content)
        intent_data = json.loads(json_str)
        return {"intent": intent_data.get("intent", "qa")}
    except json.JSONDecodeError as e:
        print(f"Error parsing intent JSON: {e}")
        print(f"LLM Response: {res.content}")
        return {"intent": "qa"} 


def rag_node(state):
    prompt = RAG_PROMPT.format(
        context=state["context"],
        history=state["history"],
        query=state["query"]
    )
    res = llm.invoke([HumanMessage(content=prompt)])
    return {"answer": res.content}


def booking_node(state):
    prompt = BOOKING_PROMPT.format(
        history=state["history"],
        query=state["query"]
    )
    res = llm.invoke([HumanMessage(content=prompt)])
    try:
        json_str = extract_json(res.content)
        booking_data = json.loads(json_str)
        return {"booking": booking_data}
    except json.JSONDecodeError as e:
        print(f"Error parsing booking JSON: {e}")
        print(f"LLM Response: {res.content}")
        return {
            "booking": {
                "name": None,
                "email": None,
                "date": None,
                "time": None
            }
        }
