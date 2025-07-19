# UI/camera.py

import pygame

class Camera:
    def __init__(self, width, height, scale=40):
        self.scale = scale
        self.width = width
        self.height = height
        self.origin_x = width // 2
        self.origin_y = height // 2
        self.dragging = False
        self.last_mouse_pos = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self.last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            lx, ly = self.last_mouse_pos
            dx, dy = mx - lx, my - ly

            self.origin_x += dx
            self.origin_y += dy

            self.last_mouse_pos = (mx, my)

        elif event.type == pygame.VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            self.origin_x = self.width // 2
            self.origin_y = self.height // 2

    def get_origin(self):
        return self.origin_x, self.origin_y

    def get_dimensions(self):
        return self.width, self.height
