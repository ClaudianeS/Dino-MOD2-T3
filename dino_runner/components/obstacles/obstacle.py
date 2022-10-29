import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, type):###iniciar eventos que é aparecer as imagens na tela
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):###atualiza o jogo
        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:##loop do obstáculo
            obstacles.pop()

    def draw(self, screen):##proximo passo do jogo (redesenhar o jogo com o proximo passo) 
        screen.blit(self.image[self.type], (self.rect.x, self.rect.y))