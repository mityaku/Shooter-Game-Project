import sys
import time

import unittest

from unittest.mock import patch, MagicMock
from ursina import *

from src.player import Player
from src.state import StateMachine
from src.ui import UIManager

class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock Ursina's app to prevent it from trying to create a window
        with patch('ursina.Ursina'):
            cls.app = MagicMock()

    def setUp(self):
        # Mock the Gun, StateMachine, and UIManager classes
        with patch('src.player.Gun', MagicMock()):
            with patch('src.state.StateMachine', MagicMock()) as MockStateMachine:
                with patch('src.ui.UIManager', MagicMock()) as MockUIManager:
                    # Create a mock instance for StateMachine and UIManager
                    self.mock_state_machine = MockStateMachine()
                    self.mock_ui_manager = MockUIManager()

                    # Instantiate the Player with mocked StateMachine and UIManager
                    self.player = Player(stateMachine=self.mock_state_machine, uiManager=self.mock_ui_manager, test=True)


    def test_initial_velocity(self):
        self.assertEqual(self.player.velocity, Vec3(0, 0, 0))

    def test_movement(self):
        initial_position = self.player.position

        # Apply a velocity to the player
        self.player.velocity = Vec3(5, 0, 0)

        # Manually set time.dt to simulate a time step
        time.dt = 1/60  # Simulate 60 FPS

        # Run the game loop for a short time to simulate movement
        for i in range(10):
            self.player.update()
            print(f"Frame {i}: Player Position: {self.player.position}, Velocity: {self.player.velocity}")

        # Check that the player's position has changed
        self.assertNotEqual(self.player.position, initial_position)

if __name__ == '__main__':
    unittest.main()
