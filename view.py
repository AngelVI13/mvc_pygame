import pygame
import model
from eventmanager import *


class GraphicalView(Listener):
    """Draws the model state onto the screen"""

    def __init__(self, event_manager, model_object):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model_object: Pointer to GameEngine: a strong reference to the game Model
        """
        super().__init__(event_manager)  # Register listener to event manager
        self.model = model_object
        self.initialized = False

        self.screen = None  # the screen surface
        self.clock: pygame.time.Clock = None  # keeps the fps constant
        self.small_font = None  # small font

    def notify(self, event):
        """Receive events posted to the message queue"""

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.initialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.initialized:
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
        text = self.small_font.render('You are in the Menu. Space to play. Esc exits.', True, (0, 255, 0))
        self.screen.blit(text, (0, 0))
        pygame.display.flip()  # todo move flip to notify() before clock.tick()?

    def render_play(self):
        """Render the game play."""
        self.screen.fill((0, 0, 0))
        text = self.small_font.render('You are playing the game. F1 for help.', True, (0, 255, 0))
        self.screen.blit(text, (0, 0))
        pygame.display.flip()

    def render_help(self):
        """Render the help screen"""
        self.screen.fill((0, 0, 0))
        text = self.small_font.render('Help is here. space, escape or return.', True, (0, 255, 0))
        self.screen.blit(text, (0, 0))
        pygame.display.flip()

    def initialize(self):
        """Set up the pygame graphical display and loads graphical resources"""
        pygame.init()
        pygame.font.init()  # todo ???
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((600, 60))  # todo store in vars
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 40)
        self.initialized = True
