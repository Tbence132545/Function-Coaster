import pygame
import numpy as np
import sympy 
import random
from game.functions import parse_function

LOGICAL_X_MIN, LOGICAL_X_MAX = -15,15
LOGICAL_Y_MIN, LOGICAL_Y_MAX = -15,15
BG_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
AXIS_COLOR = (200, 200, 200)
TEXT_COLOR = (200, 200, 200)
colors = [
    (255, 0, 0),     
    (0, 255, 0),     
    (0, 0, 255),     
    (255, 255, 0),   
    (255, 0, 255),   
    (0, 255, 255),   
    (255, 128, 0),   
    (128, 0, 255),   
    (0, 128, 128),   
    (128, 128, 128)  
]
class FinishPoint:
    def __init__(self):
        self.coord = (
            random.randint(LOGICAL_X_MIN, LOGICAL_X_MAX),
            random.randint(LOGICAL_Y_MIN, LOGICAL_Y_MAX)
        )
        self.color = (144, 238, 144)  # light green
        self.radius = 14
    @staticmethod
    def coord_to_pixel(coord, origin_x, origin_y, scale):
        x_pixel = origin_x + coord[0] * scale
        y_pixel = origin_y - coord[1] * scale
        return int(x_pixel), int(y_pixel)

    def draw(self, screen, origin_x, origin_y, scale):
        pixel_pos = self.coord_to_pixel(self.coord, origin_x, origin_y, scale)
        pygame.draw.circle(screen, self.color, pixel_pos, self.radius)

def numerical_derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

class Ball:
    def __init__(self):
        self.coord = (
            random.randint(LOGICAL_X_MIN, LOGICAL_X_MAX),
            random.randint(LOGICAL_Y_MAX, LOGICAL_Y_MAX+10)
        )
        self.color = (255, 0, 0)  # red
        self.radius = 8
        self.vx = 0.0
        self.vy = 0.0
        self.gravity = 0.05  # tweak for your scale

    @staticmethod
    def coord_to_pixel(coord, origin_x, origin_y, scale):
        x_pixel = origin_x + coord[0] * scale
        y_pixel = origin_y - coord[1] * scale
        return int(x_pixel), int(y_pixel)

    def draw(self, screen, origin_x, origin_y, scale):
        pixel_pos = self.coord_to_pixel(self.coord, origin_x, origin_y, scale)
        pygame.draw.circle(screen, self.color, pixel_pos, self.radius)

    def update(self, functions, origin_x, origin_y, scale):
        # Apply gravity downward
        self.vy -= self.gravity

        new_x = self.coord[0] + self.vx
        new_y = self.coord[1] + self.vy

        for expr in functions:
            f = parse_function(expr)
            if f is None:
                continue
            try:
                y_on_func = f(new_x)
                if not np.isfinite(y_on_func):
                    continue
                # Check collision: ball bottom touching function y
                # We approximate ball bottom as coord y - radius in logical units
                ball_bottom_y = new_y - self.radius / scale

                # If ball would go below the function surface
                if ball_bottom_y <= y_on_func:
                    # Snap ball on surface
                    new_y = y_on_func + self.radius / scale

                    # Calculate slope of function at new_x
                    slope = numerical_derivative(f, new_x)

                    # Calculate angle of slope
                    angle = np.arctan(slope)

                    # Gravity vector components along slope
                    gravity_along_slope = -self.gravity * np.sin(angle)  # Note the minus here!

                    self.vx += gravity_along_slope * np.cos(angle)
                    self.vy = gravity_along_slope * np.sin(angle)
                    # Optional: add friction to slow sliding a bit
                    friction = 0.02
                    self.vx *= (1 - friction)
                    self.vy *= (1 - friction)

                    break  # Only consider first collision function

            except Exception:
                pass

        self.coord = (new_x, new_y)
 


class StartButton:
    def __init__(self, text, x, y, font, padding=10, bg_color=(144, 238, 144), text_color=(255,255,255)):
        self.text = text
        self.font = font
        self.padding = padding
        self.bg_color = bg_color
        self.text_color = text_color
        
        self.text_surface = font.render(text, True, text_color)
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = (x, y)
        self.rect.inflate_ip(padding*2, padding*2)

    def draw(self, screen, screen_width, screen_height):
        # Update position to top-right corner with padding
        self.rect.topright = (screen_width - self.padding, self.padding)
        
        # Draw button background
        pygame.draw.rect(screen, self.bg_color, self.rect.inflate(20, 10))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        # Draw text on top (centered inside background)
        text_pos = self.rect.center
        screen.blit(self.text_surface, self.text_surface.get_rect(center=text_pos))

    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class XButton:
    def __init__(self, x, y, size=16):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 0, 0) 
        self.size = size

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.rect.topleft, self.rect.bottomright, 2)
        pygame.draw.line(screen, self.color, self.rect.bottomleft, self.rect.topright, 2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_coordinate_system(screen, width, height, origin_x, origin_y, scale):
    font = pygame.font.SysFont(None, 20)
    screen.fill(BG_COLOR)

    start_y = origin_y % scale
    for y in range(start_y, height, scale):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (width, y))
        coord = (origin_y - y) // scale
        if coord != 0:
            label = font.render(str(coord), True, TEXT_COLOR)
            screen.blit(label, (origin_x + 4, y))

    start_x = origin_x % scale
    for x in range(start_x, width, scale):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height))
        coord = (x - origin_x) // scale
        if coord != 0:
            label = font.render(str(coord), True, TEXT_COLOR)
            screen.blit(label, (x + 2, origin_y + 4))

    pygame.draw.line(screen, AXIS_COLOR, (0, origin_y), (width, origin_y), 2)
    pygame.draw.line(screen, AXIS_COLOR, (origin_x, 0), (origin_x, height), 2)

def draw_function(screen, f, origin_x, origin_y, scale, width, height, color_index=0):
    if f is None:
        return

    color = colors[color_index % len(colors)]

    xs = np.linspace(0.01, width, num=width) 
    xs_coord = (xs - origin_x) / scale

    with np.errstate(invalid='ignore', divide='ignore'):
        ys = f(xs_coord)
        if isinstance(ys, (int, float, np.number)):
            ys = np.full_like(xs_coord, ys, dtype=float)
    points = []
    for x_pixel, y in zip(xs, ys):
        if np.isfinite(y) and np.isreal(y):
            y_val = np.real(y)
            y_pixel = origin_y - y_val * scale
            if 0 <= y_pixel <= height:
                points.append((int(x_pixel), int(y_pixel)))

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, 2)


def draw_list(screen, items, x=10, y=10, line_spacing=5):
    font = pygame.font.SysFont(None, 24)
    x_button_size = 16
    x_button_padding = 5

    buttons = []

    for item in items:
        text_surface = font.render(str(item), True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

        text_width = text_surface.get_width()
        x_pos = x + text_width + x_button_padding
        y_pos = y + (text_surface.get_height() - x_button_size) // 2

        btn = XButton(x_pos, y_pos, x_button_size)
        btn.draw(screen)
        buttons.append(btn)

        y += text_surface.get_height() + line_spacing

    return buttons