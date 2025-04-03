from game.game import Game


def main():
    game = Game()
    while game.running:
        game.spawn_power_up()
        game.run()
    game.quit()


if __name__ == "__main__":
    main()
