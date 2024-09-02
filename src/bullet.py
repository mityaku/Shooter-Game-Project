from ursina import *

class Bullet(Entity):
    def __init__(self, position=Vec3(0, 0, 0), direction=Vec3(0, 0, 1), speed=60, rotation=Vec3(0,0,90), **kwargs):
        super().__init__(
            model=Cylinder(6, start=-.5),
            color=color.red,
            scale=0.1,
            position=position,
            **kwargs
        )
        self.direction = direction.normalized()
        self.speed = speed
        self.emission_color = color.red

    def update(self) -> None:
        self.position += self.direction * self.speed * time.dt

        if distance(self.position, camera.position) > 200:
            destroy(self)
