# **Comunicación de Datos** - Trabajo Integrador - **Grupo 4** - S32

## Backend - **_FastAPI_**

+Teniendo **_Python_** y el gestor de **paquetes PIP** instalados, se instalará **_FastAPI_**. En caso de no tenerlos se pueden obtener en https://www.python.org/ y https://pypi.org/project/pip/, respectivamente.

### Entorno Virtual

_C:\\...\\>_ `pip install virtualenv`

_C:\\...\\>_ `virtualenv venv`                        #Crea el entorno virtual

**_Windows:_**
`.\venv\Scripts\activate`                                 #Activa el entorno virtual

**_Linux:_**
`source venv/bin/activate`                                #Activa el entorno virtual

-Una vez creado y dentro del entorno virtual, instalar **_FastAPI_** y **_Uvicorn_**, configurar el interprete y descargar paquetes:

_(venv) C:\\...\\backend\\>_ `pip install "fastapi[all]" uvicorn`

En VSCode: F1 > Select Interpreter > Python('venv')

_(venv) C:\\...\\backend\\>_ `pip install -r requirements.txt`

### Base de Datos

+Instalar **_Version 17_** del **controlador ODBC**:

https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16 **- Recordar instalar la _V. 17_**

+Se debe tener una base de datos creada en **SSMS** con el nombre exacto: _`cdd_images`_.

+Configurar las Variables de Entorno en un archivo **_'.env'_**, situado en el directorio raiz del proyecto.

### Correr el backend:

+Situado en el directorio raiz del proyecto:

_(venv) C:\\...\\>_ `uvicorn backend.main:app --reload`


---

## Frontend - **_React_**

+Utilizando **Visual Studio Code**, agregar la extension de React: **"_ES7+ React/Redux/React-Native snippets_"**.

+Instalar todos los paquetes necesarios:

_C:\\...\\frontend\\>_ `npm install`

+Una vez instalado todo, "_C:\\...\\frontend\\>_ `npm start`" ejecutará la aplicación en el modo de desarrollo.
