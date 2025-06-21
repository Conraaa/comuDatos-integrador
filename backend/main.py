from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from PIL import Image
import os
import uuid
import logging

# bd
from backend.db.database import create_db_tables, get_db, OriginalImage, DigitalizedImage, BitDepthReducedImage, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# digitalizacion
from backend.utils.image_processing import process_image_for_digitalization

# reduccion de bits
from backend.utils.bit_depth_reducer import apply_bit_depth_reduction

# cors
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
BIT_DEPTH_REDUCED_DIRECTORY = "bit_depth_reduced_images"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
os.makedirs(BIT_DEPTH_REDUCED_DIRECTORY, exist_ok=True)

@app.on_event("startup")
async def startup():
    logger.info("Iniciando aplicación...")
    await create_db_tables()
    logger.info("Motor de base de datos configurado y tablas verificadas.")
    
@app.on_event("shutdown")
async def shutdown():
    logger.info("Cerrando aplicación...")
    logger.info("Aplicación cerrada.")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Funcionalidades de Procesamiento de Imagen</title>
            <style>
                body { font-family: sans-serif; margin: 40px; background-color: #f4f4f4; color: #333; }
                h1 { color: #333; text-align: center; }
                .container { display: flex; justify-content: space-around; gap: 20px; flex-wrap: wrap; }
                .card { background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 45%; min-width: 300px; }
                form { margin-top: 20px; }
                label { display: block; margin-bottom: 8px; font-weight: bold; }
                input[type="file"], input[type="number"], select {
                    width: calc(100% - 20px); padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px;
                }
                input[type="submit"] {
                    background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px;
                    cursor: pointer; font-size: 16px; transition: background-color 0.3s ease;
                }
                input[type="submit"]:hover { background-color: #0056b3; }
                .note { font-size: 0.9em; color: #666; margin-top: 10px; }
                .image-display { display: flex; justify-content: center; gap: 20px; margin-top: 40px; flex-wrap: wrap; }
                .image-container { text-align: center; background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .image-container img { max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 4px; max-height: 400px; object-fit: contain;}
                .image-container p { font-weight: bold; margin-bottom: 10px; color: #555; }
                #loading_message { text-align: center; margin-top: 20px; font-size: 1.2em; color: #007bff; display: none; }
            </style>
        </head>
        <body>
            <h1>Elige una Funcionalidad de Procesamiento de Imagen</h1>
            <div class="container">
                <div class="card">
                    <h2>1. Digitalización Completa</h2>
                    <p>Usa la función aplicar muestreo y su lógica de cuantización.</p>
                    <form id="digitalizationForm" action="/upload-and-process/" enctype="multipart/form-data" method="post">
                        <label for="file_digitalize">Sube tu imagen de "alta resolución":</label>
                        <input name="file" type="file" accept="image/*" id="file_digitalize">
                        <label for="sample_rate">Frecuencia de Muestreo (cada N píxeles, ej: 2):</label>
                        <input type="number" id="sample_rate" name="sample_rate" value="1" min="1">
                        <label for="quantization_bits_comp">Profundidad de Cuantización (bits, ej: 1-8):</label>
                        <input type="number" id="quantization_bits_comp" name="quantization_bits" value="8" min="1" max="8">
                        <input type="submit" value="Subir y Digitalizar">
                    </form>
                </div>

                <div class="card">
                    <h2>2. Reducción de Profundidad de Bits</h2>
                    <p>Aplica únicamente la reducción de profundidad de bits usando tu propia función.</p>
                    <form id="bitReductionForm" action="/reduce-bits/" enctype="multipart/form-data" method="post">
                        <label for="file_reduce_bits">Sube tu imagen:</label>
                        <input name="file" type="file" accept="image/*" id="file_reduce_bits" required>
                        <label for="target_bits">Profundidad de Bits Deseada (1, 8, 24):</label>
                        <input type="number" id="target_bits" name="target_bits" value="8" min="1" max="24" required>
                        <div class="note">Valores válidos: 1 (B/N), 8 (256 colores), 24 (Color Real).</div>
                        <input type="submit" value="Reducir Profundidad">
                    </form>
                </div>
            </div>

            <div id="loading_message" style="display:none;">Procesando imagen... Por favor, espera.</div>

            <div id="image_results" class="image-display">
                <div class="image-container">
                    <p>Imagen Original</p>
                    <img id="original_display" src="https://placehold.co/400x300/e0e0e0/555555?text=Original" alt="Imagen Original">
                </div>
                <div class="image-container">
                    <p>Imagen Modificada</p>
                    <img id="processed_display" src="https://placehold.co/400x300/e0e0e0/555555?text=Modificada" alt="Imagen Modificada">
                </div>
            </div>

            <script>
                async function handleFormSubmit(event, formAction) {
                    event.preventDefault();

                    const form = event.target;
                    const formData = new FormData(form);
                    const loadingMessage = document.getElementById('loading_message');
                    const originalDisplay = document.getElementById('original_display');
                    const processedDisplay = document.getElementById('processed_display');

                    loadingMessage.style.display = 'block';
                    originalDisplay.src = "https://placehold.co/400x300/e0e0e0/555555?text=Cargando...";
                    processedDisplay.src = "https://placehold.co/400x300/e0e0e0/555555?text=Cargando...";


                    try {
                        const response = await fetch(formAction, {
                            method: 'POST',
                            body: formData
                        });

                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || 'Error al procesar la imagen.');
                        }

                        const result = await response.json();
                        originalDisplay.src = result.original_image_url;
                        processedDisplay.src = result.processed_image_url;
                        originalDisplay.alt = `Original: ${result.original_filename}`;
                        processedDisplay.alt = `Procesada: ${result.processed_filename}`;

                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error al procesar la imagen: ' + error.message);
                        originalDisplay.src = "https://placehold.co/400x300/e0e0e0/FF0000?text=Error";
                        processedDisplay.src = "https://placehold.co/400x300/e0e0e0/FF0000?text=Error";
                    } finally {
                        loadingMessage.style.display = 'none';
                    }
                }

                document.getElementById('bitReductionForm').addEventListener('submit', function(event) {
                    handleFormSubmit(event, '/reduce-bits/');
                });

                document.getElementById('digitalizationForm').addEventListener('submit', function(event) {
                    handleFormSubmit(event, '/upload-and-process/');
                });
            </script>
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
        
        width, height = original_image.size
        bits_per_channel = 8

        db_original_image = OriginalImage(
            filename=original_filename,
            width=width,
            height=height,
            bits_per_channel=bits_per_channel
        )
        db.add(db_original_image)
        await db.commit()
        await db.refresh(db_original_image)
        original_image_id = db_original_image.id
        
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')

        processed_image = process_image_for_digitalization(
            original_image,
            sample_rate=sample_rate,
            quantization_bits=quantization_bits
        )

        if processed_image.mode == 'P' and file_extension in ['jpg', 'jpeg']:
            processed_image = processed_image.convert('RGB')

        processed_image.save(os.path.join(PROCESSED_DIRECTORY, processed_filename))
        
        processed_bits_per_channel = quantization_bits if 1 <= quantization_bits <= 8 else (24 if quantization_bits == 24 else None)
        
        db_digitalized_image = DigitalizedImage(
            original_image_id=original_image_id,
            filename=processed_filename,
            sample_rate_used=sample_rate,
            quantization_bits_used=quantization_bits,
            processed_width=processed_image.size[0],
            processed_height=processed_image.size[1],
            processed_bits_per_channel=processed_bits_per_channel
        )
        db.add(db_digitalized_image)
        await db.commit()
        await db.refresh(db_digitalized_image)

        logger.info(f"Imagen digitalizada guardada en la DB con ID: {db_digitalized_image.id}")

        return {
            "message": "Imagen digitalizada exitosamente",
            "original_image_url": f"/images/{original_filename}",
            "processed_image_url": f"/images/{processed_filename}",
            "original_filename": original_filename,
            "processed_filename": processed_filename
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error al procesar la imagen: {str(e)}", exc_info=True)

        if os.path.exists(original_file_path):
            os.remove(original_file_path)
            
        if os.path.exists(processed_file_path):
            os.remove(processed_file_path)
            
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")
    
@app.post("/reduce-bits/")
async def reduce_bits_image(
    file: UploadFile = File(...),
    target_bits: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")

    file_extension = file.filename.split(".")[-1].lower()
    original_filename = f"{uuid.uuid4()}.{file_extension}"
    reduced_filename = f"reduced_{uuid.uuid4()}.{file_extension}"

    original_file_path = os.path.join(UPLOAD_DIRECTORY, original_filename)
    reduced_file_path = os.path.join(BIT_DEPTH_REDUCED_DIRECTORY, reduced_filename)

    try:
        with open(original_file_path, "wb") as buffer:
            buffer.write(await file.read())

        original_image = Image.open(original_file_path)

        width, height = original_image.size
        bits_per_channel = 8

        db_original_image = OriginalImage(
            filename=original_filename,
            width=width,
            height=height,
            bits_per_channel=bits_per_channel
        )
        db.add(db_original_image)
        await db.commit()
        await db.refresh(db_original_image)
        original_image_id = db_original_image.id

        reduced_image = apply_bit_depth_reduction(
            original_image,
            target_bits=target_bits
        )

        if reduced_image.mode == 'P' and file_extension in ['jpg', 'jpeg']:
            reduced_image = reduced_image.convert('RGB')

        reduced_image.save(reduced_file_path)

        db_bit_reduced_image = BitDepthReducedImage(
            original_image_id=original_image_id,
            filename=reduced_filename,
            target_bits_per_channel=target_bits
        )
        db.add(db_bit_reduced_image)
        await db.commit()
        await db.refresh(db_bit_reduced_image)

        logger.info(f"Imagen con profundidad de bits reducida guardada en la DB con ID: {db_bit_reduced_image.id}")

        return {
            "message": "Profundidad de bits reducida exitosamente",
            "original_image_url": f"/images/{original_filename}",
            "processed_image_url": f"/images/{reduced_filename}",
            "original_filename": original_filename,
            "processed_filename": reduced_filename
        }
    except ValueError as ve:
        await db.rollback()
        logger.error(f"Error en la reducción de bits: {str(ve)}", exc_info=True)
        
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        raise HTTPException(status_code=400, detail=f"Error en la reducción de bits: {str(ve)}")
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error inesperado al reducir la profundidad de bits: {str(e)}", exc_info=True)
        
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        raise HTTPException(status_code=500, detail=f"Error inesperado al reducir la profundidad de bits: {str(e)}")


@app.post("/reduce-bits/")
async def reduce_bits_image(
    file: UploadFile = File(...),
    target_bits: int = Form(...)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")

    file_extension = file.filename.split(".")[-1]
    original_filename = f"{uuid.uuid4()}.{file_extension}"
    reduced_filename = f"reduced_{uuid.uuid4()}.{file_extension}"

    original_file_path = os.path.join(UPLOAD_DIRECTORY, original_filename)
    reduced_file_path = os.path.join(BIT_DEPTH_REDUCED_DIRECTORY, reduced_filename)

    try:
        with open(original_file_path, "wb") as buffer:
            buffer.write(await file.read())

        original_image = Image.open(original_file_path)

        reduced_image = apply_bit_depth_reduction(
            original_image,
            target_bits=target_bits
        )

        if reduced_image.mode == 'P' and file_extension.lower() in ['jpg', 'jpeg']:
            reduced_image = reduced_image.convert('RGB')

        reduced_image.save(reduced_file_path)

        return {
            "message": "Profundidad de bits reducida exitosamente",
            "original_image_url": f"/images/{original_filename}",
            "processed_image_url": f"/images/{reduced_filename}",
            "original_filename": original_filename,
            "processed_filename": reduced_filename
        }
    except ValueError as ve:
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        raise HTTPException(status_code=400, detail=f"Error en la reducción de bits: {str(ve)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        raise HTTPException(status_code=500, detail=f"Error inesperado al reducir la profundidad de bits: {str(e)}")


@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path_original = os.path.join(UPLOAD_DIRECTORY, filename)
    file_path_processed = os.path.join(PROCESSED_DIRECTORY, filename)
    file_path_reduced_bits = os.path.join(BIT_DEPTH_REDUCED_DIRECTORY, filename)

    if os.path.exists(file_path_original):
        file_path = file_path_original
    elif os.path.exists(file_path_processed):
        file_path = file_path_processed
    elif os.path.exists(file_path_reduced_bits):
        file_path = file_path_reduced_bits
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    mime_type = "image/jpeg"
    if filename.lower().endswith(('.jpg', '.jpeg')):
        mime_type = "image/jpeg"
    elif filename.lower().endswith('.png'):
        mime_type = "image/png"
    elif filename.lower().endswith('.gif'):
        mime_type = "image/gif"
    elif filename.lower().endswith('.bmp'):
        mime_type = "image/bmp"
    else:
        mime_type = "application/octet-stream"

    return StreamingResponse(open(file_path, "rb"), media_type=mime_type)

@app.get("/history/")
async def get_history_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(OriginalImage)
        .options(joinedload(OriginalImage.digitalized_versions))
        .options(joinedload(OriginalImage.bit_reduced_versions))
        .order_by(OriginalImage.created_at.desc())
    )
    original_images = result.scalars().unique().all()

    history_records = []
    for orig_img in original_images:
        orig_img_data = {
            "id": orig_img.id,
            "filename": orig_img.filename,
            "width": orig_img.width,
            "height": orig_img.height,
            "bits_per_channel": orig_img.bits_per_channel,
            "created_at": orig_img.created_at.isoformat(),
            "original_image_url": f"http://127.00.1:8000/images/{orig_img.filename}"
        }

        # digitalizacion
        for dig_img in orig_img.digitalized_versions:
            history_records.append({
                "type": "digitalized",
                "id": dig_img.id,
                "original_image": orig_img_data,
                "processed_image_url": f"http://127.0.0.1:8000/images/{dig_img.filename}",
                "processed_filename": dig_img.filename,
                "sample_rate_used": dig_img.sample_rate_used,
                "quantization_bits_used": dig_img.quantization_bits_used,
                "processed_width": dig_img.processed_width,
                "processed_height": dig_img.processed_height,
                "processed_bits_per_channel": dig_img.processed_bits_per_channel,
                "created_at": dig_img.created_at.isoformat()
            })
        
        # reduccion
        for bit_img in orig_img.bit_reduced_versions:
            history_records.append({
                "type": "bit_reduced",
                "id": bit_img.id,
                "original_image": orig_img_data,
                "processed_image_url": f"http://127.0.0.1:8000/images/{bit_img.filename}",
                "processed_filename": bit_img.filename,
                "target_bits_per_channel": bit_img.target_bits_per_channel,
                "created_at": bit_img.created_at.isoformat()
            })

    # orden
    history_records.sort(key=lambda x: x["created_at"], reverse=True)

    return JSONResponse(content=history_records)