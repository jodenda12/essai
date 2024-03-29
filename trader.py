"""
Projet démineur
Auteurs :   Mathis Bulka
            Samuel Cornier
            Léo Simon
            Sacha Trouvé

    Module trader: gestion du marchand
"""

import pygame

COIN =      -2
MAGNIFIER = -3
SHIELD =    -5
UPGRADER =  -6
RIFLE =     -10

TALK_START = ["Ah tiens quelqu'un, tu es bien vivant dis moi ?", 
    "Je vois tu viens donc de sortir d’un des tunnels les plus profonds de la ville-mine d’à côté après avoir entendu qu’elle allait être désaffectée.", 
    "Désolé, mais cela va bientôt faire trois mois que le processus est terminé, il semblerait qu’on ne t’ai pas prévenu.", 
    "Bon ce n'est pas important de toute façon, ça te dirait de jeter un coup d'oeil, j’ai quelques petits trucs à vendre et lorsque tu auras fini, tu pourra partir en suivant le panneau.", 
    "Toujours vivant, nous verrons si ça dure.", 
    "Tant mieux pour toi... et pour moi aussi car après tout tu es mon seul client, depuis la guerre et tout ça …", 
    "Passons aux choses sérieuses, que veux tu aujourd’hui ?", 
    "T’as entendu la nouvelle, apparemment les bombardements nucléaires sur les principales villes mondiales se sont arrêtés. Peut être que le conflit s’est calmé... ou peut être que tout le monde est mort !", 
    "C’est pas comme si cela nous concernait ici de toute façon.", 
    "Tu te rappelles quand je disais que tout le monde était mort en rigolant, et bien il semblerait... que ce soit finalement vrai, je ne croise plus un rat.", 
    "Tu te rends compte je pourrai être le dernier humain ? ! Bon, t'es encore là mais ça ne compte pas vraiment.", 
    "Mais bon t'imagines bien ce n’est pas la fin du monde qui arrêtera notre petit commerce, hein ?", 
    "Te revoilà, bonjour à toi et ton argent."]     
"""
TALK_START is the list of the first words of the trader in function of the round.
Index matching :
0 : round 3, first sentence
1 : round 3, second sentence
2 : round 3, third sentence
3 : round 3, fourth sentence
4 : round 4, first sentence
5 : round 4, second sentence
6 : round 4, third sentence
7 : round 5, first sentence
8 : round 5, second sentence
9 : round 5, third sentence
10 : round 6, first sentence
11 : round 6, second sentence
12 : round 6, third sentence
13 : after the round 6
"""

TALK_TRADE = ["On se souvient de la qualité bien plus longtemps que du prix.", 
    "Un excellent choix !", 
    "Tu te contente de ça ?", 
    "Allez encore un...", 
    "Que ce que tu fais encore là ?", 
    "Bon j'ai pas que ça à faire... Enfin si, mais dépêche-toi quand même."]
"""
TALK_TRADE is the list of the words of the trader that he can say, after a trade or after a long time.
Index matching :
0 : after a trade
1 : after a trade
2 : after a trade
3 : after a trade
4 : after a long time
5 : after a long time
"""

class Trader:
    """
    The Trader class represents the in-game trader that the player can visit to purchase items.

    Attributes:
        game (Game): a reference to the main game instance
        trader_image (pygame.Surface): the image of the trader
        sign_hovered_image (pygame.Surface): the image of the trader sign when hovered
        sign_rect (pygame.Rect): the rectangle of the trader sign
        magnifier_image (pygame.Surface): the image of the magnifier item
        magnifier_rect (pygame.Rect): the rectangle of the magnifier item
        shield_image (pygame.Surface): the image of the shield item
        shield_rect (pygame.Rect): the rectangle of the shield item
        upgrader_image (pygame.Surface): the image of the upgrader item
        upgrader_rect (pygame.Rect): the rectangle of the upgrader item
    """
    def __init__(self, game):
        self.game = game
        self.trader_image = pygame.image.load(f"sprites/trader.png").convert_alpha()
        self.trader_image = pygame.transform.scale(self.trader_image, (self.game.screen_width - self.game.gui_width, self.game.screen_height))

        self.sign_hovered_image = pygame.image.load(f"sprites/sign_hovered.png").convert_alpha()
        self.sign_hovered_image = pygame.transform.scale(self.sign_hovered_image, (self.trader_image.get_width() * 22/100,
                                                                                   self.trader_image.get_height() * 20/100))

        self.sign_rect = self.sign_hovered_image.get_rect()
        self.sign_rect.x = self.game.screen_width - self.game.gui_width - self.trader_image.get_width() * 26.5/100
        self.sign_rect.y = self.game.screen_height - self.trader_image.get_height() * (102*100 / 360)/100

        self.trader_rect = pygame.Rect(0, 0, self.trader_image.get_width() * (91*100 / 600) / 100, self.trader_image.get_height() * (145*100 / 360) / 100)

        size = self.game.screen_width * 7.5 / 100
        y = self.game.screen_height / 2 + self.game.screen_height * 13 / 100

        self.magnifier_image = self.game.items[MAGNIFIER].image.copy()
        self.magnifier_image = pygame.transform.scale(self.magnifier_image, (size, size))
        self.magnifier_rect = self.magnifier_image.get_rect()
        self.magnifier_rect.x = ((self.game.screen_width - self.game.gui_width)/2 - self.game.screen_width * (1 + 14) / 100) - (self.magnifier_image.get_width() / 2)
        self.magnifier_rect.y = y

        self.shield_image = self.game.items[SHIELD].image.copy()
        self.shield_image = pygame.transform.scale(self.shield_image, (size, size))
        self.shield_rect = self.shield_image.get_rect()
        self.shield_rect.x = ((self.game.screen_width - self.game.gui_width)/2 - self.game.screen_width * 2.6 / 100) - (self.shield_image.get_width() / 2)
        self.shield_rect.y = y

        self.upgrader_image = self.game.items[UPGRADER].image.copy()
        self.upgrader_image = pygame.transform.scale(self.upgrader_image, (size, size))
        self.upgrader_image = pygame.transform.flip(self.upgrader_image, True, False)
        self.upgrader_rect = self.upgrader_image.get_rect()
        self.upgrader_rect.x = ((self.game.screen_width - self.game.gui_width)/2 - self.game.screen_width * (4 - 14) / 100) - (self.upgrader_image.get_width() / 2)
        self.upgrader_rect.y = y

    def display(self):
        """
        Draws the trader and his items on the screen.
        """
        item_y = self.game.screen_height - self.trader_image.get_height()
        self.game.screen.blit(self.trader_image, (0, 0))
        self.game.screen.blit(self.magnifier_image, (self.magnifier_rect.x, self.magnifier_rect.y))
        self.game.screen.blit(self.shield_image, (self.shield_rect.x, self.shield_rect.y))
        self.game.screen.blit(self.upgrader_image, (self.upgrader_rect.x, self.upgrader_rect.y))

    def sign_hovered(self):
        """
        Returns True if the trader sign is hovered, False otherwise.
        """
        if self.sign_rect.collidepoint(pygame.mouse.get_pos()):
            self.game.screen.blit(self.sign_hovered_image, (self.sign_rect.x, self.sign_rect.y))
            return True

        return False

    def handling_events(self):
        """
        Handles events related to the trader and his items.
        """
        if self.sign_hovered():
            self.game.is_trading = False
            self.game.run()

        elif self.magnifier_rect.collidepoint(pygame.mouse.get_pos()):# and self.game.items[COIN].amount >= 0:
            self.game.items[COIN].amount -= 10
            self.game.items[MAGNIFIER].picked()
            # self.game.item_collected.play()

        elif self.shield_rect.collidepoint(pygame.mouse.get_pos()):# and self.game.items[COIN].amount >= 0:
            self.game.items[COIN].amount -= 10
            self.game.items[SHIELD].picked()
            # self.game.item_collected.play()

        elif self.upgrader_rect.collidepoint(pygame.mouse.get_pos()):# and self.game.items[COIN].amount >= 0:
            self.game.items[COIN].amount -= 10
            self.game.items[UPGRADER].picked()
            # self.game.item_collected.play()

        elif self.trader_rect.collidepoint(pygame.mouse.get_pos()) and self.game.player.active_equipped == RIFLE:
            self.game.is_trader_dead = True