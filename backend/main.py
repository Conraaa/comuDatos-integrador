from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from PIL import Image
import io
import os
import uuid

from utils.image_processing import process_image_for_digitalization
from utils.bit_depth_reducer import apply_bit_depth_reduction

from fastapi.middleware.cors import CORSMiddleware

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

UPLOAD_DIRECTORY = "uploaded_images"
PROCESSED_DIRECTORY = "processed_images"
BIT_DEPTH_REDUCED_DIRECTORY = "bit_depth_reduced_images"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
os.makedirs(BIT_DEPTH_REDUCED_DIRECTORY, exist_ok=True)

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
                    <p>Usa la función de tu compañero para aplicar muestreo y su lógica de cuantización.</p>
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
    quantization_bits: int = Form(8)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")

    file_extension = file.filename.split(".")[-1]
    original_filename = f"{uuid.uuid4()}.{file_extension}"
    processed_filename = f"processed_{uuid.uuid4()}.{file_extension}"

    original_file_path = os.path.join(UPLOAD_DIRECTORY, original_filename)

    try:
        with open(original_file_path, "wb") as buffer:
            buffer.write(await file.read())

        original_image = Image.open(original_file_path)

        processed_image = process_image_for_digitalization(
            original_image,
            sample_rate=sample_rate,
            quantization_bits=quantization_bits
        )

        if processed_image.mode == 'P' and file_extension.lower() in ['jpg', 'jpeg']:
            processed_image = processed_image.convert('RGB')

        processed_image.save(os.path.join(PROCESSED_DIRECTORY, processed_filename))

        return {
            "message": "Imagen digitalizada exitosamente",
            "original_image_url": f"/images/{original_filename}",
            "processed_image_url": f"/images/{processed_filename}",
            "original_filename": original_filename,
            "processed_filename": processed_filename
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")


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

    mime_type = "application/octet-stream"
    if filename.lower().endswith(('.jpg', '.jpeg')):
        mime_type = "image/jpeg"
    elif filename.lower().endswith('.png'):
        mime_type = "image/png"
    elif filename.lower().endswith('.gif'):
        mime_type = "image/gif"
    elif filename.lower().endswith('.bmp'):
        mime_type = "image/bmp"

    return StreamingResponse(open(file_path, "rb"), media_type=mime_type)
