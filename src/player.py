from ursina import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gun import Gun 
from src.state import StateMachine
from src.ui import UIManager

from src.enums.game_state import GameState
from src.enums.player_state import PlayerState

class Player(Entity):
    def __init__(self, stateMachine: StateMachine, uiManager: UIManager, test: bool = False, **kwargs):
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
        if self.state_machine.game_state != GameState.PLAYING:
            if self.test == False:
                return

        self.state_machine.heal(-0.1)
        self.handle_movement()
        self.apply_gravity()
        self.jump()
        self.apply_friction()

        self.camera_pivot.rotation_y += mouse.velocity[0] * 40 * time.dt
        self.camera_pivot.rotation_x -= mouse.velocity[1] * 40 * time.dt
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -80, 80)

        camera_y_rotation = self.camera_pivot.rotation_y
        camera_x_rotation = self.camera_pivot.rotation_x

        self.gun.set_target_rotation(camera_y_rotation, camera_x_rotation)

        if held_keys['left mouse']:
            self.gun.shoot()

        self.ui_manager.update()



    def handle_movement(self) -> None:
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

        self.camera_pivot.rotation_y += mouse.velocity[0] * 40
        self.camera_pivot.rotation_x -= mouse.velocity[1] * 40
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -80, 80)

    def apply_gravity(self) -> None:
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
        if self.grounded and held_keys['space']:
            self.velocity.y += math.sqrt(2 * self.jump_height * self.gravity)
            self.grounded = False

    def apply_friction(self) -> None:
        if self.velocity.length() > 0:
            friction_force = self.friction * time.dt
            self.velocity.x -= self.velocity.x * friction_force
            self.velocity.z -= self.velocity.z * friction_force

