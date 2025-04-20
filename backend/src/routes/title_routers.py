# title_routers.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from src.database import get_db
from src.utils import get_current_user
from src.models.title_models import (
    Title, ContentType, Classification, Genre,
    Theme, Resolution, FundingSource, CrewCategory,
    Person, Episode, Crew, title_content_types,
    title_genres, title_classifications, title_themes,
    title_resolutions, title_funding
)
from src.schemas.title_schemas import ( TitleReadSchema, TitleCreateSchema, TitleUpdateSchema)

title_router = APIRouter()

# ---------------------------
# Operaciones CRUD para Títulos
# ---------------------------

@title_router.get("/",
                 response_model=List[TitleReadSchema],
                 summary="Obtener todos los títulos",
                 description="Lista todos los títulos del usuario autenticado")
async def get_titles(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtiene todos los títulos del usuario actual"""
    if not current_user:
        raise HTTPException(status_code=401, detail="No autorizado")

    titles = db.query(Title).filter(Title.user_id == current_user["id"]).all()
    return titles

@title_router.get("/{title_id}",
                 response_model=TitleReadSchema,
                 summary="Obtener un título específico",
                 responses={404: {"description": "Título no encontrado"}})
async def get_title(
    title_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Obtiene un título específico por su ID"""
    title = db.query(Title).filter(
        Title.id == title_id,
        Title.user_id == current_user["id"]
    ).first()

    if not title:
        raise HTTPException(status_code=404, detail="Título no encontrado")

    return title

@title_router.post("/",
                  response_model=TitleReadSchema,
                  status_code=status.HTTP_201_CREATED,
                  summary="Crear nuevo título",
                  responses={400: {"description": "Datos inválidos"}})
async def create_title(
    title_data: TitleCreateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Crea un nuevo título con todos sus datos relacionados"""
    try:
        # Crear instancia base del título
        db_title = Title(
            **title_data.dict(exclude={
                "content_types", "classifications",
                "genres", "themes", "resolutions",
                "funding_sources", "crew"
            }),
            user_id=current_user["id"]
        )

        # Manejar relaciones M:N
        _handle_relationships(db, db_title, title_data)

        db.add(db_title)
        db.commit()
        db.refresh(db_title)

        return db_title

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creando título: {str(e)}"
        )

@title_router.put("/{title_id}",
                 response_model=TitleReadSchema,
                 summary="Actualizar título",
                 responses={
                     404: {"description": "Título no encontrado"},
                     400: {"description": "Error en los datos"}
                 })
async def update_title(
    title_id: uuid.UUID,
    title_data: TitleUpdateSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Actualiza un título existente"""
    db_title = db.query(Title).filter(
        Title.id == title_id,
        Title.user_id == current_user["id"]
    ).first()

    if not db_title:
        raise HTTPException(status_code=404, detail="Título no encontrado")

    try:
        update_data = title_data.dict(exclude_unset=True)

        # Actualizar campos simples
        for key, value in update_data.items():
            if key not in ["content_types", "classifications", "genres",
                          "themes", "resolutions", "funding_sources", "crew"]:
                setattr(db_title, key, value)

        # Actualizar relaciones
        _handle_relationships(db, db_title, title_data, update_mode=True)

        db.commit()
        db.refresh(db_title)

        return db_title

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error actualizando título: {str(e)}"
        )

@title_router.delete("/{title_id}",
                    status_code=status.HTTP_204_NO_CONTENT,
                    summary="Eliminar título",
                    responses={404: {"description": "Título no encontrado"}})
async def delete_title(
    title_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Elimina un título y todos sus datos relacionados"""
    db_title = db.query(Title).filter(
        Title.id == title_id,
        Title.user_id == current_user["id"]
    ).first()

    if not db_title:
        raise HTTPException(status_code=404, detail="Título no encontrado")

    try:
        db.delete(db_title)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error eliminando título: {str(e)}"
        )

# ---------------------------
# Funciones auxiliares
# ---------------------------

def _handle_relationships(db: Session, title: Title, data: TitleCreateSchema, update_mode: bool = False):
    """Maneja todas las relaciones M:N del título"""

    # Manejar relaciones simples (listas de IDs)
    relationship_handlers = {
        "content_types": (ContentType, title_content_types),
        "classifications": (Classification, title_classifications),
        "genres": (Genre, title_genres),
        "themes": (Theme, title_themes),
        "resolutions": (Resolution, title_resolutions)
    }

    for rel_name, (model, relation_table) in relationship_handlers.items():
        if hasattr(data, rel_name):
            ids = getattr(data, rel_name)
            if ids is not None:
                # Validar existencia de los IDs
                existing = db.query(model).filter(model.id.in_(ids)).all()
                if len(existing) != len(ids):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Algunos IDs de {rel_name} no existen"
                    )

                # Actualizar relación
                if update_mode:
                    db.execute(relation_table.delete().where(
                        relation_table.c.title_id == title.id
                    ))
                title.__getattribute__(rel_name).extend(existing)

    # Manejar funding sources con contribución
    if data.funding_sources:
        funding_data = data.funding_sources
        sources_ids = [fs.funding_source_id for fs in funding_data]

        existing_sources = db.query(FundingSource).filter(
            FundingSource.id.in_(sources_ids)
        ).all()

        if len(existing_sources) != len(sources_ids):
            raise HTTPException(
                status_code=400,
                detail="Algunos funding sources no existen"
            )

        if update_mode:
            db.execute(title_funding.delete().where(
                title_funding.c.title_id == title.id
            ))

        for fs in funding_data:
            db.execute(title_funding.insert().values(
                title_id=title.id,
                funding_source_id=fs.funding_source_id,
                contribution=fs.contribution
            ))

    # Manejar crew members
    if data.crew:
        crew_data = data.crew
        person_ids = [c.person_id for c in crew_data]
        category_ids = [c.crew_category_id for c in crew_data]

        # Validar existencia de personas y categorías
        existing_people = db.query(Person).filter(
            Person.nconst.in_(person_ids)
        ).all()
        existing_categories = db.query(CrewCategory).filter(
            CrewCategory.id.in_(category_ids)
        ).all()

        if len(existing_people) != len(person_ids):
            raise HTTPException(
                status_code=400,
                detail="Algunas personas no existen"
            )
        if len(existing_categories) != len(category_ids):
            raise HTTPException(
                status_code=400,
                detail="Algunas categorías no existen"
            )

        if update_mode:
            db.query(Crew).filter(Crew.title_id == title.id).delete()

        for crew_member in crew_data:
            db_crew = Crew(
                title_id=title.id,
                person_id=crew_member.person_id,
                crew_category_id=crew_member.crew_category_id,
                ordering=crew_member.ordering,
                job=crew_member.job,
                characters=crew_member.characters
            )
            db.add(db_crew)
