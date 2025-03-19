from ursina import *

class Bullet(Entity):
    def __init__(self, position=Vec3(0, 0, 0), direction=Vec3(0, 0, 1), speed=60, rotation=Vec3(0, 0, 90), **kwargs):
        super().__init__(
            model='sphere',
            color=color.red,
            scale=0.1,
            position=position,
            collider='box',
            **kwargs
        )

        self.direction = direction.normalized()  # Normalize the direction vector
        self.speed = speed  # Set the speed of the bullet
        self.emission_color = color.red  # Set the emission color of the bullet
        self.damage = 10
        self.playerBullet = True

    def update(self) -> None:
        # Move the bullet in its direction based on its speed
        self.position += self.direction * self.speed * time.dt

        # Destroy the bullet if it moves too far from the camera
        if distance(self.position, camera.position) > 200:
            destroy(self)
