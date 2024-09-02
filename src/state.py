from ursina import *
import sys
import os

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.enums.game_state import GameState
from src.enums.player_state import PlayerState

class StateMachine:
    """
    Singleton class that manages the game's state, including the player's health,
    kills, and the overall game state. It ensures that only one instance of 
    StateMachine exists and provides methods to modify the game state.
    """
    _instance = None  # Holds the singleton instance of StateMachine

    def __new__(cls) -> 'StateMachine':
        """
        Ensures that only one instance of StateMachine exists (singleton pattern).
        If an instance doesn't exist, it creates one and initializes it.

        Returns:
            StateMachine: The singleton instance of StateMachine.
        """
        if cls._instance is None:
            cls._instance = super(StateMachine, cls).__new__(cls)
            cls._instance.init_state_machine()
        return cls._instance

    def init_state_machine(self) -> None:
        """
        Initializes the StateMachine with default values for the player's state, health,
        kills, and the overall game state.
        """
        self.state: PlayerState = PlayerState.ALIVE
        self.player_health: int = 100
        self.max_health: int = 100
        self.kills: int = 0
        self.game_state: GameState = GameState.PLAYING

    def change_state(self, new_state: PlayerState) -> None:
        """
        Changes the player's state to the provided new state if it is valid.

        Args:
            new_state (PlayerState): The new state to change to.

        Raises:
            ValueError: If the provided new_state is not a valid PlayerState.
        """
        if isinstance(new_state, PlayerState):
            self.state = new_state
            print(f"State changed to: {self.state.value}")
        else:
            raise ValueError(f"Invalid state: {new_state}")

    def take_damage(self, amount: int) -> None:
        """
        Reduces the player's health by the specified amount. If health drops to 0 or below,
        the player's state changes to DEAD, and the game state changes to GAME_OVER.

        Args:
            amount (int): The amount of damage to apply to the player.
        """
        if self.state != PlayerState.DEAD:
            self.player_health -= amount
            if self.player_health <= 0:
                self.player_health = 0
                self.change_state(PlayerState.DEAD)
                self.game_state = GameState.GAME_OVER
            print(f"Player health: {self.player_health}/{self.max_health}")

    def heal(self, amount: int) -> None:
        """
        Increases the player's health by the specified amount, up to the maximum health.
        Does nothing if the player's state is DEAD.

        Args:
            amount (int): The amount of health to restore.
        """
        if self.state != PlayerState.DEAD:
            self.player_health += amount
            if self.player_health > self.max_health:
                self.player_health = self.max_health
            print(f"Player health: {self.player_health}/{self.max_health}")

    def add_kill(self) -> None:
        """
        Increments the player's kill count by one.
        """
        self.kills += 1
        print(f"Kills: {self.kills}")

    def pause_game(self) -> None:
        """
        Toggles the game state between PLAYING and PAUSED.
        """
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
            print("Game paused.")
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
            print("Game resumed.")

    def reset_game(self) -> None:
        """
        Resets the game to its initial state, setting the player's state to IDLE,
        restoring health to maximum, resetting the kill count, and setting the 
        game state to PLAYING.
        """
        self.state = PlayerState.IDLE
        self.player_health = self.max_health
        self.kills = 0
        self.game_state = GameState.PLAYING
        print("Game reset.")
