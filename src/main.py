from ursina import *
import sys
import os

from player import Player
from enemy import Enemy
from ui import UIManager
from state import StateMachine
from level import create_level
from src.enums.game_state import GameState

def main():
    app = Ursina()

    state_machine = StateMachine()
    ui_manager = UIManager(state_machine=state_machine)

    player = None
    enemies = []

    wave_number = 1  # Keeps track of the current wave

    create_level()

    def start_game():
        nonlocal player, enemies, wave_number
        wave_number = 1  # Reset the wave number

        state_machine.reset_game()

        # Destroy old entities if they exist
        if player:
            destroy(player)
            player = None
        for enemy in enemies:
            destroy(enemy)
        enemies.clear()

        # Create new player
        player = Player(
            stateMachine=state_machine,  # Changed from state_machine to stateMachine
            uiManager=ui_manager,        # Changed from ui_manager to uiManager
            position=(0, 1.5, 0),
            on_death=on_player_death
        )

        print(player)

        # Start the first wave
        start_wave()

        # Set the game state to PLAYING
        state_machine.game_state = GameState.PLAYING

        # Hide the mouse cursor during gameplay
        mouse.visible = False
        mouse.locked = True


    def start_wave():
        nonlocal enemies, wave_number
        print(f"Spawning wave {wave_number} with {wave_number} enemies.")
        for i in range(wave_number):
            enemy_position = Vec3(i * 5, 2, 10)  # Adjust positions as needed
            enemy = Enemy(player=player, state_machine=state_machine, position=enemy_position, on_death=on_enemy_death)
            enemies.append(enemy)

    def on_enemy_death(enemy):
        nonlocal enemies, wave_number
        enemies.remove(enemy)
        # Check if all enemies are dead
        if not enemies:
            wave_number += 1
            start_wave()

    def on_player_death():
        # Handle game over logic
        state_machine.game_state = GameState.GAME_OVER

        # Make the mouse cursor visible
        mouse.visible = True
        mouse.locked = False

        # Destroy all enemies
        for enemy in enemies:
            destroy(enemy)
        enemies.clear()

    # Disable the player (already done in player.die())

    # Set the initial game state to MENU
    ui_manager.start_game_callback = start_game
    ui_manager.restart_game_callback = start_game
    state_machine.game_state = GameState.MENU

    app.run()

if __name__ == "__main__":
    main()
