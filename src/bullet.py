from ursina import *

class Bullet(Entity):
    """
    The Bullet class represents a projectile in the game. It handles the bullet's movement, 
    its speed, and its eventual destruction when it gets too far from the camera.
    """

    def __init__(self, position=Vec3(0, 0, 0), direction=Vec3(0, 0, 1), speed=60, rotation=Vec3(0, 0, 90), **kwargs):
        """
        Initializes the Bullet entity with a given position, direction, speed, and other properties.

        Args:
            position (Vec3): The starting position of the bullet. Defaults to (0, 0, 0).
            direction (Vec3): The direction in which the bullet will travel. Defaults to (0, 0, 1).
            speed (float): The speed at which the bullet travels. Defaults to 60.
            rotation (Vec3): The rotation of the bullet. Defaults to (0, 0, 90).
            **kwargs: Additional arguments passed to the Entity constructor.
        """
        super().__init__(
            model=Cylinder(6, start=-.5),  
            color=color.red,               
            scale=0.1,                     
            position=position,             
            **kwargs
        )
        self.direction = direction.normalized()  # Normalize the direction vector
        self.speed = speed  # Set the speed of the bullet
        self.emission_color = color.red  # Set the emission color of the bullet

    def update(self) -> None:
        """
        Called every frame to update the bullet's position. Destroys the bullet if it 
        gets too far from the camera.
        """
        # Move the bullet in its direction based on its speed
        self.position += self.direction * self.speed * time.dt

        # Destroy the bullet if it moves too far from the camera
        if distance(self.position, camera.position) > 200:
            destroy(self)
