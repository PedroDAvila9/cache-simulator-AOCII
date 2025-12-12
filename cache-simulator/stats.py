from dataclasses import dataclass


@dataclass
class Stats:
    accesses: int = 0
    hits: int = 0
    misses: int = 0
    miss_compulsory: int = 0
    miss_capacity_conflict: int = 0
