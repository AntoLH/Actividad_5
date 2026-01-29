from fastapi import APIRouter, Query
router = APIRouter(
    prefix="/estudiantes",
    tags=["Estudiantes"]
)

# Base de datos simulada
estudiantes_db = [
    {"id": 1, "nombre": "Juan Pérez", "matricula": "2021001", "carrera": "Ingeniería"},
    {"id": 2, "nombre": "María López", "matricula": "2021002", "carrera": "Medicina"},
    {"id": 3, "nombre": "Carlos García", "matricula": "2021003", "carrera": "Derecho"},
    {"id": 4, "nombre": "Ana Martínez", "matricula": "2021004", "carrera": "Ingeniería"},
    {"id": 5, "nombre": "Pedro Sánchez", "matricula": "2021005", "carrera": "Medicina"},
]

@router.get("/")
def listar_estudiantes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista todos los estudiantes con paginación.
    """
    return {
        "total": len(estudiantes_db),
        "skip": skip,
        "limit": limit,
        "estudiantes": estudiantes_db[skip : skip + limit]
    }

@router.get("/{estudiante_id}")
def obtener_estudiante(estudiante_id: int):
    """
    Obtiene un estudiante por su ID.
    """
    for estudiante in estudiantes_db:
        if estudiante["id"] == estudiante_id:
            return estudiante
    return {"error": "Estudiante no encontrado"}