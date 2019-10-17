import pygame
import model
from eventmanager import *


class GraphicalView:
    """Draws the model state onto the screen"""

    def __init__(self, event_manager, model):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model: Pointer to GameEngine: a strong reference to the game Model
        """
        self.event_manager = event_manager
        event_manager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        # todo type hints ??
        self.screen: pygame.Surface = None  # the screen surface
        self.clock: pygame.time.Clock = None  # keeps the fps constant
        self.small_font: pygame.font.Font = None  # small font

    def notify(self, event):
        """Receive events posted to the message queue"""

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return

            current_state = self.model.state.peek()
            if current_state == model.STATE_MENU:
                self.render_menu()
            if current_state == model.STATE_PLAY:
                self.render_play()
            if current_state == model.STATE_HELP:
                self.render_help()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

    def render_menu(self):
        """Render the game menu"""
        self.screen.fill((0, 0, 0))  # todo color constant
        somewords = self.small_font.render('You are in the Menu. Space to play. Esc exits.', True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()  # todo move flip to notify() before clock.tick()?

    def render_play(self):
        """Render the game play."""
        self.screen.fill((0, 0, 0))
        somewords = self.small_font.render('You are playing the game. F1 for help.', True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

    def render_help(self):
        """Render the help screen"""
        self.screen.fill((0, 0, 0))
        somewords = self.small_font.render('Help is here. space, escape or return.', True, (0, 255, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

    # def render_all(self):
    #     """Draw the current game state on screen.
    #     Does nothing is isinitialized is False
    #     """
    #
    #     if not self.isinitialized:
    #         return
    #
    #     # clear display
    #     self.screen.fill((0, 0, 0))
    #     # draw some words on the screen
    #     somewords = self.small_font.render('The View is busy drawing on your screen', True, (0, 255, 0))
    #     self.screen.blit(somewords, (0, 0))
    #     # flip the display to show whatever we drew
    #     pygame.display.flip()

    def initialize(self):
        """Set up the pygame graphical display and loads graphical resources"""
        pygame.init()
        pygame.font.init()  # todo ???
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((600, 60))  # todo store in vars
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 40)
        self.isinitialized = True
