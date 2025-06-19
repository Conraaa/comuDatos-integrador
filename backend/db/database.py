from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, LargeBinary

from backend.db.config import DATABASE_URL

Base = declarative_base()

# modelo
class ImageRecord(Base):
    __tablename__ = "image_records"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String(255), nullable=False)
    processed_filename = Column(String(255), nullable=False)
    sample_rate_used = Column(Integer, nullable=False)
    quantization_bits_used = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def create_db_tables():
    print("Intentando crear tablas en la base de datos (si no existen)...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas (si no existían).")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session