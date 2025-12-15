import struct

from cache import Cache
from stats import Stats


def simulate_unified(cache: Cache, stats: Stats, path: str):
    # arquivo_de_entrada: [4 bytes endereco][4 bytes tipo] repetidos
    # tipo é ignorado na cache unificada
    with open(path, "rb") as f:
        while True:
            addr_b = f.read(4)
            if len(addr_b) < 4:
                break
            type_b = f.read(4)  # lê e ignora o tipo
            if len(type_b) < 4:
                break
            (addr,) = struct.unpack(">I", addr_b)  # uint32 big-endian
            cache.access(addr, stats)


def simulate_split(i_cache: Cache, i_stats: Stats,
                   d_cache: Cache, d_stats: Stats,
                   path: str):
    # arquivo_de_entrada (modo split):
    #   [4 bytes endereco][4 bytes tipo] repetidos
    #   tipo = 0 -> instrucao (iL1)
    #          1 -> dado (dL1)
    with open(path, "rb") as f:
        while True:
            addr_b = f.read(4)
            if len(addr_b) < 4:
                break  # EOF

            type_b = f.read(4)
            if len(type_b) < 4:
                break  # arquivo truncado

            (addr,) = struct.unpack(">I", addr_b)  # big-endian
            (tipo,) = struct.unpack(">I", type_b)

            if tipo == 0:
                # acesso de instrucao
                i_cache.access(addr, i_stats)
            else:
                # acesso de dado (tratamos qualquer coisa != 0 como dado)
                d_cache.access(addr, d_stats)
