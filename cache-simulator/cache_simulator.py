import sys
import random

from cache import Cache
from stats import Stats
from simulator import simulate_unified, simulate_split
from utils import parse_config, print_stats


def main(argv):
    random.seed()

    # 1) cache_simulator arquivo_de_entrada   -> default 1024:4:1
    # 2) cache_simulator nsets:bsize:assoc arquivo_de_entrada
    # 3) cache_simulator nI:bI:assocI nD:bD:assocD arquivo_de_entrada

    if len(argv) == 2:
        # default: 1024 conjuntos, bloco 4 bytes, assoc 1
        input_file = argv[1]
        nsets, bsize, assoc = 1024, 4, 1

        L1 = Cache(nsets, bsize, assoc)
        st = Stats()

        simulate_unified(L1, st, input_file)
        print_stats("L1 UNIFICADA (default 1024:4:1)", L1, st)
        return 0

    if len(argv) == 3:
        # cache unica L1 parametrizada
        cfg = argv[1]
        input_file = argv[2]
        nsets, bsize, assoc = parse_config(cfg)

        L1 = Cache(nsets, bsize, assoc)
        st = Stats()

        simulate_unified(L1, st, input_file)
        print_stats("L1 UNIFICADA", L1, st)
        return 0

    if len(argv) == 4:
        # cache split: iL1 e dL1
        cfg_i = argv[1]
        cfg_d = argv[2]
        input_file = argv[3]

        nsets_i, bsize_i, assoc_i = parse_config(cfg_i)
        nsets_d, bsize_d, assoc_d = parse_config(cfg_d)

        iL1 = Cache(nsets_i, bsize_i, assoc_i)
        dL1 = Cache(nsets_d, bsize_d, assoc_d)
        stI = Stats()
        stD = Stats()

        simulate_split(iL1, stI, dL1, stD, input_file)

        print_stats("Instruction Cache L1 (iL1)", iL1, stI)
        print_stats("Data Cache L1 (dL1)", dL1, stD)
        return 0

    print(
        "Uso:\n"
        f"  {argv[0]} arquivo_de_entrada\n"
        f"  {argv[0]} <nsets_L1>:<bsize_L1>:<assoc_L1> arquivo_de_entrada\n"
        f"  {argv[0]} <nsets_iL1>:<bsize_iL1>:<assoc_iL1> <nsets_dL1>:<bsize_dL1>:<assoc_dL1> arquivo_de_entrada"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
