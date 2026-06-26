from typing import Dict, List

KEYWORDS: Dict[str, List[str]] = {
    "product_id": [
        "id", "sku", "code", "item_id", "prod_id",
        "product_code", "item_code", "asin"
    ],
    "product_name": [
        "name", "title", "product", "item", "prod",
        "product_title", "item_name", "prod_name",
        "product_nm", "prod_nm", "description"
    ],
    "brand_name": [
        "brand", "manufacturer", "mfr", "make",
        "vendor", "company", "brand_nm"
    ],
    "category": [
        "cat", "type", "ctgry", "category",
        "product_type", "item_type", "dept", "department"
    ],
    "sub_category": [
        "sub_cat", "subcat", "sub_type",
        "product_subtype", "sub_department"
    ],
    "unit_price": [
        "price", "sell_price", "selling_price",
        "rate", "mrp", "retail_price", "sale_price"
    ],
    "cost_price": [
        "cost", "cst", "vendor_price", "purchase_price",
        "buy_price", "landed_cost", "wholesale_price"
    ],
    "currency": [
        "curr", "currency_code", "ccy", "cur"
    ],
    "stock_quantity": [
        "qty", "quantity", "stock", "inventory",
        "units", "available", "stock_qty", "inv_qty"
    ],
    "warehouse_location": [
        "warehouse", "location", "loc", "wh",
        "storage", "bin", "rack", "shelf"
    ],
    "supplier_id": [
        "supplier_code", "vendor_id", "vendor_code",
        "sup_id", "seller_id"
    ],
    "supplier_name": [
        "supplier", "vendor", "seller",
        "sup_name", "vendor_name", "seller_name"
    ],
    "supplier_email": [
        "email", "supplier_email", "vendor_email",
        "contact_email", "sup_email"
    ],
    "supplier_country": [
        "country", "origin", "made_in",
        "country_of_origin", "source_country"
    ],
    "weight_kg": [
        "weight", "wt", "mass",
        "weight_kg", "wgt", "gross_weight"
    ],
    "dimensions_cm": [
        "dimensions", "size", "dim",
        "measurements", "lwh", "length_width_height"
    ],
    "color": [
        "colour", "clr", "color_name",
        "product_color", "shade"
    ],
    "material": [
        "material", "fabric", "composition",
        "mat", "substance", "made_of"
    ],
    "listing_status": [
        "status", "active", "state",
        "availability", "live", "enabled"
    ],
    "created_at": [
        "created", "create_date", "date_created",
        "creation_date", "added_on", "date_added"
    ],
    "updated_at": [
        "updated", "update_date", "date_updated",
        "modified", "last_modified", "date_modified"
    ],
}