import pygame

class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, text="axaxax"):
        super().__init__()
        self.font = pygame.font.Font('jc/assets/gui/minecraft.ttf', 16)
        self.x = x
        self.y = y
        self.visible = True
        self.text = text
        # Create the initial text surface and rect
        self.image = self.font.render(self.text, True, "white", "black")
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def toggle_visibility(self):
        self.visible = not self.visible

    def set_text(self, new_text):
        """Update the text and refresh the image and rect."""
        if new_text != self.text:
            self.text = new_text
            self.image = self.font.render(self.text, True, "white", "black")
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    def update(self, surface):
        """Render the sprite if visible."""
        if self.visible:
            surface.blit(self.image, self.rect)