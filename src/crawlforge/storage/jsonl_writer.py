import json
import asyncio
import aiofiles


class JSONLWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = asyncio.Lock()

    async def write(self, data: dict):
        """Append a record to the JSONL file safely across workers."""
        async with self.lock:
            async with aiofiles.open(self.file_path, "a", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False) + "\n")
