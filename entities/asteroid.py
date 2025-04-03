"""Asteroid class for a space game."""

import random

import pygame

ASTEROID_SIZES = {"XS": 20, "SM": 40, "MD": 60, "LG": 80}


class Asteroid:
    """Asteroid class for a space game."""

    def __init__(self, position, size, color, velocity):
        self.position = pygame.Vector2(position)
        self.size = size
        self.color = color
        self.velocity = velocity
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (size // 2, size // 2), size // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """Draw the asteroid on the screen."""
        screen.blit(
            self.image, self.position - pygame.Vector2(self.size / 2, self.size / 2)
        )

    def update(self):
        """Update the asteroid's position based on its velocity."""
        self.position += self.velocity
        if self.position.x < 0 or self.position.x > 1280:
            self.velocity.x = -self.velocity.x
        if self.position.y < 0 or self.position.y > 800:
            self.velocity.y = -self.velocity.y

    def get_collision_radius(self):
        """Get the collision radius of the asteroid."""
        return self.size / 2

    def split(self):
        """Split the asteroid into smaller ones."""
        if self.size == ASTEROID_SIZES["XS"]:
            return []
        if self.size == ASTEROID_SIZES["SM"]:
            new_size = ASTEROID_SIZES["XS"]
        elif self.size == ASTEROID_SIZES["MD"]:
            new_size = ASTEROID_SIZES["SM"]
        elif self.size == ASTEROID_SIZES["LG"]:
            new_size = ASTEROID_SIZES["MD"]
        else:
            return []

        new_velocity1 = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        new_velocity2 = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))

        return [
            Asteroid(self.position, new_size, self.color, new_velocity1),
            Asteroid(self.position, new_size, self.color, new_velocity2),
        ]


class FastAsteroid(Asteroid):
    """FastAsteroid class for a space game."""

    def __init__(self, position, size, color, velocity):
        super().__init__(position, size, color, velocity)
        self.velocity *= 2  # Double the speed


class ZigzagAsteroid(Asteroid):
    """ZigzagAsteroid class for a space game."""

    def __init__(self, position, size, color, velocity):
        super().__init__(position, size, color, velocity)
        self.zigzag_direction = 1

    def update(self):
        """Update the asteroid's position with zigzag movement."""
        self.position += self.velocity
        self.velocity.x += self.zigzag_direction * 0.1
        if abs(self.velocity.x) > 2:
            self.zigzag_direction *= -1
        if self.position.x < 0 or self.position.x > 1280:
            self.velocity.x = -self.velocity.x
        if self.position.y < 0 or self.position.y > 800:
            self.velocity.y = -self.velocity.y
