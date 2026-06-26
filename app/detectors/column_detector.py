from pydantic import BaseModel
from enum import Enum
from typing import Any, List, Tuple, Dict
from collections import defaultdict, Counter
from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s — %(levelname)s — %(message)s")

logger = logging.getLogger(__name__)


class ColumnType(Enum):
    CATEGORICAL = "categorical"
    NUMERICAL = "numerical"
    TEXT = "text"
    UNKNOWN = "unknown"


class ColumnStats(BaseModel):
    name: str
    type: ColumnType
    unique_count: int
    null_count: int
    sample_values: List[Any]
    top_values: List[Tuple[str,int]]


@dataclass
class ColumnDetector():
    batch: List[Dict[str,Any]]
    sample_size: int=3
    top_n: int=5

    def analyze_col(self) -> Dict[str,ColumnStats]:
        columns: Dict[str,List[Any]] = defaultdict(list)
        for row in self.batch:
            for col,val in row.items():
                columns[col].append(val)

        
        results: Dict[str,ColumnStats] = {}
        
        for col,val in columns.items():
            non_null = [v for v in val if v is not None and str(v).strip() != " "]
            counter = Counter(str(v) for v in non_null)
            unique_count = len(counter)
            col_type = self._detect_type(non_null)
            null_count = sum(1 for v in val if v is None or v == "" or str(v).strip() == "")
            sample_values = list(dict.fromkeys(str(v) for v in non_null))[:self.sample_size]

            top_values: List[Tuple[str, int]] = []
            top_values: List[Tuple[str, int]] = []
            if col_type == ColumnType.CATEGORICAL:
                top_values = counter.most_common(self.top_n)
        
            results[col] = ColumnStats(
                name=col,
                type=col_type,
                unique_count=unique_count,
                null_count=null_count,
                sample_values=sample_values,
                top_values=top_values
            )

            logger.info(f"Column '{col}' -> {col_type.value},"
                        f"{unique_count} unique, {null_count} nulls")
        return results
    
    



    def _detect_type(self,values: List[Any]) -> ColumnType:
        if not values:
            return ColumnType.UNKNOWN
        numerical_count = 0
        for v in values:
            try:
                float(str(v))
                numerical_count+=1
            except ValueError:
                pass
        if numerical_count / len(values) > 0.8:
            return ColumnType.NUMERICAL
        
        unique_ratio = len(set(str(v) for v in values)) / len(values)
        if unique_ratio < 0.5:
            return ColumnType.CATEGORICAL

        return ColumnType.TEXT
    



def main() -> None:
    batch = [
        {"gender": "M", "ssc_percentage": "67", "status": "Placed"},
        {"gender": "F", "ssc_percentage": "79.33", "status": "Not Placed"},
        {"gender": "M", "ssc_percentage": "65", "status": "Placed"},
        {"gender": "M", "ssc_percentage": "56", "status": "Not Placed"},
        {"gender": "F", "ssc_percentage": "85.8", "status": "Placed"},
    ]

    detector = ColumnDetector(batch,2,3)

    results = detector.analyze_col()

    for col, stats in results.items():
        print(f"\n{col}:")
        print(f"  type         : {stats.type.value}")
        print(f"  unique_count : {stats.unique_count}")
        print(f"  null_count   : {stats.null_count}")
        print(f"  sample_values: {stats.sample_values}")
        print(f"  top_values   : {stats.top_values}")


if __name__ == "__main__":
    main()