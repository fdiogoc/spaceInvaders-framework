from regras_jogo.regras_abstratas import AbstractRegrasJogo
from enum import Enum, auto


import random
import pygame
from pygame.locals import *

# CONSTANTES
SCREENRECT = Rect(0, 0, 600, 600)

# IMAGENS
playerImage = pygame.image.load("player.png")
alienImage = pygame.image.load("alien.png")
background = pygame.image.load("background.png")
shotImage = pygame.image.load("bullet.png")
explosionImage = pygame.image.load("explosion.png")

screen = pygame.display.set_mode(SCREENRECT.size)
pygame.init()


class Actor:

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def update(self):
        pass


class Player(Actor):

    def __init__(self):
        Actor.__init__(self, playerImage)
        self.life = 1
        self.reloading = 0
        self.rect.centerx = SCREENRECT.centerx
        self.rect.bottom = SCREENRECT.bottom

    def move(self, direction):
        self.rect = self.rect.move(
            direction, 0).clamp(SCREENRECT)


class Alien(Actor):

    def __init__(self):
        Actor.__init__(self, alienImage)

        self.speed = 50
        self.rect.centerx = SCREENRECT.centerx

    def update(self):
        global SCREENRECT
        self.rect[0] = self.rect[0] + self.speed
        if not SCREENRECT.contains(self.rect):
            self.speed = -self.speed
            self.rect.top = self.rect.bottom + 80
            self.rect = self.rect.clamp(SCREENRECT)


class Shot(Actor):

    def __init__(self, player):
        Actor.__init__(self, shotImage)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top - 10

    def update(self):
        self.rect.top = self.rect.top - 100


class Explosion(Actor):

    def __init__(self, actor):
        Actor.__init__(self, explosionImage)
        self.life = 2
        self.rect.center = actor.rect.center

    def update(self):
        self.life = self.life - 1


class AgentesOrdenador(Enum):
    JOGADOR_PADRAO = auto()


class SpaceInvaders(AbstractRegrasJogo):

    def __init__(self):

        self.pygame = pygame

        # CRIA AS SPRITES
        self.player = Player()
        self.aliens = [Alien()]
        self.shots = []
        self.explosions = []

    def registrarAgenteJogador(self, elem_agente=AgentesOrdenador.JOGADOR_PADRAO):
        """ Só há um agente, o jogador, então não preciso de lógica.
        """
        return 1

    def isFim(self):
        """ Se o player ficar sem life o jogo acaba.
        """
        if self.player.life < 1:
            return True
        return False

    def gerarCampoVisao(self, id_agente):
        """ 
        variaveis do campo de visao
        """
        return {
            "screen": screen,
            "playerImage": playerImage,
            "alienImage": alienImage,
            "background": background,
            "shotImage": shotImage,
            "explosionImage": explosionImage,
            "player": self.player,
            "aliens": self.aliens,
            "shots": self.shots,
            "explosions": self.explosions,
            "pygame": self.pygame

        }

    def registrarProximaAcao(self, id_agente, acao):
        """ Como só há um agente atuando no mundo, o próprio jogador, não é
        necessário nenhum mecanismo para guardar ações associadas por agentes
        distintos.
        """
        self.acao_jogador = acao

    def atualizarEstado(self, diferencial_tempo):
        """ Não preciso me preocupar com a passagem do tempo, pois só uma
        jogada é feita por vez, e o jogo não muda seu estado sem jogadas.

        Verifico a ação última registrada e atualizado o estado do jogo
        computando-a.

        Sempre verifica a lista de colisao, e executa a ação tomada
        """
        from acoes_agentes import AcoesJogador

        # CRIA COLISAO
        alienrects = []
        for a in self.aliens:
            alienrects.append(a.rect)

        # collidelist retorna -1 caso falso ou o index
        hit = self.player.rect.collidelist(alienrects)
        for explosion in self.explosions:
            if explosion.life <= 0:
                self.explosions.remove(explosion)
        if hit != -1:
            alien = self.aliens[hit]
            self.explosions.append(Explosion(alien))
            self.explosions.append(Explosion(self.player))
            self.player.life = self.player.life - 1
        for shot in self.shots:
            hit = shot.rect.collidelist(alienrects)
            if shot.rect.top <= 0:
                self.shots.remove(shot)
            if hit != -1:
                alien = self.aliens[hit]
                self.explosions.append(Explosion(alien))
                self.shots.remove(shot)
                self.aliens.remove(alien)
                self.aliens.append(Alien())

        for self.actor in [self.player] + self.aliens + self.shots + self.explosions:
            self.actor.update()

        if self.acao_jogador.tipo == AcoesJogador.MOVER:
            self.player.move(self.acao_jogador.parametros)

        elif self.acao_jogador.tipo == AcoesJogador.ATIRAR:
            if not self.player.reloading and len(self.shots) < 3:
                self.shots.append(Shot(self.player))

        else:
            raise TypeError
