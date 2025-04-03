"""Player class for a 2D game."""

import math

import pygame

from .bullet import Bullet


class Player:
    """Player class for a 2D game."""

    def __init__(self, position, size, color):
        self.position = pygame.Vector2(position)
        self.size = size
        self.color = color
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0
        self.thrust = 0.1
        self.rotation_speed = 5
        self.slowdown = 0.98
        self.bullets = []
        self.lives = 3  # Initialize player lives
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.update_image()
        self.mask = pygame.mask.from_surface(self.image)
        # Invulnerability period (milliseconds) and last hit time
        self.invulnerability_duration = 2000
        self.last_hit_time = 0

    def is_invulnerable(self):
        """Check if the player is currently invulnerable."""
        return (
            pygame.time.get_ticks() - self.last_hit_time < self.invulnerability_duration
        )

    def get_points(self):
        """Calculate the points of the player's triangle shape."""
        half_size = self.size / 2
        center = self.size / 2
        return [
            (center, center - half_size),
            (center - half_size, center + half_size),
            (center + half_size, center + half_size),
        ]

    def update_image(self):
        """Update the player's image based on its current angle."""
        self.image.fill((0, 0, 0, 0))
        pygame.draw.polygon(self.image, self.color, self.get_points())
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """Draw the player on the screen."""
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_image, new_rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)

    def update(self):
        """Update the player's position and handle input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_UP]:
            self.apply_thrust()
        if keys[pygame.K_DOWN]:
            self.apply_slowdown()

        self.position += self.velocity
        self.wrap_around_screen()

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [
            bullet for bullet in self.bullets if self.is_bullet_on_screen(bullet)
        ]

    def apply_thrust(self):
        """Apply thrust to the player."""
        rad_angle = math.radians(self.angle - 90)
        self.velocity.x += self.thrust * math.cos(rad_angle)
        self.velocity.y += self.thrust * math.sin(rad_angle)

    def apply_slowdown(self):
        """Apply slowdown to the player."""
        self.velocity *= self.slowdown

    def wrap_around_screen(self):
        """Wrap the player around the screen edges."""
        if self.position.x < 0:
            self.position.x = 1280
        elif self.position.x > 1280:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = 800
        elif self.position.y > 800:
            self.position.y = 0

    def get_collision_radius(self):
        """Get the collision radius of the player."""
        return self.size / 2

    def shoot(self):
        """Shoot a bullet from the player's position."""
        rad_angle = math.radians(self.angle - 90)
        bullet_velocity = pygame.Vector2(
            10 * math.cos(rad_angle), 10 * math.sin(rad_angle)
        )
        bullet_offset = pygame.Vector2(
            (self.size / 2) * math.cos(rad_angle), (self.size / 2) * math.sin(rad_angle)
        )
        bullet_position = self.position + bullet_offset
        self.bullets.append(Bullet(bullet_position, bullet_velocity, (255, 255, 255)))

    def is_bullet_on_screen(self, bullet):
        """Check if the bullet is within the screen bounds."""
        return 0 <= bullet.position.x <= 1280 and 0 <= bullet.position.y <= 800
