from ursina import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bullet import Bullet

class Gun(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Initialize with the parent provided by the Player class
        self.model = load_model('../assets/models/pistol.obj')
        self._double_sided = False
        self.double_sided_setter(False)
        self.color_texture = load_texture('../assets/images/pistol/color.png')


        self.texture = self.color_texture


        self.position_offset = Vec3(0.6, 0.3, 0.6)  # Position relative to the camera
        self.rotation_offset = Vec3(-3, 0, 0)  # Initial rotation offset

        self.scale = 0.4  # Adjust scale to fit the player's hand
        self.rotation = self.rotation_offset  # Start with the initial rotation

        # Y-axis and X-axis spring rotation
        self.current_rotation_y = self.rotation.y
        self.target_rotation_y = self.rotation.y
        self.rotation_velocity_y = 0  # Initial velocity

        self.current_rotation_x = self.rotation.x
        self.target_rotation_x = self.rotation.x
        self.rotation_velocity_x = 0  # Initial velocity

        # Spring properties
        self.spring_constant = 200.0
        self.damping = 0.8  # Higher damping to slow down the spring effect

        self.vertical_look_sensitivity = 200  # Adjust this value for more or less movement
        self.barrel_offset = Vec3(0, 0.7, 1.4)  # Adjust this to match the barrel's position

        self.cooldown_time = 0.2  # Half a second cooldown between shots
        self.last_shot_time = 0  # Time when the last shot was fired

        self.recoil_offset = Vec3(0, 0, -0.6)  # Backward movement when firing
        self.recoil_rotation = Vec3(-15, 0, 0)  # Upward rotation when firing
        self.current_recoil_position = Vec3(0, 0, 0)
        self.current_recoil_rotation = Vec3(0, 0, 0)

        self.recoil_damping = 5  # Lower value for a smoother return
    def update(self):
        # Base position relative to the camera
        base_position = camera.position + camera.forward * self.position_offset.z
        horizontal_offset = camera.right * self.position_offset.x
        vertical_offset = camera.up * (self.position_offset.y + camera.rotation_x * self.vertical_look_sensitivity)

        # Gradually return to the original position and rotation
        self.current_recoil_position = lerp(self.current_recoil_position, Vec3(0, 0, 0), time.dt * self.recoil_damping)
        self.current_recoil_rotation = lerp(self.current_recoil_rotation, Vec3(0, 0, 0), time.dt * self.recoil_damping)

        # Apply the recoil to the gun's position and rotation
        self.position = base_position + horizontal_offset + vertical_offset + self.current_recoil_position
        self.rotation_x = self.current_rotation_x + self.current_recoil_rotation.x
        self.rotation_y = self.current_rotation_y + self.current_recoil_rotation.y

        # Smoothly return the gun to its original rotation
        rotation_difference_y = self.target_rotation_y - self.current_rotation_y
        self.rotation_velocity_y += rotation_difference_y * self.spring_constant * time.dt
        self.rotation_velocity_y *= self.damping
        self.current_rotation_y += self.rotation_velocity_y * time.dt

        rotation_difference_x = self.target_rotation_x - self.current_rotation_x
        self.rotation_velocity_x += rotation_difference_x * self.spring_constant * time.dt
        self.rotation_velocity_x *= self.damping
        self.current_rotation_x += self.rotation_velocity_x * time.dt

    def set_target_rotation(self, target_rotation_y, target_rotation_x):
        self.target_rotation_y = target_rotation_y + self.rotation_offset.y
        self.target_rotation_x = target_rotation_x + self.rotation_offset.x

    def shoot(self):
        # Check if the cooldown has passed
        if time.time() - self.last_shot_time < self.cooldown_time:
            return  # If not enough time has passed since the last shot, do nothing

        # Update the last shot time
        self.last_shot_time = time.time()

        # Apply recoil effect in the local space
        self.current_recoil_position = self.forward * self.recoil_offset.z
        self.current_recoil_rotation = self.recoil_rotation

        # Calculate the bullet's starting position at the gun's barrel
        bullet_start_position = self.world_position + self.forward * self.barrel_offset.z \
                                + self.right * self.barrel_offset.x \
                                + self.up * self.barrel_offset.y

        # Shoot the bullet in the direction the gun is pointing
        bullet_direction = self.forward

        bullet = Bullet(position=bullet_start_position, direction=bullet_direction)

        print("Shot fired!")