from ursina import *
import sys
import os

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import StateMachine
from src.enums.game_state import GameState

class UIManager(Entity):
    """
    Manages and updates the game's UI elements based on the current state of the game.
    Inherits from Entity to utilize the update method and parent UI elements properly.
    """

    def __init__(self, state_machine: StateMachine, start_game_callback=None, restart_game_callback=None) -> None:
        """
        Initializes the UIManager with the provided StateMachine and sets up the UI elements.

        Args:
            state_machine (StateMachine): The state machine instance to observe and use for updating the UI.
            start_game_callback (function): Callback function to start the game.
            restart_game_callback (function): Callback function to restart the game.
        """
        super().__init__(parent=camera.ui)
        self.state_machine = state_machine
        self.start_game_callback = start_game_callback
        self.restart_game_callback = restart_game_callback

        # Initialize HUD elements but make them invisible initially
        self.init_hud_elements()
        # Initialize Start Screen elements
        self.init_start_screen()
        # Initialize Game Over Screen elements
        self.init_game_over_screen()

        print("UIManager initialized with StateMachine")

    def init_hud_elements(self):
        """
        Initializes the HUD elements (health bar, skull icon, kill count text).
        """
        health_bar_texture = load_texture('../assets/images/HealthBar.png')

        self.health_bar = Entity(
            parent=self,
            model='quad',
            texture=health_bar_texture,
            scale=(0.4, 0.03),
            position=(0, -0.45),
            origin=(0, 0),
            visible=False  # Start as not visible
        )

        skull_icon_texture = load_texture('../assets/images/Kills.png')
        self.skull_icon = Entity(
            parent=self,
            model='quad',
            texture=skull_icon_texture,
            scale=(0.04, 0.05),
            position=(-0.05, -0.39),
            origin=(0, 0),
            visible=False  # Start as not visible
        )

        # Create the kill count text entity
        self.kill_count_text = Text(
            text=f'{self.state_machine.kills}',
            font='../assets/fonts/primary.ttf',
            parent=self,
            scale=1,
            position=(0, -0.39),
            origin=(0, 0),
            color=color.rgb(0.6, 0.6, 0.6),  # Darker gray color
            visible=False  # Start as not visible
        )

    def init_start_screen(self):
        """
        Initializes the start screen elements (background, title, play button).
        """
        self.start_screen = Entity(parent=self)

        # Background
        self.background = Entity(
            parent=self.start_screen,
            model='quad',
            texture='white_cube',
            color=color.light_gray,
            scale=(window.aspect_ratio * 2, 2),
            z=1
        )

        # Game Title
        self.title = Text(
            font='../assets/fonts/primary.ttf',
            text='Shooter Game',
            parent=self.start_screen,
            origin=(0, 0),
            scale=2,
            y=0.2,
            color=color.dark_gray
        )

        # Play Button
        self.play_button = Button(
            font='../assets/fonts/primary.ttf',
            text='Play',
            parent=self.start_screen,
            scale=(0.2, 0.1),
            y=-0.1,
            color=color.red,
            on_click=self.start_game
        )

    def init_game_over_screen(self):
        """
        Initializes the game over screen elements.
        """
        self.game_over_screen = Entity(parent=self)
        self.game_over_screen.disable()  # Start as disabled

        # Background
        self.game_over_background = Entity(
            parent=self.game_over_screen,
            model='quad',
            texture='white_cube',
            color=color.light_gray,
            scale=(window.aspect_ratio * 2, 2),
            z=1
        )

        # Game Over Text
        self.game_over_text = Text(
            font='../assets/fonts/primary.ttf',
            text='Game Over',
            parent=self.game_over_screen,
            origin=(0, 0),
            scale=2,
            y=0.2,
            color=color.red
        )

        # Player Kills
        self.kills_text = Text(
            font='../assets/fonts/primary.ttf',
            text='Kills: 0',
            parent=self.game_over_screen,
            origin=(0, 0),
            scale=1.5,
            y=0.0,
            color=color.dark_gray
        )

        # Play Again Button
        self.play_again_button = Button(
            font='../assets/fonts/primary.ttf',
            text='Play Again',
            parent=self.game_over_screen,
            scale=(0.3, 0.1),
            y=-0.2,
            color=color.dark_gray,
            on_click=self.restart_game
        )

    def start_game(self):
        """
        Callback function to start the game when the play button is clicked.
        """
        # Disable the start screen
        self.start_screen.disable()
        # Hide the game over screen if it's visible
        self.game_over_screen.disable()
        # Change the game state to PLAYING
        self.state_machine.game_state = GameState.PLAYING
        # Make HUD elements visible
        self.health_bar.visible = True
        self.skull_icon.visible = True
        self.kill_count_text.visible = True

        # Call the start_game_callback to initialize game entities
        if self.start_game_callback:
            self.start_game_callback()

    def show_game_over_screen(self, player_kills):
        """
        Displays the game over screen with the player's kills.

        Args:
            player_kills (int): The number of kills the player achieved.
        """
        # Update the kills text
        self.kills_text.text = f'Kills: {player_kills}'
        # Enable the game over screen
        self.game_over_screen.enable()
        # Hide HUD elements
        self.health_bar.visible = False
        self.skull_icon.visible = False
        self.kill_count_text.visible = False

    def restart_game(self):
        """
        Handles restarting the game.
        """
        # Disable the game over screen
        self.game_over_screen.disable()
        # Reset the state machine
        self.state_machine.game_state = GameState.MENU
        # Call the restart callback
        if self.restart_game_callback:
            self.restart_game_callback()

    def update(self) -> None:
        """
        Updates the UI based on the current game state.
        This method is called every frame.
        """
        if self.state_machine.game_state == GameState.MENU:
            # Show start screen, hide HUD and game over screen
            self.start_screen.enable()
            self.game_over_screen.disable()
            self.health_bar.visible = False
            self.skull_icon.visible = False
            self.kill_count_text.visible = False
        elif self.state_machine.game_state == GameState.GAME_OVER:
            # Show game over screen, hide HUD
            self.start_screen.disable()
            self.game_over_screen.enable()
            self.health_bar.visible = False
            self.skull_icon.visible = False
            self.kill_count_text.visible = False
            self.kills_text.text = f'Kills: {self.state_machine.kills}'
        else:
            # Hide start and game over screens, show HUD
            self.start_screen.disable()
            self.game_over_screen.disable()
            self.health_bar.visible = True
            self.skull_icon.visible = True
            self.kill_count_text.visible = True

            # Update HUD elements
            health_percentage = self.state_machine.player_health / self.state_machine.max_health
            self.health_bar.scale_x = health_percentage * 0.4

            self.kill_count_text.text = f'Kills: {self.state_machine.kills}'
