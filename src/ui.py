from ursina import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.state import StateMachine

class UIManager:
    _instance = None

    def __new__(cls, stateMachine: StateMachine) -> 'UIManager':
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance.init_ui_manager(stateMachine)
        return cls._instance

    def init_ui_manager(self, state_machine: 'StateMachine') -> None:
        self.state_machine = state_machine
        health_bar_texture = load_texture('../assets/images/HealthBar.png')

        self.health_bar = Entity(parent=camera.ui, model='quad', texture=health_bar_texture, scale=(0.4, 0.03),
                                 position=(0, -0.45), origin=(0, 0))
        print("UIManager initialized with StateMachine")

    def update(self) -> None:
        health_percentage = self.state_machine.player_health / self.state_machine.max_health
        self.health_bar.scale_x = health_percentage * 0.4
        print(f"UIManager: Health bar updated to {health_percentage * 100:.2f}%")

