import pygame

class Speech_bubble:
    """
    Manages the creation and display of text bubbles.
    """
    def __init__(self, game, speech: str):
        """
        Initialize the object.
        """
        self.game = game
        self.speech = speech
        self.bubble_image = pygame.image.load("sprites/bubble.png").convert_alpha()
        self.spike_image = pygame.image.load("sprites/spike.png").convert_alpha()

    def display(self):
        """
        Display the bubble with the text inside.
        """
        lenght = 0
        delay = 0
        speech_list = []
        new_speech = ""
        splited_speech = self.speech.split()
        is_speech_short = False

        if len(splited_speech) < 20:
            new_speech = self.speech
            speech_list.append(new_speech)
            is_speech_short = True

        else:
            for word in range(len(splited_speech)):
                lenght += len(splited_speech[word])

                if lenght <= 20:
                    new_speech += splited_speech[word] + " "
                    if len(splited_speech) - word <= 1:
                        speech_list.append(new_speech)

                else:
                    new_speech += splited_speech[word]
                    speech_list.append(new_speech)
                    lenght = 0
                    new_speech = ""

        index = -1
        maxi = len(speech_list[index])
        longer_element = speech_list[index]

        for i in range(len(speech_list)):
            index += 1
            if len(speech_list[i]) >= maxi:
                maxi = len(speech_list[index])
                longer_element = speech_list[index]

        font_size = round(self.game.square_size * 30 / 100)
        font = pygame.font.SysFont("Arial", font_size)
        text_image = font.render(longer_element, True, (0, 0, 0))
        width = text_image.get_width() * 1.2
        height = text_image.get_height() * 1.1 * len(speech_list)
        self.bubble_image = pygame.transform.smoothscale(self.bubble_image, (width, height))

        #if is_speech_short == True:
            #self.spike_image = pygame.transform.smoothscale(self.spike_image, (self.spike_image.get_width() * 95 / 100, self.spike_image.get_height() * 95 / 100))

        if is_speech_short:
            delay = 5000
        else:
            delay = 1600

        current_time = pygame.time.get_ticks()
        if current_time <= len(speech_list) * delay:

            if self.game.is_trading:
                bubble_position = (self.game.screen_width * 42 / 100 - self.bubble_image.get_width(), self.game.screen_height * 38 / 100 - self.bubble_image.get_height())
                spike_position = (self.game.screen_width * 42 / 100 - self.spike_image.get_width(), self.game.screen_height * 38 / 100)
                self.game.screen.blit(self.bubble_image, bubble_position)
                self.game.screen.blit(self.spike_image, spike_position)

                for t in range(len(speech_list)):
                    text_image = font.render(speech_list[t], True, (0, 0, 0))
                    text_position = (self.game.screen_width * 42 / 100 - self.bubble_image.get_width() * 95 / 100, self.game.screen_height * 38 / 100 - self.bubble_image.get_height() + t*text_image.get_height() + self.bubble_image.get_height() * 5 / 100)
                    self.game.screen.blit(text_image, text_position)

            else:
                bubble_position = (self.game.player.x - self.bubble_image.get_width() * 90 / 100, self.game.player.y - self.bubble_image.get_height() + self.game.gui_width * 1/2)
                spike_position = (self.game.player.x + self.bubble_image.get_width() * 10 / 100 - self.spike_image.get_width(), self.game.player.y + self.game.gui_width * 1/2)
                self.game.screen.blit(self.bubble_image, bubble_position)
                self.game.screen.blit(self.spike_image, spike_position)

                for t in range(len(speech_list)):
                    text_image = font.render(speech_list[t], True, (0, 0, 0))
                    text_position = (self.game.player.x - self.bubble_image.get_width() * 90 / 100 + self.bubble_image.get_width() * 5 / 100, self.game.player.y - self.bubble_image.get_height() + self.game.gui_width * 1/2 + t*text_image.get_height() + self.bubble_image.get_height() * 5 / 100)
                    self.game.screen.blit(text_image, text_position)

        else:
            pass