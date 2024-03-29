"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module principal du jeu démineur.
"""

import pygame
import sys

from grid import Grid
from gui import Gui
from item import Item
from player import Player
from trader import Trader

LEFT_CLICK, MIDDLE_CLICK, RIGHT_CLICK, = list(range(1, 4))

BOMB =              -1
COIN =              -2
MAGNIFIER =         -3
METAL_SCRAP =       -4
SHIELD =            -5
UPGRADER =          -6
BIONIC_GLASSES =    -7
ARMOR =             -8
JAMMER =            -9
RIFLE =             -10
FLAG =              -11

PASSIVE, ACTIVE = 0, 1

ITEM_VALUES = {
    "flag_sheet":       FLAG,
    "bomb_sheet":       BOMB,
    "coin_sheet":       COIN,
    "magnifier":        MAGNIFIER,
    "metal_scrap":      METAL_SCRAP,
    "shield":           SHIELD,
    "upgrader":         UPGRADER,
    "bionic_glasses":   BIONIC_GLASSES,
    "armor":            ARMOR,
    "jammer_sheet":     JAMMER,
    "rifle_sheet":      RIFLE
}

PLAYER_SPEAK =              0
PLAYER_INACTIVE =           1
PLAYER_MAGNIFIER =          2
PLAYER_MAGNIFIER_SHIELD =   3
PLAYER_MAGNIFIER_ARMOR =    4
PLAYER_GLASSES =            5
PLAYER_GLASSES_SHIELD =     6
PLAYER_SHIELD =             7
PLAYER_GLASSES_ARMOR =      8
PLAYER_ARMOR =              9
PLAYER_SUICIDE =            10
PLAYER_SUICIDE_ARMOR =      11
PLAYER_UPGRADER =           12
PLAYER_UPGRADER_SHIELD =    13
PLAYER_UPGRADER_ARMOR =     14
PLAYER_EXPLODE =            15
PLAYER_ASHES =              16

ANIMATION_SETTINGS = {
    FLAG:               [3, 6, [True, 0]],
    BOMB:               [5, 6, [False, 1]],
    COIN:               [6, None, [True, 0]],
    MAGNIFIER:          [0, None, [True, 0]],
    METAL_SCRAP:        [0, None, [True, 0]],
    SHIELD:             [0, None, [True, 0]],
    UPGRADER:           [0, None, [True, 0]],
    BIONIC_GLASSES:     [0, None, [True, 0]],
    ARMOR:              [0, None, [True, 0]],
    JAMMER:             [13, None, [True, 0]],
    RIFLE:              [9, None, [False, 0]],

    PLAYER_SPEAK:               [5, 2, [True, 0]],
    PLAYER_INACTIVE:            [5, 2, [True, 0]],
    PLAYER_MAGNIFIER:           [0, 60, [True, 0]],
    PLAYER_MAGNIFIER_SHIELD:    [5, 2, [True, 0]],
    PLAYER_MAGNIFIER_ARMOR:     [2, 2, [True, 0]],
    PLAYER_GLASSES:             [0, 2, [True, 0]],
    PLAYER_GLASSES_SHIELD:      [5, 2, [True, 0]],
    PLAYER_SHIELD:              [5, 2, [True, 0]],
    PLAYER_GLASSES_ARMOR:       [2, 2, [True, 0]],
    PLAYER_ARMOR:               [2, 2, [True, 0]],
    PLAYER_SUICIDE:             [3, 3, [False, 1]],
    PLAYER_SUICIDE_ARMOR:       [3, 2, [False, 1]],
    PLAYER_UPGRADER:            [0, 60, [True, 0]],
    PLAYER_UPGRADER_SHIELD:     [5, 2, [True, 0]],
    PLAYER_UPGRADER_ARMOR:      [2, 2, [True, 0]],
    PLAYER_EXPLODE:             [6, 4, [False, 1]]
}

FRAME_NUMBER, FPS_NUMBER, LOOP = 0, 1, 2

class Game:
    """
    Main game class.

    Parameters:
    screen (pygame.Surface): The screen on which to draw the game.
    width (int): The number of cells horizontally.
    height (int): The number of cells vertically.

    Attributes:
    screen (pygame.Surface): The screen on which to draw the game.
    clock (pygame.time.Clock): The clock used to control the game loop.
    width (int): The number of cells horizontally.
    height (int): The number of cells vertically.
    screen_width (int): The width of the screen in pixels.
    screen_height (int): The height of the screen in pixels.
    gui_width (int): The width of the GUI in pixels.
    gui (gui.Gui): The GUI for the game.
    player (player.Player): The player object.
    coin (coin.Coin): The coin object.
    magnifier (magnifier.Magnifier): The magnifier object.
    metal_scrap (metal_scrap.MetalScrap): The metal scrap object.
    shield (shield.Shield): The shield object.
    upgrader (upgrader.Upgrader): The upgrader object.
    bionic_glasses (bionic_glasses.Bionic_glasses): The bionic glasses object.
    armor (armor.Armor): The armor object.
    jammer (jammer.Jammer): The jammer off object.
    rifle (rifle.Rifle): The rifle object.
    items (dict): A dictionary of items in the game.
    square_size (int): The size of each square in pixels.
    x_offset (int): The x-coordinate of the left edge of the game grid in pixels.
    y_offset (int): The y-coordinate of the top edge of the game grid in pixels.
    """

    def __init__(self, screen, width: int, height: int):
        #self.sweeping_sound = pygame.mixer.Sound("sounds/sweeping.wav")
        #self.item_collected = pygame.mixer.Sound("sounds/item_collected.wav")
        self.k_pressed = False
        self.l_pressed = False
        self.m_pressed = False
        self.space_pressed = False
        self.round = 1
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width = width  # le nombre de cellules à l'horizontal
        self.height = height  # le nombre de cellules à la verticale
        self.screen_width = pygame.display.get_surface().get_width()
        self.screen_height = pygame.display.get_surface().get_height()
        self.gui_width = self.screen_width * 10 / 100
        self.gui = Gui(self, self.gui_width)
        self.player = Player(self)
        self.player_suicide = False
        self.bomb_exploding = False

        self.coin = Item(self, "coin_sheet", "right", ACTIVE, 7, self.screen_width * 1 /100, self.screen_width * 1 /100, self.screen_width * 4 /100)
        self.magnifier = Item(self, "magnifier", "bottom-right", ACTIVE, 1)
        self.metal_scrap = Item(self, "metal_scrap", "right", ACTIVE, 1, self.screen_width * 1 /100 + self.coin.image.get_width() * 2, self.screen_width * 1 /100, self.screen_width * 4 / 100)
        self.shield = Item(self, "shield", "bottom-right", PASSIVE, 1)
        self.upgrader = Item(self, "upgrader", "bottom-right", ACTIVE, 1)
        self.bionic_glasses = Item(self, "bionic_glasses", "bottom-right", ACTIVE, 1)
        self.armor = Item(self, "armor", "bottom-right", PASSIVE, 1)
        self.jammer = Item(self, "jammer_sheet", "bottom-right", ACTIVE, 14)
        self.rifle = Item(self, "rifle_sheet", "bottom-right", ACTIVE, 10)
        self.player_state = PLAYER_INACTIVE

        self.items = {
            COIN:            self.coin,
            MAGNIFIER:       self.magnifier,
            METAL_SCRAP:     self.metal_scrap,
            SHIELD:          self.shield,
            UPGRADER:        self.upgrader,
            BIONIC_GLASSES:  self.bionic_glasses,
            ARMOR:           self.armor,
            JAMMER:          self.jammer,
            RIFLE:           self.rifle
        }

        self.trader = Trader(self)
        self.is_trading = True
        self.is_trader_dead = False
        self.white = True
        self.current_time_already_exists = False

        self.square_size = int(min((self.screen_width - self.gui_width) / self.width, self.screen_height / self.height))
        self.x_offset = round((self.screen_width - self.gui_width - self.width * self.square_size) / 2)
        self.y_offset = round((self.screen_height - self.height * self.square_size) / 2)
        self.animations = {}
        self.player_state = PLAYER_INACTIVE
        self.latest_player_state = self.player_state

    def handling_events(self):
        """
        This function handles all the events that occur in the game.

        Parameters:
            None

        Returns:
            None
        """
        for item in self.player.discovered_items:
            self.items[item].is_clicked()

        if self.m_pressed:
            self.round += 1
            self.run()

        elif self.l_pressed and self.round > 1:
            self.round -= 1
            self.run()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # pygame.mixer.music.fadeout(1000)
                # pygame.time.delay(1000)
                pygame.quit()
                sys.exit()

        if not self.is_trading:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [1, 2, 3]:
                    # This block of code handles mouse clicks.

                    mouse_position = pygame.mouse.get_pos()
                    cell = ((mouse_position[0] - self.x_offset) // self.square_size,
                            (mouse_position[1] - self.y_offset) // self.square_size)

                    if cell in self.grid.grid:
                        if self.is_first_click:
                            self.grid.create_grid(cell)
                            # on tire les bombes au hasard
                            # en donnant cell afin que
                            # celui-ci ne soit pas une bombe

                            self.grid.cell_clicked(LEFT_CLICK, cell)
                            # afin de définir la cellules
                            # comme découverte (puisque
                            # elle ne peut pas être une bombe)
                            self.is_first_click = False
                            pygame.display.set_caption(f"Vous avez {self.grid.flag_to_place} {'drapeau' if self.grid.flag_to_place in [-1, 0, 1] else 'drapeaux'} à placer ! (manche {self.round})")

                        else:
                            self.grid.cell_clicked(event.button, cell)

                    else:
                        for item in self.player.discovered_items:
                            if item != COIN:
                                self.items[item].is_clicked()

                        self.player.is_clicked()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.m_pressed = True

                    elif event.key == pygame.K_l:
                        self.l_pressed = True

                    elif event.key == pygame.K_SPACE:
                        self.space_pressed = True

                    elif event.key == pygame.K_k and not self.k_pressed:
                        self.k_pressed = True

                        if self.is_first_click:
                            mouse_position = pygame.mouse.get_pos()
                            cell = ((mouse_position[0] - self.x_offset) // self.square_size,
                                    (mouse_position[1] - self.y_offset) // self.square_size)

                            if not cell in self.grid.grid:
                                cell = (9, 9)

                            self.grid.create_grid(cell)
                            self.grid.cell_clicked(LEFT_CLICK, cell)
                            self.is_first_click = False

                        self.grid.debug()

        elif self.is_trading and not self.is_trader_dead:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.trader.handling_events()

    def display(self):
        """
        This function is used to display the game elements on the screen.

        Parameters:
            None

        Returns:
            None
        """
        self.gui.display()
        for item in self.player.discovered_items:
            self.items[item].display()

        if self.player_state == PLAYER_EXPLODE and self.player.animation.lock_anim:
            self.player.display(self.player_state, 5, 5, ANIMATION_SETTINGS[self.player_state][FPS_NUMBER], [True, 0])
            self.player.animation.sprite_index = 5
            self.player.animation.lock_anim = False

        elif self.player_state in [PLAYER_SUICIDE, PLAYER_SUICIDE_ARMOR, PLAYER_SHIELD, PLAYER_GLASSES_SHIELD, PLAYER_UPGRADER_SHIELD, PLAYER_MAGNIFIER_SHIELD, PLAYER_ARMOR, PLAYER_GLASSES_ARMOR, PLAYER_UPGRADER_ARMOR, PLAYER_MAGNIFIER_ARMOR] and not self.player_suicide and not self.bomb_exploding:
            self.player.display(self.player_state, 0, 0, ANIMATION_SETTINGS[self.player_state][FPS_NUMBER], [False, 0])

        elif self.bomb_exploding:
            self.player.animation.lock_anim = False
            self.player.display(self.latest_player_state, 1, ANIMATION_SETTINGS[self.latest_player_state][FRAME_NUMBER], ANIMATION_SETTINGS[self.latest_player_state][FPS_NUMBER], [False, 1])

            if self.player.animation.lock_anim:
                self.player.animation.sprite_index = 0
                self.bomb_exploding = False

        else:
            self.player.display(self.player_state, 0, ANIMATION_SETTINGS[self.player_state][FRAME_NUMBER], ANIMATION_SETTINGS[self.player_state][FPS_NUMBER], ANIMATION_SETTINGS[self.player_state][LOOP])

        if not self.is_trading:
            pygame.draw.rect(self.screen, (152, 199, 64),
                pygame.Rect(0, 0,
                            self.x_offset, self.screen_height))

            pygame.draw.rect(self.screen, (152, 199, 64),
               pygame.Rect(self.screen_width - self.x_offset - self.gui_width, 0,
                           self.x_offset, self.screen_height))

            for coordinates, animation in self.animations.items():
                if animation.filename[8:-4] != "flag_sheet":
                    color = (229, 194, 159) if (coordinates[0] + coordinates[1]) % 2 == 0 else (215, 184, 153)

                else:
                    color = (170, 215, 81) if (coordinates[0] + round(coordinates[1])) % 2 == 0 else (162, 209, 73)

                pygame.draw.rect(self.screen, color,
                                pygame.Rect(round(coordinates[0]) * self.square_size + self.x_offset,
                                            round(coordinates[1]) * self.square_size + self.y_offset,
                                            self.square_size, self.square_size))

                image = animation.make_anim(0, 0, ANIMATION_SETTINGS[ITEM_VALUES[animation.filename[8:-4]]][FRAME_NUMBER], ANIMATION_SETTINGS[ITEM_VALUES[animation.filename[8:-4]]][FPS_NUMBER], ANIMATION_SETTINGS[ITEM_VALUES[animation.filename[8:-4]]][LOOP])
                image_x = self.square_size // 35 + coordinates[0] * self.square_size + self.x_offset
                image_y = self.square_size // 12 + coordinates[1] * self.square_size + self.y_offset
                self.screen.blit(image, (image_x, image_y))


        elif self.is_trading and not self.is_trader_dead:
            self.trader.display()
            self.trader.sign_hovered()
            self.coin.display()

            if RIFLE in self.player.discovered_items:
                self.items[RIFLE].display()

        elif self.is_trading and self.is_trader_dead:
            if self.white:
                self.screen.fill((255, 255, 255))
                if not self.current_time_already_exists:
                    self.current_time = pygame.time.get_ticks()
                    self.current_time_already_exists = True

                delay = 80
                if self.current_time + delay <= pygame.time.get_ticks():
                    self.white = False

            else:
                self.screen.fill((0, 0, 0))

        pygame.display.flip()

    def run(self):
        """
        This function initializes the game and runs the main game loop.

        Parameters:
            None

        Returns:
            None
        """

        if not self.is_trading:
            self.screen.fill((152, 199, 64))

            for y in range(0, self.height * self.square_size, self.square_size):
                for x in range(0, self.width * self.square_size, self.square_size):
                    if (x // self.square_size + y // self.square_size) % 2 == 0:
                        color = (170, 215, 81)
                    else:
                        color = (162, 209, 73)

                    pygame.draw.rect(self.screen, color,
                                    pygame.Rect(x + self.x_offset,
                                                y + self.y_offset,
                                                self.square_size,
                                                self.square_size))

            self.grid = Grid(self, self.width, self.height)

            self.is_first_click = True
            self.k_pressed = False
            self.l_pressed = False
            self.m_pressed = False
            self.animations = {}
            pygame.display.set_caption(f"Bonne chance ! (manche {self.round})")
            self.initial_time = pygame.time.get_ticks() // 60 * 10

        while True:
            self.handling_events()
            self.display()
            self.clock.tick(60)

# pygame.mixer.init(channels = 1, buffer = 2048)
# pygame.mixer.music.load("sounds/music.ogg")
pygame.init()
# pygame.mixer.music.set_volume(0.25)
# pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1200, 650))
game = Game(screen, 18, 18)
game.run()

pygame.quit()
sys.exit()