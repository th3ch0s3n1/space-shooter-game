"""Power-up class for the game."""

import pygame


class PowerUp:
    """Power-up class for the game."""

    def __init__(self, position, power_type):
        self.position = pygame.Vector2(position)
        self.power_type = power_type
        self.size = 20
        self.color = (255, 255, 0)  # Yellow color for power-ups
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image, self.color, (self.size // 2, self.size // 2), self.size // 2
        )
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """Draw the power-up on the screen."""
        screen.blit(
            self.image, self.position - pygame.Vector2(self.size / 2, self.size / 2)
        )

    def update(self):
        """Update the power-up's position."""
        pass  # Power-ups are stationary, so no update logic needed
