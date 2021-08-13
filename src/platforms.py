import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, path, scale=1):
        super().__init__()
        self.image = pygame.image.load(path)

        self.rect = self.image.get_rect()
        newSize = []
        x, y = self.rect.size
        newSize.append(int(x * scale))
        newSize.append(int(y * scale))
        self.image = pygame.transform.scale(self.image, newSize)
        self.rect = self.image.get_rect()
