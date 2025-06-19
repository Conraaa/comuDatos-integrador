from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from PIL import Image
import io
import os
import uuid
import logging

from backend.db.database import engine, AsyncSessionLocal, create_db_tables, get_db, ImageRecord, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.utils.image_processing import process_image_for_digitalization

from fastapi.middleware.cors import CORSMiddleware

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# path's directorios
UPLOAD_DIRECTORY = "uploaded_images"
PROCESSED_DIRECTORY = "processed_images"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)

@app.on_event("startup")
async def startup():
    logger.info("Iniciando aplicación...")
    await create_db_tables()
    logger.info("Motor de base de datos configurado y tablas verificadas.")
    
@app.on_event("shutdown")
async def shutdown():
    logger.info("Cerrando aplicación...")
    logger.info("Aplicación FastAPI cerrada.")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Cargar Imagen para Digitalizar</title>
        </head>
        <body>
            <h1>Sube tu imagen de "alta resolución"</h1>
            <form action="/upload-and-process/" enctype="multipart/form-data" method="post">
                <input name="file" type="file" accept="image/*">
                <br><br>
                <label for="sample_rate">Frecuencia de Muestreo (cada N píxeles, ej: 2 para cada 2px):</label>
                <input type="number" id="sample_rate" name="sample_rate" value="1" min="1">
                <br><br>
                <label for="quantization_bits">Profundidad de Cuantización (bits por canal, ej: 4, 8):</label>
                <input type="number" id="quantization_bits" name="quantization_bits" value="8" min="1" max="8">
                <br><br>
                <input type="submit" value="Subir y Procesar">
            </form>
        </body>
    </html>
    """
    pass

@app.post("/upload-and-process/")
async def upload_and_process_image(
    file: UploadFile = File(...),
    sample_rate: int = Form(1),
    quantization_bits: int = Form(8),
    db: AsyncSession = Depends(get_db)
):  
    logger.info(f"DEBUG: sample_rate recibido: {sample_rate}")
    logger.info(f"DEBUG: quantization_bits recibido: {quantization_bits}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")

    file_extension = file.filename.split(".")[-1].lower()
    original_filename = f"{uuid.uuid4()}.{file_extension}"
    processed_filename = f"processed_{uuid.uuid4()}.{file_extension}"

    original_file_path = os.path.join(UPLOAD_DIRECTORY, original_filename)
    processed_file_path = os.path.join(PROCESSED_DIRECTORY, processed_filename)

    try:
        with open(original_file_path, "wb") as buffer:
            buffer.write(await file.read())

        original_image = Image.open(original_file_path)
        
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')

        processed_image = process_image_for_digitalization(
            original_image,
            sample_rate=sample_rate,
            quantization_bits=quantization_bits
        )

        if processed_image.mode == 'P' and file_extension in ['jpg', 'jpeg']:
            processed_image = processed_image.convert('RGB')

        processed_image.save(processed_file_path)
        
        db_record = ImageRecord(
            original_filename=original_filename,
            processed_filename=processed_filename,
            sample_rate_used=sample_rate,
            quantization_bits_used=quantization_bits
        )
        db.add(db_record)
        await db.commit()
        await db.refresh(db_record)

        logger.info(f"Registro de imagen guardado en la DB con ID: {db_record.id}")

        return {
            "message": "Imagen procesada exitosamente",
            "original_image_url": f"/images/{original_filename}",
            "processed_image_url": f"/images/{processed_filename}",
            "original_filename": original_filename,
            "processed_filename": processed_filename
        }
    except Exception as e:
        logger.error(f"Error al procesar la imagen: {str(e)}", exc_info=True)

        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        if os.path.exists(processed_file_path):
            os.remove(processed_file_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path_original = os.path.join(UPLOAD_DIRECTORY, filename)
    file_path_processed = os.path.join(PROCESSED_DIRECTORY, filename)

    if os.path.exists(file_path_original):
        file_path = file_path_original
    elif os.path.exists(file_path_processed):
        file_path = file_path_processed
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    mime_type = "image/jpeg"
    if filename.lower().endswith(".png"):
        mime_type = "image/png"
    elif filename.lower().endswith(".gif"):
        mime_type = "image/gif"

    return StreamingResponse(open(file_path, "rb"), media_type=mime_type)

@app.get("/records/")
async def get_image_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ImageRecord))
    records = result.scalars().all()
    return records