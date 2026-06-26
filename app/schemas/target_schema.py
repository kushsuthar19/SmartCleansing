from pydantic import BaseModel, field_validator
from typing import Optional

class AmazonProductSchema(BaseModel):
    # Required fields
    product_id:          str
    product_name:        str

    # Semi-required
    category:            Optional[str]    = None
    unit_price:          Optional[float]  = None
    cost_price:          Optional[float]  = None
    currency:            Optional[str]    = None
    stock_quantity:      Optional[int]    = None
    brand_name:          Optional[str]    = None
    sub_category:        Optional[str]    = None
    warehouse_location:  Optional[str]    = None
    supplier_id:         Optional[str]    = None
    supplier_name:       Optional[str]    = None
    supplier_email:      Optional[str]    = None
    supplier_country:    Optional[str]    = None
    weight_kg:           Optional[float]  = None
    dimensions_cm:       Optional[str]    = None
    color:               Optional[str]    = None
    material:            Optional[str]    = None
    listing_status:      Optional[str]    = None
    created_at:          Optional[str]    = None
    updated_at:          Optional[str]    = None

    @field_validator('product_name', 'product_id')
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("cannot be empty")
        return v.strip()

    @field_validator('unit_price', 'cost_price', 'weight_kg')
    @classmethod
    def must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("must be positive")
        return v