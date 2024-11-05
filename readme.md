# Proyecto Django - Instrucciones de Inicio

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Python 3.x
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

## Instalación

1. **Clona el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_PROYECTO>
    ```

2. **Crea y activa un entorno virtual:**

    ```bash
    python -m venv .venv
    source .venv/scripts/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuración
1. **Setea las variables de entorno**
    ```
    setx DB_PASSWORD "PASSWORD"
    ```

2. **Realiza las migraciones de la base de datos:**

    ```bash
    python manage.py migrate
    ```

## Ejecución

1. **Inicia el servidor de desarrollo:**

    ```bash
    python manage.py runserver
    ```

2. **Accede a la aplicación:**

    Abre tu navegador y ve a `http://127.0.0.1:8000`.

## Reiniciar db

```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

