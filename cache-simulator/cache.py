import math
import random

from stats import Stats


class Cache:
    def __init__(self, nsets: int, bsize: int, assoc: int):
        if nsets <= 0 or bsize <= 0 or assoc <= 0:
            raise ValueError("Parametros invalidos de cache")

        self.nsets = nsets # Conjuntos
        self.bsize = bsize # Tamanho do Bloco
        self.assoc = assoc # Associatividade

        # numero de bits de offset e indice (assumindo potencias de 2)
        self.offset_bits = int(math.log2(bsize))
        self.index_bits = int(math.log2(nsets)) if nsets > 1 else 0

        # lines[set][way] = {"valid": bool, "tag": int}
        self.lines = [
            [{"valid": False, "tag": 0} for _ in range(assoc)]
            for _ in range(nsets)
        ]

    def _decode_address(self, addr: int):
        if self.index_bits > 0:
            index_mask = (1 << self.index_bits) - 1
            index = (addr >> self.offset_bits) & index_mask
        else:
            index = 0  # totalmente associativa -> 1 conjunto

        tag = addr >> (self.offset_bits + self.index_bits)
        return tag, index

    def access(self, addr: int, stats: Stats):
        stats.accesses += 1

        tag, index = self._decode_address(addr)
        set_lines = self.lines[index]

        # 1) verifica HIT
        for line in set_lines:
            if line["valid"] and line["tag"] == tag:
                stats.hits += 1
                return

        # 2) MISS
        stats.misses += 1

        # compulsorio: todas as vias invalidas neste conjunto
        all_invalid = all(not line["valid"] for line in set_lines)
        if all_invalid:
            stats.miss_compulsory += 1
        else:
            stats.miss_capacity_conflict += 1

        # 3) escolhe via: primeiro via invalida, senao random
        target_line = None
        for line in set_lines:
            if not line["valid"]:
                target_line = line
                break

        if target_line is None:
            target_line = random.choice(set_lines)

        target_line["valid"] = True
        target_line["tag"] = tag
