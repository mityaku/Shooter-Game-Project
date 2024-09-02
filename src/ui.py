from ursina import *
import sys
import os

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import StateMachine

class UIManager:
    """
    Singleton class responsible for managing and updating the game's UI elements,
    such as the health bar, based on the current state of the game.
    """
    _instance = None  # Holds the singleton instance of UIManager

    def __new__(cls, stateMachine: StateMachine) -> 'UIManager':
        """
        Ensures that only one instance of UIManager exists (singleton pattern).
        If an instance doesn't exist, it creates one and initializes it.

        Args:
            stateMachine (StateMachine): The state machine instance that UIManager will observe.

        Returns:
            UIManager: The singleton instance of UIManager.
        """
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance.init_ui_manager(stateMachine)
        return cls._instance

    def init_ui_manager(self, state_machine: 'StateMachine') -> None:
        """
        Initializes the UIManager with the provided StateMachine and sets up the UI elements.

        Args:
            state_machine (StateMachine): The state machine instance to observe and use for updating the UI.
        """
        self.state_machine = state_machine
        health_bar_texture = load_texture('../assets/images/HealthBar.png')

        self.health_bar = Entity(
            parent=camera.ui, 
            model='quad', 
            texture=health_bar_texture, 
            scale=(0.4, 0.03),
            position=(0, -0.45), 
            origin=(0, 0)
        )

        print("UIManager initialized with StateMachine")

    def update(self) -> None:
        """
        Updates the health bar based on the player's current health percentage.
        This method should be called every frame to ensure the UI is up-to-date.
        """
        health_percentage = self.state_machine.player_health / self.state_machine.max_health
        self.health_bar.scale_x = health_percentage * 0.4
        print(f"UIManager: Health bar updated to {health_percentage * 100:.2f}%")
