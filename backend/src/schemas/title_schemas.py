from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union
from enum import Enum
from uuid import UUID

# -----------------------
# Enums (Mapeo desde SQLAlchemy)
# -----------------------
class StatusEnum(str, Enum):
    desarrollo = "desarrollo"
    preproducción = "preproducción"
    rodaje = "rodaje"
    producción = "producción"
    postproducción = "postproducción"
    estreno = "estreno"
    finalizada = "finalizada"
    cancelada = "cancelada"

class ProductionTypeEnum(str, Enum):
    comunitaria = "comunitaria"
    independiente = "independiente"
    industrial = "industrial"

class OriginEnum(str, Enum):
    Misiones = "Misiones"
    Región = "Región"
    Argentina = "Argentina"
    Internacional = "Internacional"

class ContributionEnum(str, Enum):
    total = "total"
    parcial = "parcial"

class ResolutionLabelEnum(str, Enum):
    p480 = "480p"
    p720 = "720p"
    p1080 = "1080p"
    k4 = "4K"

class ClassificationCodeEnum(str, Enum):
    ATP = "ATP"
    PLUS13 = "+13"
    PLUS16 = "+16"
    PLUS18 = "+18"
    C = "C"

# -----------------------
# Schemas para Entidades Relacionadas
# -----------------------
class ContentTypeSchema(BaseModel):
    id: int
    name: str

class ClassificationSchema(BaseModel):
    id: int
    code: ClassificationCodeEnum

class GenreSchema(BaseModel):
    id: int
    name: str

class ThemeSchema(BaseModel):
    id: int
    name: str

class ResolutionSchema(BaseModel):
    id: int
    label: ResolutionLabelEnum
    aspect_ratio: Optional[str]

class FundingSourceSchema(BaseModel):
    id: int
    name: str

class CrewCategorySchema(BaseModel):
    id: int
    name: str

class PersonSchema(BaseModel):
    nconst: str
    name: str
    birth_year: Optional[int]
    death_year: Optional[int]
    professions: Optional[List[str]]

class EpisodeSchema(BaseModel):
    episode_id: UUID
    series_id: UUID
    season_number: int
    episode_number: int

class CrewLinkSchema(BaseModel):
    person_id: str
    crew_category_id: int
    ordering: int
    job: Optional[str]
    characters: Optional[str]

class FundingLinkSchema(BaseModel):
    funding_source_id: int
    contribution: ContributionEnum

class TitleBaseSchema(BaseModel):
    primary_title: str = Field(..., max_length=255)
    original_title: Optional[str] = Field(None, max_length=255)
    start_year: int = Field(..., ge=1800, le=2100)
    end_year: Optional[int] = Field(None, ge=1800, le=2100)
    runtime_minutes: Optional[int]
    status: StatusEnum
    production_type: ProductionTypeEnum
    origin: OriginEnum
    synopsis: Optional[str]
    storyline: Optional[str] = Field(None, max_length=250)
    avant_site: Optional[str]
    avant_iaavim: bool = False
    user_id: str

class TitleCreateSchema(TitleBaseSchema):
    content_types: List[int] = []
    classifications: List[int] = []
    genres: List[int] = []
    themes: List[int] = []
    resolutions: List[int] = []
    funding_sources: List[FundingLinkSchema] = []
    crew: List[CrewLinkSchema] = []

class TitleReadSchema(TitleBaseSchema):
    id: UUID
    content_types: List[ContentTypeSchema] = []
    classifications: List[ClassificationSchema] = []
    genres: List[GenreSchema] = []
    themes: List[ThemeSchema] = []
    resolutions: List[ResolutionSchema] = []
    funding_sources: List[Dict[str, Union[FundingSourceSchema, ContributionEnum]]] = []
    episodes: List[EpisodeSchema] = []
    crew: List[Dict[str, Union[PersonSchema, CrewCategorySchema, str]]] = []

class TitleUpdateSchema(TitleBaseSchema):
    content_types: List[int] = []
    classifications: List[int] = []
    genres: List[int] = []
    themes: List[int] = []
    resolutions: List[int] = []
    funding_sources: List[FundingLinkSchema] = []
    crew: List[CrewLinkSchema] = []
