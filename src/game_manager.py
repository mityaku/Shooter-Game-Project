from ursina import *
import sys
import os

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import StateMachine
from src.enums.game_state import GameState
from enemy import Enemy
from player import Player
from ui import UIManager

class GameManager(Entity):
    """
    The GameManager class handles the overall game logic, including spawning enemies,
    tracking waves, handling player death, and restarting the game.
    """

    def __init__(self, state_machine: StateMachine, ui_manager: UIManager, **kwargs):
        super().__init__(**kwargs)
        self.state_machine = state_machine
        self.ui_manager = ui_manager

        # Game variables
        self.current_wave = 1
        self.enemies_remaining = 0
        self.player = None

        # List to keep track of enemies
        self.enemies = []

    def start_game(self):
        """
        Starts the game by initializing the player and starting the first wave.
        """
        # Create the player
        self.player = Player(stateMachine=self.state_machine, uiManager=self.ui_manager, position=(0, 1.5, 0))
        self.state_machine.player_health = self.state_machine.max_health  # Reset player health

        # Start the first wave
        self.current_wave = 1
        self.spawn_wave()

    def spawn_wave(self):
        """
        Spawns a new wave of enemies based on the current wave number.
        """
        print(f"Spawning wave {self.current_wave} with {self.current_wave} enemies.")
        self.enemies_remaining = self.current_wave
        self.enemies = []

        for i in range(self.current_wave):
            # Position enemies around the player
            position = Vec3(random.uniform(-10, 10), 2, random.uniform(-10, 10))
            enemy = Enemy(player=self.player, game_manager=self, position=position)
            self.enemies.append(enemy)

    def enemy_died(self):
        """
        Called when an enemy dies. Checks if the wave is complete and spawns the next wave.
        """
        self.enemies_remaining -= 1
        self.state_machine.kills += 1  # Increase kill count

        if self.enemies_remaining <= 0:
            # All enemies in the wave are dead; start the next wave
            self.current_wave += 1
            self.spawn_wave()

    def player_died(self):
        """
        Called when the player dies. Displays the end screen.
        """
        print("Player died!")
        self.state_machine.game_state = GameState.GAME_OVER
        self.ui_manager.show_end_screen(self.state_machine.kills)

    def restart_game(self):
        """
        Restarts the game from wave 1.
        """
        # Destroy existing enemies and player
        for enemy in self.enemies:
            destroy(enemy)
        self.enemies = []
        if self.player:
            destroy(self.player)
            self.player = None

        # Reset game variables
        self.state_machine.kills = 0
        self.current_wave = 1
        self.state_machine.game_state = GameState.PLAYING
        self.ui_manager.hide_end_screen()

        # Start the game
        self.start_game()
