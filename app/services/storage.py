from pathlib import Path

from app.core.config import settings


class LocalStorage:
    def __init__(self, root: str = settings.storage_path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    async def save(self, key: str, content: bytes) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return key

    async def read(self, key: str) -> bytes:
        return (self.root / key).read_bytes()


storage = LocalStorage()
