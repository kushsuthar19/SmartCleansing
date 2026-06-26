from typing import Protocol, AsyncGenerator, List, Dict,Any

class BaseParser(Protocol):
    async def parse(self) -> AsyncGenerator[List[Dict[str,Any]],None]:
        ...