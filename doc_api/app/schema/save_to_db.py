import pandas as pd
from sqlalchemy.orm import Session
from schema.models import Metadatas, BookingInfo
from services.chunker import Chunkmethod
from datetime import datetime

def save_to_db(df: pd.DataFrame, db: Session):
    for _, row in df.iterrows():

        existing = (
            db.query(Metadatas)
            .filter(
                Metadatas.document_name == row["document_name"],
                Metadatas.document_type == row["document_type"]
            )
            .first()
        )

        if existing:
            existing.chunk_method = Chunkmethod(row["chunk_method"])
            existing.chunk_size = int(row["chunk_size"])
        else:
            db.add(
                Metadatas(
                    document_name=row["document_name"],
                    document_type=row["document_type"],
                    chunk_method=Chunkmethod(row["chunk_method"]),
                    chunk_size=int(row["chunk_size"]),
                )
            )

    db.commit()


def save_booking(booking: dict, db: Session) -> BookingInfo:
    """
    Save interview booking information to PostgreSQL.
    
    Args:
        booking: Dict with keys: name, email, date (YYYY-MM-DD), time (HH:MM)
        db: Database session
    
    Returns:
        BookingInfo: Saved booking record
    """
    try:
        # Convert date string to datetime.date if provided
        booking_date = None
        if booking.get("date"):
            booking_date = datetime.strptime(booking["date"], "%Y-%m-%d").date()
        
        booking_record = BookingInfo(
            name=booking.get("name"),
            email=booking.get("email"),
            date=booking_date,
            time=booking.get("time")
        )
        
        db.add(booking_record)
        db.commit()
        db.refresh(booking_record)
        
        print(f"Booking saved successfully: {booking_record.id}")
        return booking_record
    except Exception as e:
        db.rollback()
        print(f"Error saving booking: {e}")
        raise

