from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, Float, ForeignKey
from sqlalchemy.orm import relationship

from backend.db.config import DATABASE_URL

Base = declarative_base()


# modelo imagenes originales
class OriginalImage(Base):
    __tablename__ = "original_images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    bits_per_channel = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    digitalized_versions = relationship("DigitalizedImage", back_populates="original_image")
    bit_reduced_versions = relationship("BitDepthReducedImage", back_populates="original_image")

# modelo imagenes digitalizadas
class DigitalizedImage(Base):
    __tablename__ = "digitalized_images"

    id = Column(Integer, primary_key=True, index=True)
    original_image_id = Column(Integer, ForeignKey("original_images.id"), nullable=False)
    filename = Column(String(255), nullable=False, unique=True)
    sample_rate_used = Column(Integer, nullable=False)
    quantization_bits_used = Column(Integer, nullable=False)
    processed_width = Column(Integer, nullable=False)
    processed_height = Column(Integer, nullable=False)
    processed_bits_per_channel = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    original_image = relationship("OriginalImage", back_populates="digitalized_versions")

# modelo imagenes profundidad de bits reducida
class BitDepthReducedImage(Base):
    __tablename__ = "bit_depth_reduced_images"

    id = Column(Integer, primary_key=True, index=True)
    original_image_id = Column(Integer, ForeignKey("original_images.id"), nullable=False)
    filename = Column(String(255), nullable=False, unique=True)
    target_bits_per_channel = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    original_image = relationship("OriginalImage", back_populates="bit_reduced_versions")


# motor y sesion
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas en la BD.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session