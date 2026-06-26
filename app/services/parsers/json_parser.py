from typing import AsyncGenerator, List, Dict, Any
from dataclasses import dataclass
import aiofiles
import asyncio
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)

MAX_JSON_SIZE = 500 * 1024 * 1024  # 500MB


@dataclass
class JSONParser:
    file_path: str
    chunk_size: int = 500

    async def parse(self) -> AsyncGenerator[List[Dict[str, Any]], None]:
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        file_size = os.path.getsize(self.file_path)
        batch: List[Dict[str, Any]] = []

        # --- detect JSONL first by peeking ---
        async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
            first_line = ""
            async for line in f:
                if line.strip():
                    first_line = line.strip()
                    break

        is_jsonl = first_line.startswith('{') and not self._is_nested_object(first_line)

        if is_jsonl:
            # JSONL — truly streaming, memory efficient
            logger.info("Detected JSONL format")
            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    batch.append(json.loads(line))
                    if len(batch) >= self.chunk_size:
                        yield batch
                        batch = []
                        await asyncio.sleep(0)

        else:
            # JSON object or array — must load fully
            if file_size > MAX_JSON_SIZE:
                raise ValueError(
                    f"JSON file too large ({file_size // 1024 // 1024}MB). "
                    f"Convert to JSONL for files over 500MB."
                )

            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as f:
                content = await f.read()

            data = json.loads(content)
            records = self._extract_records(data)

            for row in records:
                batch.append(row)
                if len(batch) >= self.chunk_size:
                    yield batch
                    batch = []
                    await asyncio.sleep(0)

        if batch:
            yield batch

        logger.info("Completed JSON dataset streaming")

    def _is_nested_object(self, line: str) -> bool:
        # a single JSONL line is a complete object on one line
        # a nested JSON object spans multiple lines
        try:
            data = json.loads(line)
            # if it parsed and contains a list value, it's nested
            return isinstance(data, dict) and any(
                isinstance(v, list) for v in data.values()
            )
        except json.JSONDecodeError:
            return True  # incomplete line = multi-line JSON object

    def _extract_records(self, data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            logger.info("Detected bare JSON array")
            return data

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    logger.info(f"Detected nested JSON — records under key: '{key}'")
                    return value

        raise ValueError(f"No list of records found in JSON structure")


async def main() -> None:
    parser = JSONParser(
        "E:\\SmartCleansing\\airports.json",
        chunk_size=10
    )
    async for batch in parser.parse():
        print(f"Batch of {len(batch)} rows — first: {batch[0]}")


if __name__ == "__main__":
    asyncio.run(main())