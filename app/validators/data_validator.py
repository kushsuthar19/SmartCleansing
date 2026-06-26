# Input:
#   batch          → [{"code": "ATL", "name": "Atlanta Airport", ...}]
#   mapping        → {"code": MappingResult(target="product_id"), ...}

# Output:
#   valid_rows     → rows that pass validation
#   invalid_rows   → rows that failed with reason why


# Required fields present   → product_name must exist
# 2. Type correctness          → unit_price must be float, not "abc"
# 3. Empty string check        → product_name cannot be ""
# 4. Null check                → required fields cannot be None

# Folder Location

from pydantic import BaseModel
from dataclasses import dataclass
from typing import List,Dict, Any
import logging
from schemas.target_schema import AmazonProductSchema
from mappers.column_mapper import MappingResult

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class ValidatedRow(BaseModel):
    original: Dict[str, Any]
    mapped: Dict[str, Any]      # renamed columns using mapping
    is_valid: bool
    errors: List[str]           # empty if valid

@dataclass
class DataValidator:
    batch: List[Dict[str,Any]]
    mapping: Dict[str,MappingResult]

    def validate(self) -> Dict[str,Any]:
        valid_rows = []
        invalid_rows = []

        for row in self.batch:
            mapped_row = {}
            for source_col,val in row.items():
                result = self.mapping.get(source_col)
                if result and result.target_column:
                    mapped_row[result.target_column] = val

            try:
                AmazonProductSchema(**mapped_row)
                is_valid = True
                errors = []
            
            except Exception as e:
                is_valid = False
                errors = [str(e)]
            

            validated = ValidatedRow(
                original=row,
                mapped=mapped_row,
                is_valid=is_valid,
                errors=errors
            )

            if is_valid:
                valid_rows.append(validated)
            else:
                invalid_rows.append(validated)

            
        logger.info(f"Valid: {len(valid_rows)} rows, Invalid: {len(invalid_rows)} rows")

        return {
            "valid": valid_rows,
            "invalid": invalid_rows
        }
                


