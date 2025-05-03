from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid, random, string

@dataclass  # Automatically adds __init__, __repr__, and comparison methods
class Item:
    # Unique identifier using UUID4
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Random 6-character ASCII name
    name: str = field(default_factory=lambda: ''.join(random.choices(string.ascii_letters, k=6)))
    # Random date within the past year
    date: datetime = field(
        default_factory=lambda: datetime.now() - timedelta(days=random.randint(0, 365))
    )

def generate_items(n: int, seed: int = None) -> list[Item]:
    """
    Generate a list of `n` random Item instances.
    If `seed` is provided, the RNG will be seeded for reproducible output.
    """
    # Seed the RNG if a deterministic sequence is desired
    if seed is not None:
        random.seed(seed)

    # Instantiate `n` Items with unique IDs, random names, and random dates
    return [Item() for _ in range(n)]
