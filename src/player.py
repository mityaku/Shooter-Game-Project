from ursina import *
import sys
import os

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gun import Gun
from src.state import StateMachine
from src.ui import UIManager
from src.enums.game_state import GameState
from src.enums.player_state import PlayerState

class Player(Entity):
    """
    The Player class represents the player character in the game. It manages movement,
    interactions with the environment, and integrates with the StateMachine and UIManager
    for game state management and UI updates.
    """

    def __init__(self, stateMachine: StateMachine, uiManager: UIManager, test: bool = False, **kwargs):
        """
        Initializes the Player entity with movement and state management capabilities.

        Args:
            stateMachine (StateMachine): The state machine managing the player's state.
            uiManager (UIManager): The UI manager responsible for updating the UI elements.
            test (bool): Indicates if the player is in test mode (used for testing purposes).
            **kwargs: Additional arguments passed to the Entity constructor.
        """
        super().__init__(
            model='cube',
            color=color.rgba(255, 165, 0, 0),
            scale_y=2,
            collider='box',
            **kwargs
        )
        self.test = test
        self.state_machine: StateMachine = stateMachine
        self.ui_manager: UIManager = uiManager
        self.speed: float = 30
        self.acceleration: float = 30
        self.jump_height: float = 2
        self.gravity: float = 9.81
        self.velocity: Vec3 = Vec3(0, 0, 0)
        self.grounded: bool = False
        self.friction: float = 5

        self.camera_pivot: Entity = Entity(parent=self, y=1)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 120
        mouse.locked = True

        self.gun: Gun = Gun(parent=self)

    def update(self) -> None:
        """
        Called every frame to update the player's state and handle input.
        Manages movement, gravity, jumping, and interaction with the gun and UI.
        """
        if self.state_machine.game_state != GameState.PLAYING and not self.test:
            return

        self.state_machine.heal(-0.1)
        self.handle_movement()
        self.apply_gravity()
        self.jump()
        self.apply_friction()

        # Update camera rotation based on mouse movement
        self.camera_pivot.rotation_y += mouse.velocity[0] * 2000 * time.dt
        self.camera_pivot.rotation_x -= mouse.velocity[1] * 1700 * time.dt
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -80, 80)

        # Update gun's rotation based on the camera's current rotation
        camera_y_rotation = self.camera_pivot.rotation_y
        camera_x_rotation = self.camera_pivot.rotation_x
        self.gun.set_target_rotation(camera_y_rotation, camera_x_rotation)

        if held_keys['left mouse']:
            self.gun.shoot()

        # Update UI elements
        self.ui_manager.update()

    def handle_movement(self) -> None:
        """
        Handles player movement based on keyboard input, applying directional velocity.
        """
        forward = Vec3(camera.forward.x, 0, camera.forward.z).normalized()
        right = Vec3(camera.right.x, 0, camera.right.z).normalized()

        direction = Vec3(
            forward * (held_keys['w'] - held_keys['s']) +
            right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        if direction != Vec3(0, 0, 0):
            self.velocity += direction * self.acceleration * time.dt
            if self.velocity.length() > self.speed:
                self.velocity = self.velocity.normalized() * self.speed

        self.position += self.velocity * time.dt

    def apply_gravity(self) -> None:
        """
        Applies gravity to the player, making them fall if not grounded.
        """
        if not self.grounded:
            self.velocity.y -= self.gravity * time.dt

        hit_info = self.intersects()
        if hit_info.hit:
            if self.velocity.y < 0:
                self.grounded = True
                self.velocity.y = 0
                self.y = hit_info.entity.world_y + 0.5 * self.scale_y
        else:
            self.grounded = False

    def jump(self) -> None:
        """
        Makes the player jump if they are grounded and the space bar is pressed.
        """
        if self.grounded and held_keys['space']:
            self.velocity.y += math.sqrt(2 * self.jump_height * self.gravity)
            self.grounded = False

    def apply_friction(self) -> None:
        """
        Applies friction to the player's horizontal movement, slowing them down over time.
        """
        if self.velocity.length() > 0:
            friction_force = self.friction * time.dt
            self.velocity.x -= self.velocity.x * friction_force
            self.velocity.z -= self.velocity.z * friction_force
