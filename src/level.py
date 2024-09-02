from ursina import *

def create_level() -> None:
    ground = Entity(model='plane', scale=(100, 1, 100), collider='box')
    ground.texture = load_texture('../assets/images/ground.png')
    ground.texture_scale = (5,5)

    AmbientLight(y=2, z=3, rotation=(45, -45, 45), color=(color.rgb(255,50,50)))

    custom_skybox = Sky()
    custom_skybox.texture = load_texture('../assets/images/Sky.png')
    custom_skybox.scale = 1000
    custom_skybox.double_sided_setter(True)
    custom_skybox.model = 'sphere'
    
