import sys
import time

import unittest

from unittest.mock import patch, MagicMock
from ursina import *

from src.player import Player
from src.state import StateMachine
from src.ui import UIManager

class TestPlayer(unittest.TestCase):
    """
    Unit test class for testing the Player class in a game environment. 
    This class uses unittest framework and mocks external dependencies such as Gun, StateMachine, and UIManager.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up the class-level test fixtures. Mocks Ursina's app to prevent it from creating a window during tests.
        This method is called once before any tests are run.
        """
        with patch('ursina.Ursina'):
            cls.app = MagicMock()

    def setUp(self) -> None:
        """
        Sets up the test environment before each test. Mocks the Gun, StateMachine, and UIManager classes,
        and initializes a Player instance with these mocks.
        """
        # Mock the Gun, StateMachine, and UIManager classes
        with patch('src.player.Gun', MagicMock()):
            with patch('src.state.StateMachine', MagicMock()) as MockStateMachine:
                with patch('src.ui.UIManager', MagicMock()) as MockUIManager:
                    # Create mock instances for StateMachine and UIManager
                    self.mock_state_machine = MockStateMachine()
                    self.mock_ui_manager = MockUIManager()

                    # Instantiate the Player with mocked dependencies
                    self.player = Player(
                        stateMachine=self.mock_state_machine, 
                        uiManager=self.mock_ui_manager, 
                        test=True
                    )

    def test_initial_velocity(self) -> None:
        """
        Tests that the player's initial velocity is set to (0, 0, 0).
        """
        self.assertEqual(self.player.velocity, Vec3(0, 0, 0))

    def test_movement(self) -> None:
        """
        Tests the player's movement logic by applying a velocity and checking if the player's position changes.
        """
        initial_position = self.player.position

        # Apply a velocity to the player
        self.player.velocity = Vec3(5, 0, 0)

        # Manually set time.dt to simulate a time step (simulate 60 FPS)
        time.dt = 1 / 60  

        # Run the game loop for a short time to simulate movement
        for i in range(10):
            self.player.update()
            print(f"Frame {i}: Player Position: {self.player.position}, Velocity: {self.player.velocity}")

        # Check that the player's position has changed
        self.assertNotEqual(self.player.position, initial_position)

if __name__ == '__main__':
    unittest.main()