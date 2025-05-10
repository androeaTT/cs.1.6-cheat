import pygame

class EspBorder(pygame.sprite.Sprite):
    def __init__(self, x, y, distance, color=(255, 0, 0)):
        super().__init__()
        sized = distance / 2000
        width = 9 / sized
        height = 18 / sized
        x = x - width / 2
        y = y - height / 2
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height), 1)
        self.rect = self.image.get_rect(topleft=(x, y))
    
