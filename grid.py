"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module grid: gestion de l'affichage du plateau de jeu
"""

import pygame
import random

from anim import Spritesheet

LEFT_CLICK, MIDDLE_CLICK, RIGHT_CLICK, WHEELUP, WHEELDOWN = list(range(1, 6))

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

PLAYER_EXPLODE = 15

ITEM_NAME = {-1: "bomb_sheet", -2: "coin_sheet", -3: "magnifier", -4: "metal_scrap",
             -5: "shield", -6: "upgrader", -7: "bionic_glasses",
             -8: "armor", -9: "jammer_sheet", -10: "rifle_sheet"}

ITEM_IMAGES = {
    BOMB: "bomb_sheet",
    COIN: "coin_sheet",
    MAGNIFIER: "magnifier",
    METAL_SCRAP: "metal_scrap",
    SHIELD: "shield",
    UPGRADER: "upgrader",
    BIONIC_GLASSES: "bionic_glasses",
    ARMOR: "armor",
    JAMMER: "jammer_sheet",
    RIFLE: "rifle_sheet"
}

FRAME_AND_FPS_NUMBER = {
    BOMB: [6, 6],
    COIN: [7, 20],
    MAGNIFIER: [1, 20],
    METAL_SCRAP: [1, 20],
    SHIELD: [1, 20],
    UPGRADER: [1, 15],
    BIONIC_GLASSES: [1, 20],
    ARMOR: [1, 20],
    JAMMER: [14, 20],
    RIFLE: [10, 20]
}

FRAME_NUMBER, FPS_NUMBER = 0, 1

ITEM_PER_ROUND = {
    1: {COIN: 0, MAGNIFIER: 0, METAL_SCRAP: 0,
        SHIELD: 0, BOMB: 10},

    2: {COIN: 100, MAGNIFIER: 0, METAL_SCRAP: 0, 
        SHIELD: 0, BOMB: 15},

    3: {COIN: 65, MAGNIFIER: 20, METAL_SCRAP: 15,
        SHIELD: 0, BOMB: 16},

    4: {COIN: 63, MAGNIFIER: 15, METAL_SCRAP: 15,
        SHIELD: 7, BOMB: 19}
}

CELL_VALUE, CELL_STATE, IS_COLLECTED = 0, 1, 2
FLAGGED, HIDDEN, NOT_HIDDEN = -1, 0, 1
NOT_COLLECTED, COLLECTED = False, True

COLORS = {-1: (66, 36, 66),
          1: (25, 118, 210),
          2: (56, 142, 60),
          3: (211, 47, 47),
          4: (123, 31, 162),
          5: (255, 143, 0),
          6: (0, 0, 0),
          7: (0, 0, 0),
          8: (0, 0, 0)}

class Grid:
    """
    This class is used to manage the display of the game grid.

    Parameters
    ----------
    game : Game
        The game instance that this grid belongs to.
    width : int
        The width of the grid.
    height : int
        The height of the grid.

    Attributes
    ----------
    game : Game
        The game instance that this grid belongs to.
    width : int
        The width of the grid.
    height : int
        The height of the grid.
    grid : dict
        A dictionary that stores the state of each cell on the grid. The keys are
        tuples of (x, y) coordinates, and the values are a list containing the
        following values:

        * CELL_VALUE: The value of the cell, which can be a number, a bomb, or an
          item.
        * CELL_STATE: The state of the cell, which can be hidden, flagged, or
          visible.
        * IS_COLLECTED: A boolean value indicating whether the cell contains an
          item that has been collected.

    bomb_number : int
        The number of bombs on the grid. This value is calculated based on the
        current round.
    items_to_pick : dict
        A dictionary that stores the number of items of each type that need to be
        placed on the grid. The keys are the item types, and the values are the
        number of items.
    number_of_item_to_place : int
        The total number of items that need to be placed on the grid. This value
        is calculated based on the bomb_number and the current round.
    flag_to_place : int
        The number of flags that need to be placed on the grid. This value is
        calculated based on the bomb_number and the number of items that need to
        be placed.
    safe_cells_number : int
        The number of safe cells on the grid. This value is calculated based on
        the total number of cells and the bomb_number.
    not_hidden_cells : int
        The number of cells that are not currently hidden. This value is updated
        as cells are revealed or flagged.

    Methods
    -------
    get_all_cells_around(cell)
        Returns a list of all the cells surrounding the given cell.
    create_grid(cell)
        Creates a grid of bombs and items around the given cell.
    cell_clicked(button, cell, play_sound=True)
        Handles a click on a cell.
    __str__()
        Returns a string representation of the grid.
    display(cell)
        Renders the grid on the screen.
    """

    def __init__(self, game, width: int, height: int):
        self.game = game
        self.width = width
        self.height = height
        self.grid = {}
        self.flag_to_place = 0

        for h in range(height):
            for w in range(width):
                self.grid[(w, h)] = [CELL_VALUE, HIDDEN, NOT_COLLECTED]

        total_cells = self.width * self.height

        self.items_to_pick = {}

        if self.game.round <= 4:
            local_round = self.game.round
            bomb_percentage = ITEM_PER_ROUND[self.game.round][BOMB]
            bomb_number = round(total_cells * bomb_percentage/100)

            for item in ITEM_PER_ROUND[self.game.round]:
                if item != BOMB:
                    self.items_to_pick[item] = 0

                else:
                    self.items_to_pick[item] = bomb_number

        else:
            local_round = 4
            bomb_percentage = ITEM_PER_ROUND[4][BOMB] + 3 * (self.game.round - 4)

            if bomb_percentage > 100:
                bomb_percentage = 100

            bomb_number = round(total_cells * bomb_percentage/100)

            for item in ITEM_PER_ROUND[4]:
                if item != BOMB:
                    self.items_to_pick[item] = 0

                else:
                    self.items_to_pick[item] = bomb_number

            if self.game.round == 6:
                self.items_to_pick[RIFLE] = 1
                self.flag_to_place += 1

        if self.game.round > 1:
            item_percentage = 10
            if bomb_percentage + item_percentage > 100:
                item_percentage = 100 - bomb_percentage

            self.number_of_item_to_place = round(bomb_number * item_percentage/100)

        else:
            self.number_of_item_to_place = 0

        for item_number in range(self.number_of_item_to_place):
            random_number = round(random.random() * 100)

            if random_number == 0:
                random_number = 1

            for item, chance in ITEM_PER_ROUND[local_round].items():
                if item != BOMB and item != COIN and chance > 0:
                    min = 0
                    for i in range(item + 1, -1):
                        min += ITEM_PER_ROUND[local_round][i]

                    max = 0
                    for i in range(item, -1):
                        max += ITEM_PER_ROUND[local_round][i]

                    if min < random_number <= max:
                        self.items_to_pick[item] += 1

                elif item == COIN:
                    if random_number <= chance:
                        self.items_to_pick[item] += 1

        self.flag_to_place += bomb_number + self.number_of_item_to_place
        self.safe_cells_number = total_cells - bomb_number
        self.not_hidden_cells = 0
        self.items_flagged = []
        self.jammer_to_give_back = 0
        self.temp_animations = []

    def get_all_cells_around(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns a list of all the cells surrounding the given cell.

        Parameters
        ----------
        cell: tuple[int, int]
            The coordinates of the center cell.

        Returns
        -------
        all_cells: list[tuple[int, int]]
            A list of tuples, each representing the coordinates of a cell.
        """
        all_cells = []
        for delta_row in [-1, 0, 1]:
            for delta_column in [-1, 0, 1]:
                if ((delta_row, delta_column)!= (0, 0) and 0 <= cell[1] + delta_row < self.height and 0 <= cell[0] + delta_column < self.width):
                    all_cells.append((cell[0] + delta_column, cell[1] + delta_row))

        return all_cells

    def create_grid(self, cell: tuple[int, int]):
        """
        Creates a grid of bombs and items around the given cell.

        Parameters
        ----------
        cell : tuple[int, int]
            The coordinates of the center cell.

        Returns
        -------
        None
        """
        shuffled_grid = [i for i in self.grid]
        shuffled_grid.pop(shuffled_grid.index(cell))
        all_cells = self.get_all_cells_around(cell)

        for cell in all_cells:
            shuffled_grid.pop(shuffled_grid.index(cell))

        random.shuffle(shuffled_grid)

        def pick_and_update_cells_around(item, amount):
            """
            A helper function that picks and updates cells around a given cell.

            Parameters
            ----------
            to_pick : list[int, int]
                A list containing the value and number of cells to pick.

            Returns
            -------
            None
            """
            for index in range(len(shuffled_grid[:amount])):
                if index >= len(shuffled_grid[:amount]):
                    return

                cell = shuffled_grid[index]
                shuffled_grid.pop(index)
                self.grid[cell][CELL_VALUE] = item

                # la partie qui suit est l'algorithme proposé par Axel, permettant de
                # définir pour chaque cellules pour lesquelles c'est nécessaire, le
                # nombre de bombes se trouvant autour de celles-ci
                all_cells = self.get_all_cells_around(cell)

                for cell in all_cells:
                    if self.grid[cell][CELL_VALUE] >= 0:
                    # cette condition permet de vérifier si la
                    # cellule n'est ni une bombe ni un item
                        self.grid[cell][CELL_VALUE] += 1

        for item, amount in self.items_to_pick.items():
            pick_and_update_cells_around(item, amount)

    def cell_clicked(self, button: int,
                     cell: tuple[int, int],
                     play_sound: bool = True):
        """
        Handles a click on a cell.

        Parameters
        ----------
        button : int
            The mouse button that was clicked. Can be LEFT_CLICK, MIDDLE_CLICK,
            RIGHT_CLICK, WHEELUP, or WHEELDOWN.
        cell : tuple[int, int]
            The coordinates of the cell that was clicked.
        play_sound : bool, optional
            A boolean value indicating whether to play the sweeping sound when an
            unrevealed cell is clicked. The default is True.

        Returns
        -------
        None
        """
        if button == LEFT_CLICK:
            if self.game.player.active_equipped == BIONIC_GLASSES and not self.game.is_first_click:
                self.game.player.active_equipped = MAGNIFIER
                self.cell_clicked(LEFT_CLICK, cell, False)

                all_cells = self.get_all_cells_around(cell)
                for temp_cell in all_cells:
                    self.game.player.active_equipped = MAGNIFIER
                    self.cell_clicked(LEFT_CLICK, temp_cell, False)

                self.game.player.active_equipped = None

            else:
                if self.grid[cell][CELL_STATE] == HIDDEN:
                    if play_sound and self.grid[cell][CELL_VALUE] != BOMB:
                        # self.game.sweeping_sound.play()
                        pass

                    if self.grid[cell][CELL_VALUE] < 0:
                        self.flag_to_place -= 1

                        if self.grid[cell][CELL_VALUE] == BOMB:
                            if self.game.player.active_equipped == MAGNIFIER:
                                self.grid[cell][CELL_STATE] = FLAGGED
                                self.game.player.active_equipped = None
                                self.game.player_state = PLAYER_STATES[(self.game.player.active_equipped, self.game.player.passive_equipped)]

                            else:
                                jammer_near = False
                                all_cells = self.get_all_cells_around(cell)
                                for temp_cell in all_cells:
                                    if self.grid[temp_cell][CELL_VALUE] == JAMMER:
                                        jammer_near = True

                                if jammer_near:
                                    self.grid[cell][CELL_STATE] = NOT_HIDDEN

                                elif self.game.player.passive_equipped in [SHIELD, ARMOR]:
                                    self.game.bomb_exploding = True
                                    self.game.latest_player_state = self.game.player_state
                                    self.game.items[self.game.player.passive_equipped].health -= 1

                                    if self.game.items[self.game.player.passive_equipped].health == 0:
                                        self.game.player.passive_equipped = None
                                        self.game.player_state = PLAYER_STATES[(self.game.player.active_equipped, self.game.player.passive_equipped)]

                                    self.grid[cell][CELL_STATE] = NOT_HIDDEN

                                else:
                                    self.grid[cell][CELL_STATE] = NOT_HIDDEN
                                    self.display(cell)
                                    pygame.display.set_caption("Perdu")
                                    self.game.player_state = PLAYER_EXPLODE

                            self.display(cell)

                        else:
                            if not self.grid[cell][CELL_VALUE] in self.game.player.discovered_items:
                                self.game.player.discovered_items.append(self.grid[cell][CELL_VALUE])

                            self.grid[cell][CELL_STATE] = NOT_HIDDEN
                            self.display(cell)
                            self.not_hidden_cells += 1

                    else:
                        self.grid[cell][CELL_STATE] = NOT_HIDDEN
                        self.display(cell)

                        if self.game.player.active_equipped in [MAGNIFIER, BIONIC_GLASSES] and not self.game.is_first_click:
                            self.game.player.active_equipped = None

                        elif self.grid[cell][CELL_VALUE] == 0:
                            all_cells = self.get_all_cells_around(cell)

                            for temp_cell in all_cells:
                                if self.grid[temp_cell][CELL_STATE] == HIDDEN:
                                    self.cell_clicked(LEFT_CLICK, temp_cell, False)
                                    self.display(temp_cell)

                        if self.not_hidden_cells == self.safe_cells_number and not self.game.k_pressed:
                            pygame.display.set_caption("Gagné !")
                            # pygame.time.delay(2000)

                            self.game.items[JAMMER].amount += self.jammer_to_give_back
                            current_time = pygame.time.get_ticks() // 60 * 10
                            coins_earned = 2000 // int(current_time - self.game.initial_time) + self.game.round
                            self.game.items[COIN].amount += coins_earned
                            print(coins_earned)

                            if self.game.space_pressed:
                                self.game.round += 1
                                self.game.space_pressed = False

                            if self.game.round < 3:
                                self.game.run()

                            else:
                                self.game.is_trading = True
                                self.game.run()

                            # pygame.time.delay(1000)
                            # pygame.mixer.music.fadeout(1000)```

                else:
                    if self.game.player.active_equipped == MAGNIFIER:
                        pass

                    elif self.grid[cell][CELL_STATE] == NOT_HIDDEN and self.grid[cell][CELL_VALUE] < -1 and self.grid[cell][CELL_VALUE] != JAMMER:
                        self.game.items[self.grid[cell][CELL_VALUE]].picked()
                        self.grid[cell][IS_COLLECTED] = COLLECTED
                        # self.game.item_collected.play()
                        self.display(cell)

                    else:
                        # self.game.sweeping_sound.play()
                        if self.grid[cell][CELL_STATE] == NOT_HIDDEN and self.game.player.active_equipped == JAMMER:
                            self.jammer_to_give_back += 1
                            self.grid[cell][CELL_VALUE] = JAMMER
                            self.game.player.active_equipped = None
                            self.game.player_state = PLAYER_STATES[(self.game.player.active_equipped, self.game.player.passive_equipped)]
                            self.display(cell)

                        else:
                            all_cells = self.get_all_cells_around(cell)

                            for temp_cell in all_cells:
                                if self.grid[temp_cell][CELL_STATE] == HIDDEN:
                                    self.cell_clicked(LEFT_CLICK, temp_cell, False)

        elif button == RIGHT_CLICK:
            if self.grid[cell][CELL_STATE] == HIDDEN:
                self.grid[cell][CELL_STATE] = FLAGGED
                self.flag_to_place -= 1

                if self.grid[cell][CELL_VALUE] < -1:
                    self.items_flagged.append(cell)

                pygame.display.set_caption(f"Vous avez {self.flag_to_place} {'drapeau' if self.flag_to_place in [-1, 0, 1] else 'drapeaux'} à placer ! (manche {self.game.round})")
                self.display(cell)

            elif self.grid[cell][CELL_STATE] == FLAGGED:
                self.grid[cell][CELL_STATE] = HIDDEN
                self.flag_to_place += 1

                if self.grid[cell][CELL_VALUE] < -1:
                    self.items_flagged.pop(self.items_flagged.index(cell))

                pygame.display.set_caption(f"Vous avez {self.flag_to_place} {'drapeau' if self.flag_to_place in [-1, 0, 1] else 'drapeaux'} à placer ! (manche {self.game.round})")
                self.display(cell)

        for item in self.items_flagged:
            if self.is_circled(item):
                self.display(item)

    def debug(self):
        for cell in self.grid:
            if self.grid[cell][CELL_VALUE] < -1:
                self.grid[cell][IS_COLLECTED] = COLLECTED
                self.flag_to_place -= 1
                self.grid[cell][CELL_STATE] = NOT_HIDDEN
                self.game.items[self.grid[cell][CELL_VALUE]].picked()

                if not self.grid[cell][CELL_VALUE] in self.game.player.discovered_items:
                    self.game.player.discovered_items.append(self.grid[cell][CELL_VALUE])

            elif self.grid[cell][CELL_VALUE] == BOMB:
                self.grid[cell][CELL_STATE] = FLAGGED
                self.flag_to_place -= 1

            else:
                self.grid[cell][CELL_STATE] = NOT_HIDDEN

            self.display(cell)

        pygame.display.set_caption(f"Vous avez {self.flag_to_place} {'drapeau' if self.flag_to_place in [-1, 0, 1] else 'drapeaux'} à placer ! (manche {self.game.round})")

    def __str__(self) -> str:
        """
        Returns a string representation of the grid.

        Parameters
        ----------
        None

        Returns
        -------
        A string representation of the grid.
        """

        output = "┌" + "┬" .join([6 * "─"] * self.width) + "┐" + "\n"

        for h in range(self.height):
            row_output = ""

            for w in range(self.width):
                cell = self.grid[(w, h)]

                if cell[CELL_STATE] == NOT_HIDDEN:
                    row_output += f"|  {cell[CELL_VALUE]}   "

                elif cell[CELL_STATE] == HIDDEN:
                    if cell[CELL_VALUE] == BOMB:
                        row_output += "|  B   "

                    else:
                        row_output += f"| ({cell[CELL_VALUE]})  "

                elif cell[CELL_STATE] == FLAGGED:
                    if cell[CELL_VALUE] == BOMB:
                        row_output += "| [B]  "

                    else:
                        row_output += f"| [{cell[CELL_VALUE]}]  "

            output += row_output + "|" + "\n"
            if h < self.height - 1:
                output += "├" + "┼" .join([6 * "─"] * self.width) + "┤" + "\n"

        output += "└" + "┴" .join([6 * "─"] * self.width) + "┘" + "\n"

        return output

    def display(self, cell: tuple[int, int]):
        """
        Renders the grid on the screen.

        Parameters
        ----------
        cell : tuple[int, int]
            The coordinates of the cell to render.

        Returns
        -------
        None
        """
        if self.grid[cell][CELL_STATE] == FLAGGED:
            if self.grid[cell][CELL_VALUE] < -1 and self.is_circled(cell):
                image = pygame.transform.scale(pygame.image.load(f"sprites/blue_flag.png").convert_alpha(), (self.game.square_size, self.game.square_size))
                image_x = cell[0] * self.game.square_size + self.game.x_offset
                image_y = cell[1] * self.game.square_size + self.game.y_offset
                self.game.screen.blit(image, (image_x, image_y))

            else:
                animation = Spritesheet(f"sprites/flag_sheet.png", 4, 1, (self.game.square_size, self.game.square_size), 24)
                self.game.animations[(cell[0], cell[1] * 99.9/100)] = animation

        elif self.grid[cell][CELL_STATE] == NOT_HIDDEN:
            color = (229, 194, 159) if (cell[0] + cell[1]) % 2 == 0 else (215, 184, 153)
            pygame.draw.rect(self.game.screen, color,
                             pygame.Rect(cell[0] * self.game.square_size + self.game.x_offset,
                                         cell[1] * self.game.square_size + self.game.y_offset,
                                         self.game.square_size, self.game.square_size))

            if self.grid[cell][CELL_VALUE] < 0:
                if self.grid[cell][IS_COLLECTED] == NOT_COLLECTED:
                    if self.grid[cell][CELL_VALUE] in [JAMMER, BOMB]:
                        animation = Spritesheet(f"sprites/{ITEM_IMAGES[self.grid[cell][CELL_VALUE]]}.png", FRAME_AND_FPS_NUMBER[self.grid[cell][CELL_VALUE]][FRAME_NUMBER], 1, (self.game.square_size * 0.9, self.game.square_size * 0.9), 24)
                        self.game.animations[(cell[0], cell[1])] = animation

                    else:
                        image_name = ITEM_NAME[self.grid[cell][CELL_VALUE]]
                        animation = Spritesheet(f"sprites/{image_name}.png", FRAME_AND_FPS_NUMBER[self.grid[cell][CELL_VALUE]][FRAME_NUMBER], 1, ((self.game.square_size * 0.9, self.game.square_size * 0.9)), 1)
                        image = animation.get()
                        image_x = self.game.square_size // 35 + cell[0] * self.game.square_size + self.game.x_offset
                        image_y = self.game.square_size // 12 + cell[1] * self.game.square_size + self.game.y_offset
                        self.game.screen.blit(image, (image_x, image_y))

                else:
                    image = pygame.transform.scale(pygame.image.load(f"sprites/hole.png").convert_alpha(), (self.game.square_size, self.game.square_size))
                    image_x = cell[0] * self.game.square_size + self.game.x_offset
                    image_y = cell[1] * self.game.square_size + self.game.y_offset
                    self.game.screen.blit(image, (image_x, image_y))

            else:
                color = (229, 194, 159) if (cell[0] + cell[1]) % 2 == 0 else (215, 184, 153)
                pygame.draw.rect(self.game.screen, color,
                                pygame.Rect(cell[0] * self.game.square_size + self.game.x_offset,
                                            cell[1] * self.game.square_size + self.game.y_offset,
                                            self.game.square_size, self.game.square_size))

                if self.grid[cell][CELL_VALUE] > 0:
                    font_size = round(self.game.square_size * 80/100)
                    font = pygame.font.SysFont("Arial", font_size)
                    cell_value = str(self.grid[cell][CELL_VALUE])
                    image = font.render(cell_value, True,
                                        COLORS[self.grid[cell][CELL_VALUE]])
                    image_x = self.game.square_size // 3.5 + cell[0] * self.game.square_size + self.game.x_offset
                    image_y = self.game.square_size // 15 + cell[1] * self.game.square_size + self.game.y_offset
                    self.game.screen.blit(image, (image_x, image_y))

        elif self.grid[cell][CELL_STATE] == HIDDEN:
            del self.game.animations[(cell[0], cell[1] * 99.9/100)]

            color = (170, 215, 81) if (cell[0] + cell[1]) % 2 == 0 else (162, 209, 73)
            pygame.draw.rect(self.game.screen, color,
                             pygame.Rect(cell[0] * self.game.square_size + self.game.x_offset,
                                         cell[1] * self.game.square_size + self.game.y_offset,
                                         self.game.square_size, self.game.square_size))

    def is_circled(self, cell: tuple[int, int]):
        all_cells = self.get_all_cells_around(cell)
        good_cells = 0
        for cell in all_cells:
            if self.grid[cell][CELL_STATE] == NOT_HIDDEN or (self.grid[cell][CELL_STATE] == FLAGGED and self.grid[cell][CELL_VALUE] < 0):
                good_cells += 1

        if good_cells == len(all_cells):
            return True

        return False