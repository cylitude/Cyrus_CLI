from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid, random, string

@dataclass
class Item:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = field(default_factory=lambda: ''.join(random.choices(string.ascii_letters, k=6)))
    date: datetime = field(default_factory=lambda: datetime.now() - timedelta(days=random.randint(0, 365)))

def generate_items(n: int, seed: int = None) -> list[Item]:
    """
    Generate a list of n random Item instances.
    If seed is provided, the RNG will be seeded for reproducible output.
    """
    if seed is not None:
        random.seed(seed)
    return [Item() for _ in range(n)]
