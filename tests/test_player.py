import sys
import time
import unittest
from unittest.mock import patch, MagicMock
from ursina import *
from src.player import Player
from src.state import StateMachine
from src.ui import UIManager
from src.enums.game_state import GameState

class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from ursina import Ursina
        cls.app = Ursina()
        cls.app.development_mode = False

    def setUp(self) -> None:
        with patch('src.player.Gun', MagicMock()):
            with patch('src.state.StateMachine', MagicMock()) as MockStateMachine:
                with patch('src.ui.UIManager', MagicMock()) as MockUIManager:
                    self.mock_state_machine = MockStateMachine()
                    self.mock_ui_manager = MockUIManager()

                    self.mock_state_machine.player_health = 100
                    self.mock_state_machine.game_state = GameState.PLAYING

                    self.player = Player(
                        stateMachine=self.mock_state_machine, 
                        uiManager=self.mock_ui_manager, 
                        test=True
                    )

        from ursina import mouse, held_keys
        mouse.velocity = Vec2(0, 0)
        held_keys['left mouse'] = False

    def test_initial_velocity(self) -> None:
        self.assertEqual(self.player.velocity, Vec3(0, 0, 0))

    def test_movement(self) -> None:
        initial_position = self.player.position

        self.player.velocity = Vec3(5, 0, 0)

        time.dt = 1 / 60  

        for i in range(10):
            self.player.update()
            print(f"Frame {i}: Player Position: {self.player.position}, Velocity: {self.player.velocity}")

        self.assertNotEqual(self.player.position, initial_position)

if __name__ == '__main__':
    unittest.main()
