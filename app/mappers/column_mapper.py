from dataclasses import dataclass
from typing import Dict,List,Optional
from detectors.column_detector import ColumnStats
from pydantic import BaseModel
from enum import Enum
from mappers.keywords import KEYWORDS
from difflib import SequenceMatcher
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class Methods(Enum):
    EXACT = "exact"
    CONTAINS = "contains"
    KEYWORD = "keyword"
    SIMILARITY = "similarity"
    NONE = "none"


class MappingResult(BaseModel):
    source_column: str
    target_column: Optional[str]
    confidence: float
    method: Methods


@dataclass
class ColumnMaper:
    detected_columns: Dict[str,ColumnStats]
    target_schema: List[str]

    def map_rules(self) -> Dict[str,MappingResult]:
        if not self.detected_columns:
            raise Exception(f"{self.detected_columns} is empty")
        
        mapping_result: Dict[str,MappingResult]= {}
        

# exact match
        for col in self.detected_columns.keys():
            key = col.lower()
            result = self._map_single(col,key)
            mapping_result[col] = result
            logger.info(
                f"'{col}' → '{result.target_column}' "
                f"({result.method.value}, {result.confidence})"
            )
            
        return mapping_result


    def _map_single(self,original,key):
        
        # for exact match 
        if key in self.target_schema:
                return MappingResult(
                    source_column=original,
                    target_column=key,
                    confidence=1.0,
                    method=Methods.EXACT
                )
        
        #contains
        for target in self.target_schema:
            if target in key or key in target:
                return MappingResult(
                    source_column=original,
                    target_column=target,
                    confidence=0.8,
                    method=Methods.CONTAINS
                )
        
       #keyword match
        for col,row in KEYWORDS.items():
            if key in row:
                return MappingResult(
                    source_column=original,
                    target_column=col,
                    confidence=0.7,
                    method=Methods.KEYWORD
                )

        # similarity
        best_match = max(self.target_schema, key = lambda t: SequenceMatcher(None,key,t).ratio())
        best_score = round(SequenceMatcher(None,key,best_match).ratio(),2)

        if best_score > 0.5:
            return MappingResult(
                source_column=original,
                target_column=best_match,
                confidence=best_score,
                method= Methods.SIMILARITY
            )

        # None
        return MappingResult(
            source_column=original,
            target_column=None,
            confidence=0.0,
            method=Methods.NONE
        )
        
            
            