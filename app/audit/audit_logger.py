from dataclasses import dataclass
from typing import Dict
import aiofiles
import json
import logging
import uuid
import datetime
from mappers.column_mapper import MappingResult

logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class AuditLogger:
    source_file: str
    total_rows: int
    valid_rows: int
    invalid_rows: int
    mapping: Dict[str, MappingResult]
    duration_seconds: float
    output_path: str = "audit_log.jsonl"

    async def log(self) -> None:
        run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.datetime.now().isoformat()

        record = {
            "run_id": run_id,
            "timestamp": timestamp,
            "source_file": self.source_file,
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "confidence_scores": {
                col: result.confidence
                for col, result in self.mapping.items()
            },
            "mapped_columns": [
                col for col, result in self.mapping.items()
                if result.target_column is not None
            ],
            "unmapped_columns": [
                col for col, result in self.mapping.items()
                if result.target_column is None
            ],
            "duration_seconds": self.duration_seconds,
        }

        async with aiofiles.open(self.output_path, 'a', encoding='utf-8') as f:
            await f.write(json.dumps(record, ensure_ascii=False) + "\n")

        logger.info(
            f"Audit logged — run_id: {run_id}, "
            f"valid: {self.valid_rows}, "
            f"invalid: {self.invalid_rows}, "
            f"duration: {self.duration_seconds}s"
        )