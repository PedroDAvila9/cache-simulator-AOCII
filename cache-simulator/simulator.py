import struct

from cache import Cache
from stats import Stats


def simulate_unified(cache: Cache, stats: Stats, path: str):
    # arquivo_de_entrada: sequencia de enderecos uint32 (32 bits)
    with open(path, "rb") as f:
        data = f.read(4)
        while data:
            (addr,) = struct.unpack("<I", data)  # uint32 little-endian
            cache.access(addr, stats)
            data = f.read(4)


def simulate_split(i_cache: Cache, i_stats: Stats,
                   d_cache: Cache, d_stats: Stats,
                   path: str):
    # arquivo_de_entrada (modo split):
    #   [1 byte tipo][4 bytes endereco] repetidos
    #   tipo = 0 -> instrucao (iL1)
    #          1 -> dado (dL1)
    with open(path, "rb") as f:
        while True:
            type_b = f.read(1)
            if not type_b:
                break  # EOF

            addr_b = f.read(4)
            if len(addr_b) < 4:
                break  # arquivo truncado

            tipo = type_b[0]              # inteiro 0..255
            (addr,) = struct.unpack("<I", addr_b)

            if tipo == 0:
                # acesso de instrucao
                i_cache.access(addr, i_stats)
            else:
                # acesso de dado (tratamos qualquer coisa != 0 como dado)
                d_cache.access(addr, d_stats)
