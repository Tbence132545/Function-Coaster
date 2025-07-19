# main.py

import pygame
import sys
from UI.input_box import TextBox
from UI.draw_utils import draw_coordinate_system, draw_function,draw_list,StartButton,FinishPoint,Ball
from game.functions import parse_function
from UI.camera import Camera
import random
from game.game import Game
pygame.init()

WIDTH, HEIGHT = 800, 600


def main():
    global screen, camera, textbox

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Function Coaster")
    camera = Camera(WIDTH, HEIGHT)
    textbox = TextBox(WIDTH, HEIGHT)

    game = Game(screen, camera,WIDTH,HEIGHT)

    clock = pygame.time.Clock()
    running = True
    while running:
        origin_x, origin_y = camera.get_origin()
        width, height = camera.get_dimensions()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            textbox.handle_event(event)
            camera.handle_event(event)

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if game.start_button.is_clicked(pos):
                    if game.won:
                        game.reset()
                    else:
                        if not game.started:
                            game.start_game()
                        else:
                            game.restart_game()
                else:
                    
                    for i, btn in enumerate(game.buttons):
                        if btn.is_clicked(pos):
                            print(f"Removing function: {game.functions[i]}")
                            game.functions.pop(i)
                            break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    expr = textbox.text
                    try:
                        game.user_function = parse_function(expr)
                        game.functions.append(expr)
                        textbox.text = ""
                    except Exception as e:
                        print("Error parsing the expression:", e)
                if event.key == pygame.K_r:
                    game.reset()

        game.update(origin_x, origin_y)
        game.draw(origin_x, origin_y, width, height,textbox=textbox)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

