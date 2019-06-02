#!/usr/bin/env python3

import time
from regras_jogo.regras_abstratas import construir_jogo
from agentes.abstrato import construir_agente


def ler_tempo(em_turnos=True):
    """ Se o jogo for em turnos, passe 1 (rodada), senão se o jogo for
    continuo ou estratégico, precisa.
    """
    return 1 if em_turnos else time.time()


def iniciar_jogo():

    # Inicializar e configurar jogo
    jogo = construir_jogo()
    id_jogador, jogador = jogo.registrarAgenteJogador(), construir_agente()
    tempo_de_jogo = 0

    while not jogo.isFim():

        # Mostrar mundo ao jogador
        ambiente_perceptivel = jogo.gerarCampoVisao(id_jogador)
        jogador.adquirirPercepcao(ambiente_perceptivel)

        # Decidir jogada e apresentar ao jogo
        acao = jogador.escolherProximaAcao()
        jogo.registrarProximaAcao(id_jogador, acao)

        # Atualizar jogo
        tempo_corrente = ler_tempo()
        jogo.atualizarEstado(tempo_corrente - tempo_de_jogo)
        tempo_de_jogo += tempo_corrente


if __name__ == '__main__':
    iniciar_jogo()
