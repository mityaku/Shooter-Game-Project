from enum import Enum

class GameState(Enum):
    PLAYING = 'playing'
    PAUSED = 'paused'
    GAME_OVER = 'game_over'
