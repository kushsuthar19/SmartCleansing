from dataclasses import dataclass
from typing import List, Dict, Any
import aiofiles
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class OutputWriter:
    transformed_rows: List[Dict[str, Any]]
    output_path: str = "output.jsonl"

    async def write(self) -> None:
        if not self.transformed_rows:
            raise ValueError("No transformed rows to write")

        logger.info(f"Writing {len(self.transformed_rows)} rows to {self.output_path}")

        try:
            async with aiofiles.open(self.output_path, 'w', encoding='utf-8') as f:
                for row in self.transformed_rows:
                    line = json.dumps(row, ensure_ascii=False)
                    await f.write(line + "\n")

            logger.info(f"Output file written successfully → {self.output_path}")

        except Exception as e:
            logger.error(f"Failed to write output: {e}")
            raise