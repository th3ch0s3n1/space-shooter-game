"""Bullet class for a simple 2D game."""

import pygame


class Bullet:
    """Bullet class for a simple 2D game."""

    def __init__(self, position, velocity, color, size=5):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = color
        self.size = size
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (size, size), size)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Update the bullet's position based on its velocity."""
        self.position += self.velocity

    def draw(self, screen):
        """Draw the bullet on the screen."""
        screen.blit(self.image, self.position - pygame.Vector2(self.size, self.size))

    def get_collision_radius(self):
        """Get the collision radius of the bullet."""
        return self.size
