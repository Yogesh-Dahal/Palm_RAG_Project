from sqlalchemy import *
from core.database import Base
from services.chunker import Chunkmethod

class Metadatas(Base):
    __tablename__ = 'metadata'
    __table_args__ = {'schema': 'datas'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False)
    chunk_method = Column(Enum(Chunkmethod, name="chunk_method", schema='datas'), nullable=False)
    chunk_size = Column(Integer,nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

class BookingInfo(Base):
    __tablename__ = 'booking'
    __table_args__ = {'schema':'datas'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    date = Column(Date, nullable=True)
    time = Column(String(5), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now()) 