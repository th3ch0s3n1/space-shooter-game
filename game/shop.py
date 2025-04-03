"""Shop Module"""

import pygame


class Shop:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 36)
        # Each option includes a label and an upgrade function.
        self.options = [
            ("Increase Thrust", self.upgrade_thrust),
            ("Extra Life", self.extra_life),
            ("Activate Shield", self.activate_shield),
        ]
        self.selected = 0  # current selection index

    def run(self):
        shop_open = True
        while shop_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shop_open = False
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        # Execute the selected upgrade function.
                        self.options[self.selected][1]()
                        shop_open = False

            self.draw()
            pygame.display.flip()
            self.game.clock.tick(60)

    def draw(self):
        # Dim the background.
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Draw shop title.
        title_surf = self.font.render("Upgrade Shop", True, (255, 255, 255))
        self.screen.blit(
            title_surf,
            (self.screen.get_width() // 2 - title_surf.get_width() // 2, 100),
        )

        # Draw each upgrade option.
        start_y = 200
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            option_text = self.font.render(option[0], True, color)
            self.screen.blit(
                option_text,
                (
                    self.screen.get_width() // 2 - option_text.get_width() // 2,
                    start_y + i * 40,
                ),
            )

    def upgrade_thrust(self):
        # Increases the thrust of the player.
        self.game.player.thrust += 0.05

    def extra_life(self):
        # Adds an extra life to the player.
        self.game.player.lives += 1

    def activate_shield(self):
        # Activates the player's shield.
        self.game.player.shield = True
