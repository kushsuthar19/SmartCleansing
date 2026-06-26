from dataclasses import dataclass
from typing import List,Any
from validators.data_validator import ValidatedRow
import logging 
import re

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)




@dataclass
class DataTransformer:
    valid_rows:List[ValidatedRow]
    

    def transform(self) -> List[ValidatedRow]:
        
        
        transformed_rows = []
        for validated_row in self.valid_rows:
            transformed = {}
            mapped = validated_row.mapped

            for col,val in mapped.items():
                val = self._transform_value(col=col,val=val)
                transformed[col] = val
            
            transformed_rows.append(transformed)
        
        logger.info(f"Transformed {len(transformed_rows)} rows")
        return transformed_rows





    def _transform_value(self, col: str, val: Any) -> Any:
        
        TITLE_CASE_FIELDS = ["product_name", "brand_name", "supplier_name"]
        UPPER_CASE_FIELDS = ["product_id", "supplier_country", "currency"]
        UNKNOWN_VALUES = {"n/a", "null", "none", "na", "-", "unknown", ""}
        
        if val is None:
            return None

        # string transformations
        if isinstance(val, str):
            val = val.strip()

            # normalize unknown values
            if val.lower() in UNKNOWN_VALUES:
                return None

            # title case
            if col in TITLE_CASE_FIELDS:
                return val.title()

            # upper case
            if col in UPPER_CASE_FIELDS:
                return val.upper()

            # strip currency symbols → float
            if col in ("unit_price", "cost_price"):
                return self._to_float(val)

            # strip non-numeric → int
            if col in ("stock_quantity",):
                return self._to_int(val)

        return val




    def _to_float(self, val: str) -> Any:
        cleaned = re.sub(r"[^\d.]", "", val)
        try:
            return float(cleaned)
        except ValueError:
            logger.warning(f"Could not convert '{val}' to float")
            return None

    def _to_int(self, val: str) -> Any:
        cleaned = re.sub(r"[^\d]", "", val)
        try:
            return int(cleaned)
        except ValueError:
            logger.warning(f"Could not convert '{val}' to int")
            return None
