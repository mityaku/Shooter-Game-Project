import unittest
from unittest.mock import patch, MagicMock
import time  # Standard library time
from ursina import Vec3, camera
from ursina import time as ursina_time
from ursina import Ursina

class TestGun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Ursina(headless=True)  # Initialize Ursina

    def setUp(self):
        # Initialize camera attributes
        camera.position = Vec3(0, 0, 0)
        camera.rotation = Vec3(0, 0, 0)

        # Simulate time
        ursina_time.dt = 1 / 60  # Simulate 60 FPS

        # Mock time.time() to control time progression
        self.original_time_time = time.time
        time.time = MagicMock(return_value=1000)

    def tearDown(self):
        # Restore original time.time
        time.time = self.original_time_time

    @patch('src.gun.Bullet')
    @patch('ursina.mesh_importer.load_model', return_value=MagicMock())
    @patch('ursina.texture_importer.load_texture', return_value=MagicMock())
    def test_shooting_cooldown(self, mock_load_texture, mock_load_model, mock_bullet_class):
        # Import Gun within the test method after patches are applied
        from src.gun import Gun

        # Initialize the Gun object
        self.gun = Gun()

        # First shot should succeed
        self.gun.shoot()
        self.assertEqual(self.gun.last_shot_time, 1000)
        self.assertEqual(mock_bullet_class.call_count, 1)

        # Try to shoot again immediately
        self.gun.shoot()
        self.assertEqual(self.gun.last_shot_time, 1000)
        self.assertEqual(mock_bullet_class.call_count, 1)

        # Advance time and shoot again
        time.time.return_value += self.gun.cooldown_time + 0.01
        self.gun.shoot()
        expected_time = 1000 + self.gun.cooldown_time + 0.01
        self.assertEqual(self.gun.last_shot_time, expected_time)
        self.assertEqual(mock_bullet_class.call_count, 2)

    @patch('src.gun.Bullet')
    @patch('ursina.mesh_importer.load_model', return_value=MagicMock())
    @patch('ursina.texture_importer.load_texture', return_value=MagicMock())
    def test_recoil(self, mock_load_texture, mock_load_model, mock_bullet_class):
        from src.gun import Gun
        self.gun = Gun()

        initial_recoil_position = Vec3(self.gun.current_recoil_position)
        initial_recoil_rotation = Vec3(self.gun.current_recoil_rotation)

        self.gun.shoot()

        # Recoil should have been applied
        self.assertNotEqual(self.gun.current_recoil_position, initial_recoil_position)
        self.assertNotEqual(self.gun.current_recoil_rotation, initial_recoil_rotation)

    @patch('src.gun.Bullet')
    @patch('ursina.mesh_importer.load_model', return_value=MagicMock())
    @patch('ursina.texture_importer.load_texture', return_value=MagicMock())
    def test_update(self, mock_load_texture, mock_load_model, mock_bullet_class):
        from src.gun import Gun
        self.gun = Gun()

        initial_position = Vec3(self.gun.position)
        initial_rotation_x = self.gun.rotation_x
        initial_rotation_y = self.gun.rotation_y

        # Set some recoil and target rotations
        self.gun.current_recoil_position = Vec3(1, 1, 1)
        self.gun.current_recoil_rotation = Vec3(1, 1, 1)
        self.gun.target_rotation_x = 10
        self.gun.target_rotation_y = 20

        # Run update
        self.gun.update()

        # Position and rotation should have changed
        self.assertNotEqual(self.gun.position, initial_position)
        self.assertNotEqual(self.gun.rotation_x, initial_rotation_x)
        self.assertNotEqual(self.gun.rotation_y, initial_rotation_y)

    @patch('src.gun.Bullet')
    @patch('ursina.mesh_importer.load_model', return_value=MagicMock())
    @patch('ursina.texture_importer.load_texture', return_value=MagicMock())
    def test_set_target_rotation(self, mock_load_texture, mock_load_model, mock_bullet_class):
        from src.gun import Gun
        self.gun = Gun()

        self.gun.set_target_rotation(30, 40)
        expected_target_rotation_y = 30 + self.gun.rotation_offset.y
        expected_target_rotation_x = 40 + self.gun.rotation_offset.x
        self.assertEqual(self.gun.target_rotation_y, expected_target_rotation_y)
        self.assertEqual(self.gun.target_rotation_x, expected_target_rotation_x)

if __name__ == '__main__':
    unittest.main()
