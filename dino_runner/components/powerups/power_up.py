import random
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class PowerUp(Sprite):
    def __init__(self, image, type):##iniciar eventos que é aparecer as imagens na tela
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.rect.y = random.randint(125, 175)

        self.start_time = 0##iniciar a contagem do tempo
        self.duration = random.randint(5, 10)

    def update(self, game_speed, power_ups):##atualização da velocidade do jogo e do poder do jogador
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            power_ups.pop()

    def draw(self, screen):##poximo passo do jogo (resedenha o proximo passo do jogo)
        screen.blit(self.image, self.rect)