import pygame

class TextBox:
    def __init__(self, width, height):
        self.rect = pygame.Rect(20, height - 50, width - 40, 30)
        self.color = pygame.Color('white')
        self.text = ''
        self.font = pygame.font.SysFont(None, 28)
        self.active = False
        self.prefix = "f(x) := "

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return 'ENTER'
            elif event.key == pygame.K_BACKSPACE:
                self.text = ''
                return 'BACKSPACE'
            else:
                self.text += event.unicode
        return None 
    def draw(self, screen, width, height):
        self.rect.width = width - 40
        self.rect.y = height - 50

        pygame.draw.rect(screen, self.color, self.rect, 2)

        txt_surface = self.font.render(self.prefix + self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
