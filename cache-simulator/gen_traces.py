import struct
import random


def gen_unified_trace(path: str, n_accesses: int = 200_000):
    """
    Gera um arquivo binário com n_accesses endereços (uint32 little-endian).
    Mistura acessos com localidade (loop) e acessos aleatórios.
    """
    random.seed(42)

    # região de código e dados só para simular algo parecido com programa real
    CODE_BASE = 0x00400000
    DATA_BASE = 0x10000000

    with open(path, "wb") as f:
        for i in range(n_accesses):
            r = random.random()

            if r < 0.6:
                # "código": acessos sequenciais num range pequeno (localidade espacial)
                addr = CODE_BASE + ((i * 4) % 0x4000)
            elif r < 0.9:
                # "dados": acessos com padrão de stride/mod (por exemplo, acesso a vetor)
                addr = DATA_BASE + ((i * 16) % 0x8000)
            else:
                # acessos bem aleatórios (poluição / conflitos)
                addr = random.randrange(0, 1 << 20)

            f.write(struct.pack("<I", addr))


def gen_split_trace(path: str, n_accesses: int = 200_000):
    """
    Gera um traço tipado: 1 byte (0=instrução, 1=dado) + 4 bytes de endereço.
    """
    random.seed(123)

    CODE_BASE = 0x00400000
    DATA_BASE = 0x10000000

    with open(path, "wb") as f:
        for i in range(n_accesses):
            # probabilidade de instrução vs dados (ajusta como quiser)
            if random.random() < 0.65:
                tipo = 0  # instrução
                addr = CODE_BASE + ((i * 4) % 0x4000)
            else:
                tipo = 1  # dado
                # padrão com alguma localidade + aleatoriedade
                if random.random() < 0.7:
                    addr = DATA_BASE + ((i * 16) % 0x8000)
                else:
                    addr = DATA_BASE + random.randrange(0, 1 << 15)

            f.write(bytes([tipo]))
            f.write(struct.pack("<I", addr))


if __name__ == "__main__":
    gen_unified_trace("trace_unified.bin", 200_000)
    print("Gerado trace_unified.bin")

    gen_split_trace("trace_split.bin", 200_000)
    print("Gerado trace_split.bin")
