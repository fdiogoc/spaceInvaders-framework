from dataclasses import dataclass
from enum import Enum


class AcoesJogador(Enum):
    ATIRAR = "atirar"
    MOVER = "mover"


@dataclass
class AcaoJogador():
    tipo: str
    parametros: tuple = tuple()

    @classmethod
    def mover(cls, direction):
        return cls(AcoesJogador.MOVER, direction)

    @classmethod
    def atirar(cls):
        return cls(AcoesJogador.ATIRAR)
