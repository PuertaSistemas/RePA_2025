import uuid
from enum import Enum as PyEnum
from typing import List, Optional
from pydantic import BaseModel

# -----------------------
# Enums Pydantic
# -----------------------
class StatusEnumStr(str, PyEnum):
    desarrollo = "desarrollo"
    preproduccion = "preproducción"
    rodaje = "rodaje"
    produccion = "producción"
    postproduccion = "postproducción"
    estreno = "estreno"
    finalizada = "finalizada"
    cancelada = "cancelada"

class ProductionTypeEnumStr(str, PyEnum):
    comunitaria = "comunitaria"
    independiente = "independiente"
    industrial = "industrial"

class OriginEnumStr(str, PyEnum):
    Misiones = "Misiones"
    Region = "Región"
    Argentina = "Argentina"
    Internacional = "Internacional"

class ContributionEnumStr(str, PyEnum):
    total = "total"
    parcial = "parcial"

class ResolutionLabelEnumStr(str, PyEnum):
    p480 = "480p"
    p720 = "720p"
    p1080 = "1080p"
    k4 = "4K"

class ClassificationCodeEnumStr(str, PyEnum):
    ATP = "ATP"
    PLUS13 = "+13"
    PLUS16 = "+16"
    PLUS18 = "+18"
    C = "C"

# -----------------------
# Schemas principales: Titles
# -----------------------
class TitleCreateSchema(BaseModel):
    primary_title: str
    original_title: Optional[str]
    start_year: int
    end_year: Optional[int]
    runtime_minutes: Optional[int]
    status: StatusEnumStr
    production_type: ProductionTypeEnumStr
    origin: OriginEnumStr
    synopsis: Optional[str]
    storyline: Optional[str]
    avant_site: Optional[str]
    avant_iaavim: bool

class TitleUpdateSchema(BaseModel):
    primary_title: Optional[str]
    original_title: Optional[str]
    start_year: Optional[int]
    end_year: Optional[int]
    runtime_minutes: Optional[int]
    status: Optional[StatusEnumStr]
    production_type: Optional[ProductionTypeEnumStr]
    origin: Optional[OriginEnumStr]
    synopsis: Optional[str]
    storyline: Optional[str]
    avant_site: Optional[str]
    avant_iaavim: Optional[bool]

class TitleReadSchema(BaseModel):
    id: uuid.UUID
    primary_title: str
    original_title: Optional[str]
    start_year: int
    end_year: Optional[int]
    runtime_minutes: Optional[int]
    status: StatusEnumStr
    production_type: ProductionTypeEnumStr
    origin: OriginEnumStr
    synopsis: Optional[str]
    storyline: Optional[str]
    avant_site: Optional[str]
    avant_iaavim: bool

    class Config:
        orm_mode = True

# -----------------------
# Schemas Entidades Auxiliares
# -----------------------
class ContentTypeCreateSchema(BaseModel):
    name: str

class ContentTypeUpdateSchema(BaseModel):
    name: Optional[str]

class ContentTypeReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ClassificationCreateSchema(BaseModel):
    code: ClassificationCodeEnumStr

class ClassificationUpdateSchema(BaseModel):
    code: Optional[ClassificationCodeEnumStr]

class ClassificationReadSchema(BaseModel):
    id: int
    code: ClassificationCodeEnumStr

    class Config:
        orm_mode = True

class GenreCreateSchema(BaseModel):
    name: str

class GenreUpdateSchema(BaseModel):
    name: Optional[str]

class GenreReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class LanguageCreateSchema(BaseModel):
    name: str

class LanguageUpdateSchema(BaseModel):
    name: Optional[str]

class LanguageReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ThemeCreateSchema(BaseModel):
    name: str

class ThemeUpdateSchema(BaseModel):
    name: Optional[str]

class ThemeReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ResolutionCreateSchema(BaseModel):
    label: ResolutionLabelEnumStr
    aspect_ratio: Optional[str]

class ResolutionUpdateSchema(BaseModel):
    label: Optional[ResolutionLabelEnumStr]
    aspect_ratio: Optional[str]

class ResolutionReadSchema(BaseModel):
    id: int
    label: ResolutionLabelEnumStr
    aspect_ratio: Optional[str]

    class Config:
        orm_mode = True

class FundingSourceCreateSchema(BaseModel):
    name: str

class FundingSourceUpdateSchema(BaseModel):
    name: Optional[str]

class FundingSourceReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CrewCategoryCreateSchema(BaseModel):
    name: str

class CrewCategoryUpdateSchema(BaseModel):
    name: Optional[str]

class CrewCategoryReadSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PersonCreateSchema(BaseModel):
    nconst: str
    name: str
    birth_year: Optional[int]
    death_year: Optional[int]
    professions: Optional[List[str]]

class PersonUpdateSchema(BaseModel):
    name: Optional[str]
    birth_year: Optional[int]
    death_year: Optional[int]
    professions: Optional[List[str]]

class PersonReadSchema(BaseModel):
    nconst: str
    name: str
    birth_year: Optional[int]
    death_year: Optional[int]
    professions: Optional[List[str]]

    class Config:
        orm_mode = True

# -----------------------
# Schemas Relaciones M:N y 1:N
# -----------------------
class TitleContentTypeLinkSchema(BaseModel):
    title_id: uuid.UUID
    content_type_id: int

class TitleClassificationLinkSchema(BaseModel):
    title_id: uuid.UUID
    classification_id: int

class TitleGenreLinkSchema(BaseModel):
    title_id: uuid.UUID
    genre_id: int

class TitleThemeLinkSchema(BaseModel):
    title_id: uuid.UUID
    theme_id: int

class TitleResolutionLinkSchema(BaseModel):
    title_id: uuid.UUID
    resolution_id: int

class TitleFundingLinkSchema(BaseModel):
    title_id: uuid.UUID
    funding_source_id: int
    contribution: ContributionEnumStr

class EpisodeCreateSchema(BaseModel):
    episode_id: uuid.UUID
    series_id: uuid.UUID
    season_number: int
    episode_number: int

class EpisodeReadSchema(BaseModel):
    episode_id: uuid.UUID
    series_id: uuid.UUID
    season_number: int
    episode_number: int

    class Config:
        orm_mode = True

class CrewEntryCreateSchema(BaseModel):
    title_id: uuid.UUID
    person_id: str
    crew_category_id: int
    ordering: int
    job: Optional[str]
    characters: Optional[str]

class CrewEntryReadSchema(BaseModel):
    title_id: uuid.UUID
    person_id: str
    crew_category_id: int
    ordering: int
    job: Optional[str]
    characters: Optional[str]

    class Config:
        orm_mode = True
