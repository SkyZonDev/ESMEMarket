from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class Sale(BaseModel):
    """
    @Description Modèle représentant une vente
    """
    order_id: str = Field(..., description="Identifiant unique de la commande")
    product: str = Field(..., description="Nom du produit")
    quantity: int = Field(..., gt=0, description="Quantité commandée")
    price: float = Field(..., gt=0, description="Prix unitaire")
    order_date: datetime = Field(..., description="Date de la commande")
    purchase_address: str = Field(..., description="Adresse d'achat")

class SaleCreate(BaseModel):
    """
    @Description Modèle pour la création d'une nouvelle vente
    """
    product: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    purchase_address: str

class SaleUpdate(BaseModel):
    """
    @Description Modèle pour la mise à jour d'une vente existante
    """
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)

class SalesFilter(BaseModel):
    """
    @Description Modèle pour le filtrage des ventes
    """
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_quantity: Optional[int] = Field(None, gt=0)
    max_quantity: Optional[int] = None
    min_price: Optional[float] = Field(None, gt=0)
    max_price: Optional[float] = None
    product: Optional[str] = None
