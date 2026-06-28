from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class TypeLogement(str, Enum):
    studio = "studio"
    chambre = "chambre"
    colocation = "colocation"
    appartement = "appartement"


class SearchCriteria(BaseModel):
    ville: str
    type_logement: Optional[TypeLogement] = None
    meuble: Optional[bool] = None
    budget_max: Optional[float] = None
    budget_min: Optional[float] = None
    proximite: List[str] = []
    quartiers_preferes: List[str] = []
    disponibilite: Optional[str] = None
    criteres_speciaux: List[str] = []


class RawListing(BaseModel):
    titre: str
    prix: Optional[float] = None
    adresse: str
    description: str
    lien: str
    date_publication: Optional[str] = None
    source: str
    photos: List[str] = []


class ScoredListing(BaseModel):
    listing: RawListing
    score_pertinence: int
    prix_vs_marche: str
    signaux_arnaque: List[str]
    verdict: str
    explication: str


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    criteres: SearchCriteria
    resultats: List[ScoredListing]
    total_trouve: int
    total_retenu: int
    duree_recherche_sec: float
