"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module gui: gestion de l'affichage du plateau de jeu
"""

import pygame

class Gui:
    """
    The Gui class is responsible for managing the display of the game GUI,
    including the game menu, inventory, and HUD elements.

    Parameters:
    game (Game): The Game instance that this GUI is associated with.
    gui_width (int): The width of the GUI in pixels.

    Attributes:
    game (Game): The Game instance that this GUI is associated with.
    color (tuple): The color of the GUI background.
    gui_width (int): The width of the GUI in pixels.
    offset_y (int): The vertical offset of the GUI.
    """

    def __init__(self, game, gui_width):
        self.game = game
        self.color = (135, 135, 135)
        self.gui_width = gui_width + 1
        self.offset_y = self.game.screen_height * 1/100

    def display(self):
        """
        Draw the GUI on the screen.
        """
        pygame.draw.rect(self.game.screen, self.color,
             pygame.Rect(self.game.screen_width - self.gui_width,
                         0,
                         self.gui_width, self.game.screen_height))


class Button(pygame.sprite.Sprite):
    """
    A button that can be added to the game screen.

    Parameters:
    game (Game): The game instance that the button is associated with.
    x (int): The x-coordinate of the top-left corner of the button.
    y (int): The y-coordinate of the top-left corner of the button.
    color (tuple): The color of the button's border.
    text (str): The text that appears on the button.
    text_color (tuple): The color of the text on the button.
    font_size (int): The font size of the text on the button.

    Attributes:
    game (Game): The game instance that the button is associated with.
    x (int): The x-coordinate of the top-left corner of the button.
    y (int): The y-coordinate of the top-left corner of the button.
    text (str): The text that appears on the button.
    text_color (tuple): The color of the text on the button.
    font_size (int): The font size of the text on the button.
    original_image (Surface): The image of the button without hover effects.
    hovered_image (Surface): The image of the button with hover effects.
    image (Surface): The current image of the button, depending on hover state.
    rect (Rect): The bounding rectangle of the button's image.
    """

    def __init__(self, game, x: int, y: int, color: tuple[int, int, int],
                 text: str, text_color: tuple[int, int, int], font_size: int):
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.game.buttons.add(self)

        self.original_image = self.create_button_image(color, font_size, 11)
        hovered_color = tuple(value + 20 if value <= 235 else 0 for value in color)
        self.hovered_image = self.create_button_image(hovered_color,
                                                      font_size + 1, 12)

        self.image = self.original_image

    def create_button_image(self, color, font_size, value):
        """
        Create the image of the button.

        Parameters:
        color (tuple): The color of the button's border.
        font_size (int): The font size of the text on the button.
        border_width (int): The width of the border around the button.

        Returns:
        Surface: The image of the button.
        """

        font = pygame.font.SysFont("Arial", font_size)
        image = font.render(self.text, True, self.text_color)

        self.rect = image.get_rect()
        self.rect.width += value
        self.rect.height += value
        self.rect.center = (self.game.screen_width, self.rect.height / 2)

        background = pygame.Surface((self.rect.width, self.rect.height))
        background.fill(color)
        background.get_rect(center = self.rect.center)
        text_rect = image.get_rect(center = background.get_rect().center)

        background.blit(image, text_rect.topleft)

        return background

    def update(self):
        """
        Update the button's state based on the mouse position.

        If the mouse is hovering over the button, the hovered_image is displayed.
        If the left mouse button is pressed and the button is not currently active,
        the button is activated and the print("Pressed") statement is executed.
        """

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.hovered_image

            if pygame.mouse.get_pressed()[0]:
                print("Pressed")

        else:
            self.image = self.original_image