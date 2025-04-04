"""Asteroids Clone Game"""

import math
import random
import sys

import pygame

from .shop import Shop
from entities.asteroid import Asteroid, FastAsteroid, ZigzagAsteroid, ASTEROID_SIZES
from entities.player import Player
from entities.powerup import PowerUp

POWER_UP_TYPES = ["extra_life", "increased_speed", "shield"]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        pygame.display.set_caption("Asteroids Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.game_over = False
        self.level = 1
        self.player = Player((640, 400), 50, (255, 255, 255))
        self.asteroids = self.create_asteroids(self.level)
        self.power_ups = []
        self.score = 0  # Initialize score

    def spawn_power_up(self):
        position = (random.randint(0, 1280), random.randint(0, 800))
        power_type = random.choice(POWER_UP_TYPES)
        self.power_ups.append(PowerUp(position, power_type))

    def create_asteroids(self, level):
        # Increase number of asteroids as level increases.
        asteroids = []
        num_large = 3 + (level - 1)
        num_fast = 2 + (level // 2)
        num_zigzag = 2 + (level // 2)
        for _ in range(num_large):
            size = random.choice(list(ASTEROID_SIZES.values()))
            velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)) * (
                1 + level * 0.1
            )
            asteroids.append(
                Asteroid(
                    (random.randint(0, 1280), random.randint(0, 800)),
                    size,
                    (255, 0, 0),
                    velocity,
                )
            )

        for _ in range(num_fast):
            size = random.choice(list(ASTEROID_SIZES.values()))
            velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)) * (
                1 + level * 0.1
            )
            asteroids.append(
                FastAsteroid(
                    (random.randint(0, 1280), random.randint(0, 800)),
                    size,
                    (0, 255, 0),
                    velocity,
                )
            )

        for _ in range(num_zigzag):
            size = random.choice(list(ASTEROID_SIZES.values()))
            velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2)) * (
                1 + level * 0.1
            )
            asteroids.append(
                ZigzagAsteroid(
                    (random.randint(0, 1280), random.randint(0, 800)),
                    size,
                    (0, 0, 255),
                    velocity,
                )
            )
        return asteroids

    def open_shop(self):
        shop = Shop(self)
        shop.run()

    def next_level(self):
        self.level += 1
        self.asteroids = self.create_asteroids(self.level)

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(60)

    def display_lives(self):
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {self.player.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.game_over:
            self.display_game_over()
        else:
            self.player.draw(self.screen)
            for asteroid in self.asteroids:
                asteroid.draw(self.screen)
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            self.display_score()  # Display the current score
            self.display_lives()  # Display the player lives
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(
            text, (640 - text.get_width() // 2, 400 - text.get_height() // 2)
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()
                elif event.key == pygame.K_s:
                    self.open_shop()
            elif event.type == pygame.VIDEORESIZE:
                self.resize_screen(event.w, event.h)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def update(self):
        self.player.update()
        for asteroid in self.asteroids:
            asteroid.update()
        self.check_collisions()
        self.check_power_up_collection()
        # Advance to the next level when there are no asteroids left.
        if not self.asteroids:
            self.next_level()

    def check_power_up_collection(self):
        for power_up in self.power_ups[:]:
            if self.is_collision(self.player, power_up):
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)

    def apply_power_up(self, power_up):
        if power_up.power_type == "extra_life":
            self.player.lives += 1
        elif power_up.power_type == "increased_speed":
            self.player.thrust *= 1.5
        elif power_up.power_type == "shield":
            self.player.shield = True
            # Add logic to handle shield duration and effect

    def check_collisions(self):
        # Check collisions between bullets and asteroids.
        for bullet in self.player.bullets[:]:
            for asteroid in self.asteroids[:]:
                if self.is_collision(bullet, asteroid):
                    self.player.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.asteroids.extend(asteroid.split())
                    self.score += 10  # Increase score
                    break

        # Check collisions between the player and asteroids.
        for asteroid in self.asteroids:
            if self.is_collision(self.player, asteroid):
                if not self.player.is_invulnerable():
                    self.player.lives -= 1
                    self.player.last_hit_time = pygame.time.get_ticks()
                    if self.player.lives <= 0:
                        self.game_over = True
                    # Reset the level instead of setting game_over
                    self.asteroids = self.create_asteroids(self.level)
                    # Optionally reset player status (position/velocity)
                    self.player.position = pygame.Vector2(640, 400)
                    self.player.velocity = pygame.Vector2(0, 0)
                break

        # Advance to the next level when there are no asteroids left.
        if not self.asteroids:
            self.level += 1
            self.asteroids = self.create_asteroids(self.level)

    def is_collision(self, obj1, obj2):
        # Compute the distance between the centers.
        distance = math.hypot(
            obj2.position.x - obj1.position.x, obj2.position.y - obj1.position.y
        )

        # Use get_collision_radius if available, otherwise default to half of size.
        radius1 = getattr(obj1, "get_collision_radius", lambda: obj1.size / 2)()
        radius2 = getattr(obj2, "get_collision_radius", lambda: obj2.size / 2)()

        # Fast bounding circle test.
        if distance > (radius1 + radius2):
            return False

        # Prepare offset for precise mask collision check.
        offset = (
            int(obj2.position.x - obj1.position.x),
            int(obj2.position.y - obj1.position.y),
        )
        return obj1.mask.overlap(obj2.mask, offset) is not None

    def quit(self):
        pygame.quit()
        sys.exit()
