from ursina import *
import sys
import os
from math import atan2, degrees

# Add the src directory to the system path to allow imports from the src package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import StateMachine
from src.enums.game_state import GameState

class Enemy(Entity):
    """
    The Enemy class represents an enemy entity that follows the player, faces them along the Y-axis,
    hovers towards them with low friction, and shoots bullets that can damage the player.
    It also handles taking damage from bullets and being destroyed when health reaches zero.
    """

    def __init__(self, player, on_death=None, **kwargs):
        """
        Initializes the Enemy entity with a model, texture, health, and behavior to follow and attack the player.

        Args:
            player (Entity): The player instance to follow and attack.
            game_manager (GameManager): The game manager instance to notify when the enemy dies.
            **kwargs: Additional arguments passed to the Entity constructor.
        """
        super().__init__(
            model=load_model('../assets/models/untitled.fbx'),  # Replace with your enemy model path
            texture=load_texture('../assets/images/drone_d.png'),  # Replace with your enemy texture path
            collider='box',
            scale=random.randint(3,12)/1000,
            **kwargs
        )
        self.player = player
        self.state_machine = StateMachine()
        self.speed = random.randint(4, 12)  # Movement speed towards the player
        self.hover_height = random.randint(2,5)  # The height at which the enemy hovers
        self.friction = random.randint(1,3)/10  # Low friction for hovering effect
        self.velocity = Vec3(0, 0, 0)
        self.shoot_distance = 15.0  # Distance at which the enemy starts shooting
        self.shoot_cooldown = 1  # Time between shots in seconds
        self.last_shot_time = 0.0
        self.on_death = on_death

        # Health properties
        self.health = 100  # Enemy's starting health
        self.max_health = 100

        # Death animation flag
        self.is_dying = False

    def update(self):
        """
        Updates the enemy's behavior every frame: follow the player, face the player along Y-axis,
        check for collisions with bullets, and shoot at the player if in range.
        """
        if self.state_machine.game_state != GameState.PLAYING:
            return

        # If the enemy is dying, skip the rest of the update
        if self.is_dying:
            return
        
        if not self.player or not self.player.enabled:
            # Player is dead or doesn't exist; skip enemy actions
            destroy(self)
            return

        # Calculate the direction towards the player, ignoring Y-axis
        direction = self.player.position - self.position
        direction.y = 0  # Ignore vertical difference
        distance_to_player = direction.length()
        if distance_to_player > 0:
            direction = direction.normalized()
        else:
            direction = Vec3(0, 0, 0)

        # Calculate the yaw angle to face the player
        angle = degrees(atan2(direction.x, direction.z))
        self.rotation_y = angle

        # Move towards the player with hovering effect
        self.velocity += direction * self.speed * time.dt
        self.velocity -= self.velocity * self.friction * time.dt  # Apply friction
        self.position += self.velocity * time.dt

        # Maintain hovering height
        self.y = self.hover_height

        # Shooting logic
        if distance_to_player <= self.shoot_distance:
            current_time = time.time()
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.shoot_at_player()
                self.last_shot_time = current_time

        # Collision detection with bullets
        self.check_bullet_collision()

    def shoot_at_player(self):
        """
        Shoots a bullet towards the player that can damage them.
        """
        # Calculate the bullet's starting position at the enemy's position
        bullet_start_position = self.position + self.forward * 1.5  # Adjust as needed

        # Shoot the bullet towards the player
        bullet_direction = (self.player.position - self.position).normalized()
        EnemyBullet(position=bullet_start_position, direction=bullet_direction, player=self.player)

        print("Enemy shot fired!")

    def take_damage(self, amount):
        """
        Reduces the enemy's health by the specified amount and checks for death.

        Args:
            amount (int): The amount of damage to apply to the enemy.
        """
        self.health -= amount
        print(f"Enemy health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.die()

    def die(self):
        if self.is_dying:
            return  # Already dying, do not initiate again

        print("Enemy died!")
        self.is_dying = True


        self.player.state_machine.add_kill()

        # Disable enemy's collider and movement
        self.collider = None
        self.velocity = Vec3(0, 0, 0)

        # Remove reference to the player
        self.player = None

        # Animate the enemy flying up quickly
        self.animate_y(self.y + 100, duration=1, curve=curve.in_expo)

        # Schedule destruction after animation is complete
        invoke(self.destroy_enemy, delay=1)


    def destroy_enemy(self):
        """
        Destroys the enemy entity and calls the on_death callback.
        """
        if self.on_death:
            print("fired omn death")
            self.on_death(self)
        destroy(self)

    def check_bullet_collision(self):
        """
        Checks for collision with player bullets and applies damage if hit.
        """
        # Iterate over all entities in the scene
        for entity in scene.entities:
            # Skip self and non-Entity instances
            if entity == self or not isinstance(entity, Entity):
                continue
            # Skip if the entity doesn't have a 'damage' attribute (assuming bullets have 'damage')
            if not hasattr(entity, 'damage'):
                continue
            # Skip if the entity is an EnemyBullet
            if isinstance(entity, EnemyBullet):
                continue
            # Check for collision with the bullet
            if self.intersects(entity).hit:
                # Apply damage and destroy the bullet
                self.take_damage(entity.damage)
                destroy(entity)
                print("Enemy hit by player bullet!")
                break  # Break after handling one bullet collision per frame

class EnemyBullet(Entity):
    """
    The EnemyBullet class represents a bullet fired by the enemy that can damage the player.
    """

    def __init__(self, position=Vec3(0, 0, 0), direction=Vec3(0, 0, 1), speed=20.0, player=None, **kwargs):
        """
        Initializes the EnemyBullet entity.

        Args:
            position (Vec3): The starting position of the bullet.
            direction (Vec3): The direction in which the bullet will travel.
            speed (float): The speed at which the bullet travels.
            player (Entity): The player instance to target.
            **kwargs: Additional arguments passed to the Entity constructor.
        """
        super().__init__(
            model='sphere',
            color=color.red,
            scale=0.2,
            position=position,
            collider='sphere',
            **kwargs
        )
        self.direction = direction.normalized()
        self.speed = speed
        self.damage = 10  # Damage dealt to the player
        self.player = player  # Reference to the player

    def update(self):
        """
        Updates the bullet's position every frame and checks for collision with the player.
        """
        
        if not self.player or not self.player.enabled:
            # Player is dead or doesn't exist; skip enemy actions
            destroy(self)
            return
        
        self.position += self.direction * self.speed * time.dt

        # Destroy the bullet if it moves too far from the player
        if distance(self.position, self.player.position) > 100:
            destroy(self)
            return

        # Check for collision with the player
        if self.intersects(self.player).hit:
            # Damage the player
            print(self.player.health)
            self.player.take_damage(self.damage)
            destroy(self)
            print("Player hit by enemy bullet!")
