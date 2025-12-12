from cache import Cache
from stats import Stats


def parse_config(cfg: str):
    # formato: nsets:bsize:assoc
    try:
        nsets_s, bsize_s, assoc_s = cfg.split(":")
    except ValueError:
        raise ValueError(f"Config invalida: {cfg}")
    return int(nsets_s), int(bsize_s), int(assoc_s)


def print_stats(title: str, cache: Cache, st: Stats):
    print(f"=== {title} ===")
    print(f"Config: nsets={cache.nsets}, bsize={cache.bsize}, assoc={cache.assoc}")
    print(f"TOTAL ACCESSES: {st.accesses}")
    print(f"HITS:           {st.hits}")
    print(f"MISSES:         {st.misses}")
    print(f"  COMPULSORIOS: {st.miss_compulsory}")
    print(f"  CAP+CONFLITO: {st.miss_capacity_conflict}")
    if st.accesses > 0:
        hit_ratio = st.hits / st.accesses
        miss_ratio = st.misses / st.accesses
        print(f"HIT RATIO:      {hit_ratio:.6f}")
        print(f"MISS RATIO:     {miss_ratio:.6f}")
    print()
