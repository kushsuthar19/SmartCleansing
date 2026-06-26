from services.parsers.protocol_parser import BaseParser
from services.parsers.csv_parser import CSVParser
from services.parsers.json_parser import JSONParser
from dataclasses import dataclass
import asyncio

@dataclass
class ParseRouter:
    file_path: str
    chunk_size: int = 50

    def get_parser(self) -> BaseParser:
        if self.file_path.lower().endswith(".csv"):
            return CSVParser(self.file_path, self.chunk_size)
            
        elif self.file_path.lower().endswith(".json"):
            return JSONParser(self.file_path, self.chunk_size)
        else:
            raise ValueError("Not supported Data Format")

async def main() -> None:
    router = ParseRouter("E:\SmartCleansing\Job_Placement_Data.csv",chunk_size=5)

    parser = router.get_parser()
    
    
    async for batch in parser.parse():
        print(batch)


if __name__ == "__main__":
    asyncio.run(main())