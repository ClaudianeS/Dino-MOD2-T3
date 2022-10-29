import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):## função de executar o jogo
        self.running = True
        while self.running:
            if not self.playing:##jogando
                self.show_menu()##quando não jogar mais, aparece o menu 

        pygame.display.quit()
        pygame.quit()

    def run(self):#função de correr        
        self.playing = True
        self.obstacle_manager.reset_obstacles()##reseta os obstacolos no final do jogo
        self.power_up_manager.reset_power_ups()##reseta os poderes no final do jogo
        self.game_speed = 20#velocidade adicional do jogo com base nos pontos 
        self.score = 0
        while self.playing:##game loop: events, update, draw
            self.events()
            self.update()
            self.draw()

    def events(self):#loop eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):#loop atualização
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):#loop atualização de pontuação
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5#sempre que a pontuação chegar a 100 aumenta a velocidade em 5

    def draw(self):##loop de proximos passos 
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) 
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):#proximos passos do plano de fundo 
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):#proximo passo da pontuação
         draw_message_component(
            f"Score: {self.score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50
        )   

    def draw_power_up_time(self):#proximos passos laço de aumenta a pontuação aumenta o tempo
        if self.player.has_power_up:#se aumentar a pontuação =>
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:#se o tempo for maior ou igual a 0 =>
                draw_message_component(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:#se qualquer outra coisa =>
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):#lidar com os eventos do menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):#definição de apresentação do menu
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:#iniciar jogo
           draw_message_component("Press any key to start", self.screen)
        else:#se acontecer qualquer outra coisa => reiniciar
            draw_message_component("Press any key to restart", self.screen, pos_y_center=half_screen_height + 140)
            draw_message_component(
                f"Your Score: {self.score}",#ao reiniciar mostrar a pontuação no centro superior da tela
                self.screen,
                pos_y_center=half_screen_height - 150
            )            
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))

        pygame.display.flip()

        self.handle_events_on_menu()