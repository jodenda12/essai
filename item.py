"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module item: gestion des objets du jeu
"""

import pygame
from anim import Spritesheet

PASSIVE, ACTIVE = 0, 1

BOMB = -1
COIN = -2
MAGNIFIER = -3
METAL_SCRAP = -4
SHIELD = -5
UPGRADER = -6
BIONIC_GLASSES = -7
ARMOR = -8
JAMMER = -9
RIFLE = -10

ITEM_VALUES = {
    "bomb": BOMB ,
    "coin_sheet": COIN,
    "magnifier": MAGNIFIER,
    "metal_scrap": METAL_SCRAP,
    "shield": SHIELD,
    "upgrader": UPGRADER,
    "bionic_glasses": BIONIC_GLASSES,
    "armor": ARMOR,
    "jammer_sheet": JAMMER,
    "rifle_sheet": RIFLE
}

UPGRADED = {
    ITEM_VALUES["magnifier"]: ITEM_VALUES["bionic_glasses"],
    ITEM_VALUES["shield"]: ITEM_VALUES["armor"]
}

PLAYER_STATES = {
    (None, None): 1,
    (MAGNIFIER, None): 2,
    (MAGNIFIER, SHIELD): 3,
    (MAGNIFIER, ARMOR): 4,
    (BIONIC_GLASSES, None): 5,
    (BIONIC_GLASSES, SHIELD): 6,
    (None, SHIELD): 7,
    (BIONIC_GLASSES, ARMOR): 8,
    (None, ARMOR): 9,
    (RIFLE, None): 10,
    (RIFLE, ARMOR): 11,
    (UPGRADER, None): 12,
    (UPGRADER, SHIELD): 13,
    (UPGRADER, ARMOR): 14
}

class Item():
    """
    This class represents an item in the game.

    Parameters:
    game (Game): The game instance that the item is associated with.
    item (str): The name of the item.
    text_position (str): The position of the item's amount text.
    Can be "bottom-right" or "right".
    item_type (int): The type of the item. Can be either PASSIVE or ACTIVE.
    x (int): The x-coordinate of the top-left corner of the item.
    If not specified, the item is placed at a default position.
    y (int): The y-coordinate of the top-left corner of the item.
    If not specified, the item is placed at a default position.
    size (int): The size of the item's sprite image.
    If not specified, the item is scaled to a default size.

    Attributes:
    game (Game): The game instance that the item is associated with.
    item (str): The name of the item.
    text_position (str): The position of the item's amount text.
    Can be "bottom-right" or "right".
    item_type (int): The type of the item. Can be either PASSIVE or ACTIVE.
    x (int): The x-coordinate of the top-left corner of the item.
    y (int): The y-coordinate of the top-left corner of the item.
    size (int): The size of the item's sprite image.
    image (Surface): The sprite image of the item.
    rect (Rect): The bounding rectangle of the item's image.
    amount (int): The amount of the item.
    player_equipped (dict): A dictionary that stores the
    equipped items for the player's passive and active slots.
    value (int): The value of the item. This is used to
    determine whether the player can equip the item or not.
    """

    def __init__(self, game, item: str, text_position: str, item_type: int, frame_number_x: int, x = None, y = None, size = None):
        self.item = item
        self.game = game
        self.text_position = text_position
        self.item_type = item_type
        self.value = ITEM_VALUES[self.item]
        self.frame_number_x = frame_number_x

        if x is None:
            self.x = self.game.screen_width - self.game.gui_width + self.game.gui_width // 4

        else:
            self.x = x

        if y is None:
            self.y = round(self.game.screen_height * 2/100) + self.game.gui.offset_y
            self.game.gui.offset_y += round((self.game.screen_height - self.game.player.image.get_height() * 150/100) / 7)

        else:
            self.y = y

        if size is None:
            size = self.game.gui_width // 2.5

        self.animation = Spritesheet(f"sprites/{self.item}.png", frame_number_x, 1, (size, size), 15)
        self.image = self.animation.get()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.amount = 0
        self.amount += 100

        if self.value == SHIELD:
            self.health_point = 1

        elif self.value == ARMOR:
            self.health_point = 2

    def display(self):
        """
        Draw the item on the screen.

        This function draws the item's sprite image at its current position on the screen.
        It also displays the item's amount text, if applicable.

        Parameters:
        None

        Returns:
        None
        """
        self.game.screen.blit(self.image, (self.x, self.y))
        font = pygame.font.SysFont("Arial", self.image.get_height() // 3)
        image = font.render("x" + str(self.amount), True, (255, 255, 255))

        if self.text_position == "bottom-right":
            text_y = self.y + self.image.get_height() - image.get_height()

        elif self.text_position == "right":
            text_y = round(self.y + self.image.get_height() / 2 - image.get_height() / 2)

        text_x = round(self.x + self.image.get_width() * 100.5/100)
        self.game.screen.blit(image, (text_x, text_y))

    def anim(self):
        """
        Anim the item using the SpriteSheet object
        """
        frame_number_x = self.frame_number_x - 1

        self.image = self.animation.make_anim(0, 0, frame_number_x, None, [self.value != COIN and self.value != RIFLE, 0])

    def picked(self):
        """
        Increment the amount of the item by 1.

        Parameters:
            None

        Returns:
            None
        """
        self.amount += 1

    def is_clicked(self):
        """
        Check if the item is clicked.

        This function checks if the mouse cursor is currently hovering over the item.
        If it is, it decrements the item's amount and equips it if it is possible to do so.

        Parameters:
            None

        Returns:
            None
        """
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.anim()
            if not self.game.is_trading:
                if self.value != COIN:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.game.player.active_equipped == ITEM_VALUES["upgrader"] and self.amount > 0 and (self.value in UPGRADED.keys()):
                                self.amount -= 1

                                if not UPGRADED[self.value] in self.game.player.discovered_items:
                                    self.game.player.discovered_items.append(UPGRADED[self.value])

                                self.game.items[UPGRADED[self.value]].picked()
                                self.game.player.active_equipped = None

                            else:
                                if self.value != METAL_SCRAP:
                                    if self.item_type == PASSIVE:
                                        if self.game.player.passive_equipped is None:
                                            if self.amount > 0:
                                                self.health = self.health_point
                                                self.game.player.passive_equipped = self.value
                                                self.amount -= 1

                                    elif self.item_type == ACTIVE:
                                        if self.game.player.active_equipped == self.value:
                                            self.picked()
                                            self.game.player.active_equipped = None

                                        else:
                                            if self.amount > 0:
                                                if self.game.player.active_equipped is None:

                                                    self.game.player.active_equipped = self.value
                                                    self.amount -= 1

                                                elif self.game.player.active_equipped != self.value:
                                                    self.game.items[self.game.player.active_equipped].picked()
                                                    self.game.player.active_equipped = self.value
                                                    self.amount -= 1

                                elif self.value == METAL_SCRAP:
                                    if self.amount >= 5:
                                        self.amount -= 5
                                        self.game.items[JAMMER].amount += 1

                                        if not JAMMER in self.game.player.discovered_items:
                                            self.game.player.discovered_items.append(JAMMER)

            else:
                if self.value == RIFLE:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.game.player.active_equipped != self.value:
                                self.game.player.active_equipped = self.value
                                self.amount -= 1

                            else:
                                self.picked()
                                self.game.player.active_equipped = None

            if (self.game.player.active_equipped, self.game.player.passive_equipped) in PLAYER_STATES.keys():
                self.game.player_state = PLAYER_STATES[(self.game.player.active_equipped, self.game.player.passive_equipped)]

        else:
            self.image = pygame.image.load(f"sprites/{self.item}.png").convert_alpha()
            self.image = self.animation.make_anim(0, 0, 0, None, [False, 0])
            self.animation.sprite_index = 0
            self.animation.lock_anim = False