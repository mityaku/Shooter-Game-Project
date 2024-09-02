from ursina import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.enums.game_state import GameState
from src.enums.player_state import PlayerState

class StateMachine:
    _instance = None

    def __new__(cls) -> 'StateMachine':
        if cls._instance is None:
            cls._instance = super(StateMachine, cls).__new__(cls)
            cls._instance.init_state_machine()
        return cls._instance

    def init_state_machine(self) -> None:
        self.state: PlayerState = PlayerState.ALIVE
        self.player_health: int = 100
        self.max_health: int = 100
        self.kills: int = 0
        self.game_state: GameState = GameState.PLAYING

    def change_state(self, new_state: PlayerState) -> None:
        if isinstance(new_state, PlayerState):
            self.state = new_state
            print(f"State changed to: {self.state.value}")
        else:
            raise ValueError(f"Invalid state: {new_state}")

    def take_damage(self, amount: int) -> None:
        if self.state != PlayerState.DEAD:
            self.player_health -= amount
            if self.player_health <= 0:
                self.player_health = 0
                self.change_state(PlayerState.DEAD)
                self.game_state = GameState.GAME_OVER
            print(f"Player health: {self.player_health}/{self.max_health}")

    def heal(self, amount: int) -> None:
        if self.state != PlayerState.DEAD:
            self.player_health += amount
            if self.player_health > self.max_health:
                self.player_health = self.max_health
            print(f"Player health: {self.player_health}/{self.max_health}")

    def add_kill(self) -> None:
        self.kills += 1
        print(f"Kills: {self.kills}")

    def pause_game(self) -> None:
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
            print("Game paused.")
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
            print("Game resumed.")

    def reset_game(self) -> None:
        self.state = PlayerState.IDLE
        self.player_health = self.max_health
        self.kills = 0
        self.game_state = GameState.PLAYING
        print("Game reset.")
