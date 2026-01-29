
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import estudiantes

app = FastAPI(
    title="API de Gestión Académica",
    description="Sistema para gestionar estudiantes, profesores y cursos",
    version="1.0.0"
)

# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")

# Configurar motor de templates Jinja2
templates = Jinja2Templates(directory="templates")

# Incluir routers de la API
app.include_router(estudiantes.router, prefix="/api/v1", tags=["Estudiantes"])


@app.get("/", tags=["Inicio"])
async def home(request: Request):
    """
    Página de inicio del sistema con estadísticas en tiempo real
    """
    # Importar base de datos de estudiantes
    from app.routers.estudiantes import estudiantes_db
   
    # Calcular estadísticas
    total = len(estudiantes_db)
    activos = len([e for e in estudiantes_db if e.get("activo", True)])
   
    # Calcular promedio general
    if total > 0:
        suma_promedios = sum([e.get("promedio", 0) for e in estudiantes_db])
        promedio = suma_promedios / total
    else:
        promedio = 0
   
    # Datos que se pasan al template
    context = {
        "request": request,  # Obligatorio para Jinja2
        "titulo": "Sistema de Gestión Académica",
        "descripcion": "API REST desarrollada con FastAPI",
        "total_estudiantes": total,
        "estudiantes_activos": activos,
        "promedio_general": f"{promedio:.2f}",
        "features": [
            {
                "icono": "[EST]",
                "titulo": "Estudiantes",
                "descripcion": "Gestión completa de estudiantes con validaciones de datos"
            },
            {
                "icono": "[PROF]",
                "titulo": "Profesores",
                "descripcion": "Control y administración de profesores del sistema"
            },
            {
                "icono": "[CURS]",
                "titulo": "Cursos",
                "descripcion": "Administración de cursos y materias académicas"
            },
            {
                "icono": "[STATS]",
                "titulo": "Estadísticas",
                "descripcion": "Métricas y reportes del sistema en tiempo real"
            }
        ]
    }
   
    # Renderizar template con los datos
    return templates.TemplateResponse("home.html", context)