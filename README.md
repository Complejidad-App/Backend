# Complejidad App — Backend

REST API construida con **FastAPI** que aplica algoritmos de análisis sobre un
dataset y devuelve los resultados en **formato JSON**, para que el frontend los
consuma y los muestre gráficamente.

## Requisitos

- Python 3.11+

## Instalación

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt          # solo runtime
pip install -r requirements-dev.txt      # runtime + herramientas de desarrollo
```

## Variables de entorno

Copia `.env.example` a `.env` y ajusta los valores (sobre todo `BACKEND_CORS_ORIGINS`
con la URL del frontend):

```bash
cp .env.example .env
```

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentación interactiva (Swagger): http://localhost:8000/docs
- Documentación alternativa (ReDoc): http://localhost:8000/redoc

## Endpoints de ejemplo

| Método | Ruta                       | Descripción                                   |
| ------ | -------------------------- | --------------------------------------------- |
| GET    | `/`                        | Información básica de la API                   |
| GET    | `/api/v1/health`           | Verificación de estado                         |
| POST   | `/api/v1/analysis/stats`   | Estadísticas + histograma de una lista de números |

Ejemplo de petición:

```bash
curl -X POST http://localhost:8000/api/v1/analysis/stats \
  -H "Content-Type: application/json" \
  -d '{"values": [4, 8, 15, 16, 23, 42]}'
```

## Estructura del proyecto

```
app/
├── main.py              # Punto de entrada: crea la app FastAPI y registra CORS y rutas
├── core/
│   └── config.py        # Configuración (variables de entorno, CORS)
├── api/
│   ├── routes.py        # Agrupa todos los routers
│   └── endpoints/       # Un archivo por grupo de endpoints
│       ├── health.py
│       └── analysis.py
├── schemas/             # Modelos Pydantic (entrada/salida JSON)
│   └── analysis.py
└── services/            # Lógica de negocio / algoritmos de análisis
    └── analysis_service.py
tests/                   # Pruebas con pytest
```

> El endpoint `/analysis/stats` y el servicio `analysis_service.py` son un
> **ejemplo**. A medida que avance el análisis del dataset, agrega aquí los
> algoritmos reales: crea un schema en `schemas/`, la lógica en `services/` y
> expón el endpoint en `api/endpoints/`.

## Desarrollo

```bash
# Linter + formato (Ruff)
ruff check .
ruff format .

# Pruebas
pytest
```
