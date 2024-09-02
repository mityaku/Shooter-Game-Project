from ursina import Ursina
from ursina import *

from player import Player
from state import StateMachine
from ui import UIManager

from level import create_level

def main():
    app = Ursina(
        development_mode=True,
        borderless=False,
        fullscreen=False
    )
    create_level()

    stateMachine = StateMachine()
    uiManager = UIManager(stateMachine = stateMachine)

    Player(stateMachine = stateMachine, uiManager=uiManager, position=(0, 1.5, 0))

    app.run()

if __name__ == "__main__":
    main()
