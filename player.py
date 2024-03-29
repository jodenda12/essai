"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module player: gère l'affichage de l'avatar du joueur en bas à droite du plateau.
"""

import pygame

from anim import Spritesheet

COIN = -2
MAGNIFIER = -3
METAL_SCRAP = -4
SHIELD = -5
UPGRADER = -6
BIONIC_GLASSES = -7
ARMOR = -8
JAMMER = -9
RIFLE = -10

SPRITE_WIDTH =  150
SPRITE_HEIGHT = 150

class Player:
    """
    Class representing the player in the game.

    Parameters:
        game (Game): The game instance the player belongs to.

    Attributes:
        discovered_items (list): A list of items that the player has discovered.
        game (Game): The game instance the player belongs to.
        image (pygame.Surface): The image of the player.
        x (int): The x-coordinate of the player.
        y (int): The y-coordinate of the player.
        passive_equipped (int): The ID of the passive item equipped by the player.
        active_equipped (int): The ID of the active item equipped by the player.
    """

    def __init__(self, game):
        self.discovered_items = [COIN, MAGNIFIER, METAL_SCRAP, SHIELD, UPGRADER, BIONIC_GLASSES, ARMOR, JAMMER, RIFLE]
        self.game = game
        self.x = self.game.screen_width - self.game.gui_width
        self.y = self.game.screen_height - self.game.gui_width

        self.animation = Spritesheet("sprites/player_sheet.png", 7, 16, (self.game.gui_width, self.game.gui_width), 2)
        self.image = self.animation.get()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.passive_equipped = None
        self.active_equipped = None

    def display(self, line: int, start_frame: int, end_frame: int, fps: int, loop: bool):
        """
        Display the player on the screen.

        Args:
            None

        Returns:
            None
        """
        self.image = self.animation.make_anim(line, start_frame, end_frame, fps, loop)
        self.game.screen.blit(self.image, (self.x, self.y))

    def is_clicked(self):
        """
        Check if the player is clicked.

        This function checks if the mouse cursor is currently hovering over the player.
        If it is and if the player has the rifle equipped, it changes the animation.

        Parameters:
            None

        Returns:
            None
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.active_equipped == RIFLE:
            self.game.player_suicide = True