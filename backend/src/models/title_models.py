import uuid
from enum import Enum as PyEnum
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, SmallInteger,
    Enum, ForeignKey, Table
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, declarative_base
from src.database import Base

# -----------------------
# Enumeraciones SQLAlchemy
# -----------------------
class StatusEnum(PyEnum):
    desarrollo = "desarrollo"
    preproduccion = "preproducción"
    rodaje = "rodaje"
    produccion = "producción"
    postproduccion = "postproducción"
    estreno = "estreno"
    finalizada = "finalizada"
    cancelada = "cancelada"

class ProductionTypeEnum(PyEnum):
    comunitaria = "comunitaria"
    independiente = "independiente"
    industrial = "industrial"

class OriginEnum(PyEnum):
    Misiones = "Misiones"
    Region = "Región"
    Argentina = "Argentina"
    Internacional = "Internacional"

class ContributionEnum(PyEnum):
    total = "total"
    parcial = "parcial"

class ResolutionLabelEnum(PyEnum):
    p480 = "480p"
    p720 = "720p"
    p1080 = "1080p"
    k4 = "4K"

class ClassificationCodeEnum(PyEnum):
    ATP = "ATP"
    PLUS13 = "+13"
    PLUS16 = "+16"
    PLUS18 = "+18"
    C = "C"

# -----------------------
# Tablas de asociación M:N
# -----------------------

title_content_types = Table(
    'title_content_types', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('content_type_id', Integer, ForeignKey('content_types.id'), primary_key=True)
)

title_classifications = Table(
    'title_classifications', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('classification_id', Integer, ForeignKey('classifications.id'), primary_key=True)
)

title_genres = Table(
    'title_genres', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

title_themes = Table(
    'title_themes', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('theme_id', Integer, ForeignKey('themes.id'), primary_key=True)
)

title_resolutions = Table(
    'title_resolutions', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('resolution_id', Integer, ForeignKey('resolutions.id'), primary_key=True)
)

title_funding = Table(
    'title_funding', Base.metadata,
    Column('title_id', UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True),
    Column('funding_source_id', Integer, ForeignKey('funding_sources.id'), primary_key=True),
    Column('contribution', Enum(ContributionEnum), nullable=False)
)

# -----------------------
# Modelos SQLAlchemy
# -----------------------

class Title(Base):
    __tablename__ = 'titles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_title = Column(String, nullable=False)
    original_title = Column(String, nullable=True)
    start_year = Column(SmallInteger, nullable=False)
    end_year = Column(SmallInteger, nullable=True)
    runtime_minutes = Column(Integer, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)
    production_type = Column(Enum(ProductionTypeEnum), nullable=False)
    origin = Column(Enum(OriginEnum), nullable=False)
    synopsis = Column(Text, nullable=True)
    storyline = Column(String(250), nullable=True)
    avant_site = Column(String, nullable=True)
    avant_iaavim = Column(Boolean, default=False)

    content_types = relationship('ContentType', secondary=title_content_types, back_populates='titles')
    classifications = relationship('Classification', secondary=title_classifications, back_populates='titles')
    genres = relationship('Genre', secondary=title_genres, back_populates='titles')
    themes = relationship('Theme', secondary=title_themes, back_populates='titles')
    resolutions = relationship('Resolution', secondary=title_resolutions, back_populates='titles')
    funding_sources = relationship('FundingSource', secondary=title_funding, back_populates='titles')

    episodes = relationship('Episode', primaryjoin='Title.id==Episode.series_id', back_populates='series')
    crew = relationship('Crew', back_populates='title', cascade='all, delete')

class ContentType(Base):
    __tablename__ = 'content_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    titles = relationship('Title', secondary=title_content_types, back_populates='content_types')

class Classification(Base):
    __tablename__ = 'classifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Enum(ClassificationCodeEnum), unique=True, nullable=False)
    titles = relationship('Title', secondary=title_classifications, back_populates='classifications')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    titles = relationship('Title', secondary=title_genres, back_populates='genres')

class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    titles = relationship('Title', secondary=title_themes, back_populates='themes')

class Resolution(Base):
    __tablename__ = 'resolutions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(Enum(ResolutionLabelEnum), nullable=False)
    aspect_ratio = Column(String, nullable=True)
    titles = relationship('Title', secondary=title_resolutions, back_populates='resolutions')

class FundingSource(Base):
    __tablename__ = 'funding_sources'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    titles = relationship('Title', secondary=title_funding, back_populates='funding_sources')

class CrewCategory(Base):
    __tablename__ = 'crew_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

class Person(Base):
    __tablename__ = 'people'
    nconst = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    birth_year = Column(SmallInteger, nullable=True)
    death_year = Column(SmallInteger, nullable=True)
    professions = Column(ARRAY(String), nullable=True)
    crew_entries = relationship('Crew', back_populates='person')

class Episode(Base):
    __tablename__ = 'title_episodes'
    episode_id = Column(UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True)
    series_id = Column(UUID(as_uuid=True), ForeignKey('titles.id'), nullable=False)
    season_number = Column(SmallInteger, nullable=False)
    episode_number = Column(SmallInteger, nullable=False)

    series = relationship('Title', foreign_keys=[series_id], back_populates='episodes')
    episode = relationship('Title', foreign_keys=[episode_id])

class Crew(Base):
    __tablename__ = 'title_crew'
    title_id = Column(UUID(as_uuid=True), ForeignKey('titles.id'), primary_key=True)
    person_id = Column(String, ForeignKey('people.nconst'), primary_key=True)
    crew_category_id = Column(Integer, ForeignKey('crew_categories.id'), nullable=False)
    ordering = Column(SmallInteger, nullable=False)
    job = Column(String, nullable=True)
    characters = Column(String, nullable=True)

    title = relationship('Title', back_populates='crew')
    person = relationship('Person', back_populates='crew_entries')
    category = relationship('CrewCategory')
