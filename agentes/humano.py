from agentes.abstrato import AgenteAbstrato
import sys
import random
import pygame
from pygame.locals import *


class AgentePrepostoESHumano(AgenteAbstrato):

    def adquirirPercepcao(self, percepcao_mundo):
        """ Inspeciona a disposicao dos elementos no objeto de visao e escreve
        na tela para o usuário saber o que seu agente está percebendo.
        """
        screen = percepcao_mundo['screen']
        playerImage = percepcao_mundo['playerImage']
        alienImage = percepcao_mundo['alienImage']
        background = percepcao_mundo['background']
        shotImage = percepcao_mundo['shotImage']
        explosionImage = percepcao_mundo['explosionImage']
        aliens = percepcao_mundo['aliens']
        player = percepcao_mundo['player']
        shots = percepcao_mundo['shots']
        explosions = percepcao_mundo['explosions']
        self.pygame = percepcao_mundo['pygame']

        screen.blit(background, (0, 0))
        for a in aliens:
            screen.blit(alienImage, a.rect)
        screen.blit(playerImage, player.rect)
        for shot in shots:
            screen.blit(shotImage, shot.rect)
        for explosion in explosions:
            screen.blit(explosionImage, explosion.rect)
        pygame.display.flip()

    def escolherProximaAcao(self):
        from acoes_agentes import AcaoJogador

        direction = 0

        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                import sys
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    direction = 100
                    return AcaoJogador.mover(direction)
                elif event.key == K_LEFT:
                    direction = -100
                    return AcaoJogador.mover(direction)
                elif event.key == K_SPACE:
                    return AcaoJogador.atirar()
