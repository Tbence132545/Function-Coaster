import pygame 
from UI.draw_utils import Ball, FinishPoint,StartButton, draw_coordinate_system,draw_function,draw_list
from game.functions import parse_function
from UI.input_box import TextBox

def check_finish_collision(ball, finish_point, finish_radius, scale):
    dx = ball.coord[0] - finish_point.coord[0]
    dy = ball.coord[1] - finish_point.coord[1]
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance <= (ball.radius + finish_radius) / scale:
        return True
    return False    

class Game:
    def __init__(self, screen, camera, HEIGHT,WIDTH):
        self.screen = screen
        self.camera = camera
        self.font = pygame.font.SysFont(None, 30)
        self.large_font = pygame.font.SysFont(None, 72)
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.reset()

    def reset(self):
        self.functions = []
        self.buttons = []
        self.user_function = None
        self.ball = Ball()
        self.finish_point = FinishPoint()
        self.ball_start_coord = self.ball.coord
        self.started = False
        self.won = False
        self.start_button = StartButton("Start", self.WIDTH - 100, 10, self.font)
        self.start_button.bg_color = (144, 238, 144)  # green

    def start_game(self):
        self.started = True
        self.won = False
        self.start_button.text = "Restart"
        self.start_button.bg_color = (255, 204, 203)  # pink

    def restart_game(self):
        self.started = False
        self.won = False
        self.start_button.text = "Start"
        self.start_button.bg_color = (144, 238, 144)  # green
        self.ball.coord = self.ball_start_coord
        self.ball.vx = 0
        self.ball.vy = 0

    def player_won(self):
        self.started = False
        self.won = True
        self.start_button.text = "New Game"
        self.start_button.bg_color = (203, 195, 227)  # purple

    def update(self, origin_x, origin_y):
        if self.started and not self.won:
            parsed_functions = []
            for expr in self.functions:
                f, interval = parse_function(expr)
                if f is not None:
                    parsed_functions.append((f, interval))

            self.ball.update(parsed_functions, origin_x, origin_y, self.camera.scale)

            if check_finish_collision(self.ball, self.finish_point, self.finish_point.radius, self.camera.scale):
                self.player_won()

    def draw(self, origin_x, origin_y, width, height, textbox):
        self.screen.fill((255, 255, 255))
        draw_coordinate_system(self.screen, width, height, origin_x, origin_y, self.camera.scale)
        textbox.draw(self.screen, width, height)
        for i, expr in enumerate(self.functions):
            f,interval = parse_function(expr)
            if f is not None:
                draw_function(self.screen, f,interval, origin_x, origin_y, self.camera.scale, width, height, i)
        if self.functions:
            self.buttons = draw_list(self.screen, self.functions)
        else:
            self.buttons = []

        self.start_button.draw(self.screen, width, height)
        self.finish_point.draw(self.screen, origin_x, origin_y, self.camera.scale)
        self.ball.draw(self.screen, origin_x, origin_y, self.camera.scale)

        if self.won:
            text_surface = self.large_font.render("You Won!", True, (0, 128, 0))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            self.screen.blit(text_surface, text_rect)