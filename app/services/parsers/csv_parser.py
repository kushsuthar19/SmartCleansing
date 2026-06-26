from dataclasses import dataclass
from typing import AsyncGenerator,Any,List,Dict
import asyncio
import logging
import csv
import os
import aiofiles

logging.basicConfig(level=logging.INFO,format="%(asctime)s — %(levelname)s — %(message)s")

logger = logging.getLogger(__name__)

@dataclass
class CSVParser:
    file_path: str
    chunk_size: int = 500

    
    async def parse(self) -> AsyncGenerator[List[Dict[str,Any]],None]:
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"File Not Found: {self.file_path}")
        
        batch: List[Dict[str,Any]] = []
        headers: List[str] = []
        first_line = True

        
        async with aiofiles.open(self.file_path,'r', encoding="utf-8") as f:
                async for raw_line in f:
                     if first_line:
                          headers = next(csv.reader([raw_line.rstrip('\n')]))
                          first_line = False
                          continue
                     line = raw_line.rstrip('\n')
                     if not line:
                          continue

                     values = next(csv.reader([line]))
                     row = dict(zip(headers,values))
                     batch.append(row)

                     if len(batch) >= self.chunk_size:
                          yield batch 
                          batch = []
                          await asyncio.sleep(0)


                if batch:
                     yield batch
                     logger.info("Completed dataset streaming")           

            


async def main() -> None:
    parser = CSVParser("E:\\SmartCleansing\\Job_Placement_Data.csv", chunk_size=5)

    formated = parser.parse()
    async for data in formated:
        print(data)

if __name__ == "__main__":
    asyncio.run(main())

