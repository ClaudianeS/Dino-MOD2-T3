import random
import pygame

from dino_runner.components.powerups.shield import Shield


class PowerUpManager:##gerenciador codificador de poder
    def __init__(self):
        self.power_ups = []##evento: contadem de poder
        self.when_appears = 0#quando o poder aparece

    def generate_power_up(self, score):##configuração de aparecer o poder de acordo com a pontuação
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            self.power_ups.append(Shield())

    def update(self, score, game_speed, player):##atalização dos: pontos, velocidade, e do jogador
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.shield = True
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):##proximo passo do poder 
        for power_up in self.power_ups:#quando o poder aumentar
            power_up.draw(screen)##o poder é atualizado na tela

    def reset_power_ups(self):##quando terminar o jogo ate o final o poder será resetado
        self.power_ups = []
        self.when_appears = random.randint(200, 300)