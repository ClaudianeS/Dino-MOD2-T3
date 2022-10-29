import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:##gerenciador codificador de obstaculos
    def __init__(self):##evento: obstaculos
        self.obstacles = []

    def update(self, game):##atualização do jogo (tipo de obstaculos)
        obstacle_type = [
            Cactus(),
            Bird(),
        ]

        if len(self.obstacles) == 0:#laço de aparecer os obstaculos            
            self.obstacles.append(obstacle_type[random.randint(0,1)])
            
        for obstacle in self.obstacles:#laço de obstaculos depois de obstaculos
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):#se o jogador colidir com o obstaculos ele morre
                if not game.player.has_power_up:##ele não ganha ponto
                    pygame.time.delay(500)#o tempo dele atrasa
                    game.playing = False#ele não joga mais
                    game.death_count += 1#ele perde uma vida
                    break#para o jodo
                else:
                    self.obstacles.remove(obstacle)#se for qualquer outra coisa o obstaculo é removido

    def reset_obstacles(self):##resetar obstaculos no final do jogo
        self.obstacles = []

    def draw(self, screen):###proximo obstaculo
        for obstacle in self.obstacles:
            obstacle.draw(screen)                             