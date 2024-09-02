from ursina import *

def create_level() -> None:
    """
    Creates the game level by setting up the ground, ambient light, and a custom skybox.
    This function initializes essential elements of the environment.

    Returns:
        None
    """
    # Create the ground entity with a large plane model and apply texture
    ground = Entity(model='plane', scale=(100, 1, 100), collider='box')
    ground.texture = load_texture('../assets/images/ground.png')
    ground.texture_scale = (5, 5)  # Scale the texture to repeat across the ground

    # Add ambient lighting to the scene with a specific rotation and color
    AmbientLight(y=2, z=3, rotation=(45, -45, 45), color=(color.rgb(255, 50, 50)))

    # Create a custom skybox using a spherical model and apply a texture to it
    custom_skybox = Sky()
    custom_skybox.texture = load_texture('../assets/images/Sky.png')
    custom_skybox.scale = 1000  # Scale the skybox to encompass the entire scene
    custom_skybox.double_sided_setter(True)  # Ensure the skybox is visible from the inside
    custom_skybox.model = 'sphere'  # Use a spherical model for the skybox
