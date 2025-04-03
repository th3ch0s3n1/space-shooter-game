# Space Shooter Game

This is a 2D space shooter game developed in Python using Pygame. The project features a player ship with movement and shooting, various types of asteroids, an AI enemy, and an upgrade shop GUI.

## Project Overview

- **Player**: Navigates, shoots bullets, and collects upgrades.
- **Asteroids**: Includes normal, fast, and zigzag variants. Larger asteroids split into smaller ones.
- **Upgrade Shop**: Pauses the game to display upgrade options.
- **Utilities & Assets**: Common helper functions and game assets (images, sounds, fonts) are organized in separate directories.

## Project Structure

```bash
   ├── main.py
   ├── game/
   │   ├── __init__.py
   │   ├── game.py         # Contains the Game class and related game loop logic.
   │   ├── shop.py         # Contains the Shop class.
   ├── entities/
   │   ├── __init__.py
   │   ├── player.py       # Contains the Player class.
   │   ├── asteroid.py     # Contains Asteroid, FastAsteroid, ZigzagAsteroid classes.
   │   ├── bullet.py       # Contains the Bullet class.
   │   └── powerup.py      # Contains the PowerUp class.
   ├── utils/
   │   ├── __init__.py
   │   └── helpers.py      # Contains common utility functions.
   └── README.md
```

## Requirements

- Python 3.x
- Pygame

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv

2. Activate the virtual environment (on Windows):
    ```bash
    .venv\Scripts\activate

3. Install the required packages:
    ```bash
    pip install pygame

## Running the Game

Execute the following command in your terminal:
```bash
 python main.py
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
