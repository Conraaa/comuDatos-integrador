# Comunicación de Datos - Trabajo Integrador - Grupo 4 - S32

## Backend - FastAPI

+Teniendo Python y el gestor de paquetes PIP instalados, se instalará FastAPI. En caso de no tenerlos se pueden obtener en https://www.python.org/ y https://pypi.org/project/pip/, respectivamente.

### Entorno Virtual

_C:...\backend>_ `pip install virtualenv`

_C:...\backend>_ `virtualenv venv`                    #Crea el entorno virtual

**_Windows:_**
`.\venv\Scripts\activate`                                 #Activa el entorno virtual

**_Linux:_**
`source venv/bin/activate`                                #Activa el entorno virtual

-Una vez creado y dentro del entorno virtual, instalar FastAPI y Uvicorn, configurar el interprete y descargar paquetes:

_(venv) C:...\backend>_ `pip install "fastapi[all]" uvicorn`

En VSCode: F1 > Select Interpreter > Python('venv')

_(venv) C:...\backend>_ `pip install -r requirements.txt`

### Correr el backend:

_(venv) C:...\backend>_ `uvicorn main:app --reload`


## Frontend - React
