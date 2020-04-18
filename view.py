from typing import Tuple

import pygame
from model import GameEngine, States
from eventmanager import *


class GraphicalView(Listener):
    """Draws the model state onto the screen"""

    def __init__(
        self,
        event_manager: EventManager,
        model_object: GameEngine,
        win_size: Tuple[int, int] = (600, 400),
        win_title: str = "Application",
        fps: int = 30,
    ):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model_object: Pointer to GameEngine: a strong reference to the game Model
        @param win_size: Tuple containing window wight and height
        @param win_title: Window title text
        @param fps: Frames per second
        """
        super().__init__(event_manager)  # Register listener to event manager
        self.model = model_object
        self.window_size = win_size
        self.window_title = win_title
        self.fps = fps

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
            # only draw on tick events and when initialized
            if not self.initialized:
                return

            current_state = self.model.state.peek()
            if current_state == States.STATE_MENU:
                self.render_menu()
            if current_state == States.STATE_PLAY:
                self.render_play()
            if current_state == States.STATE_HELP:
                self.render_help()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(self.fps)

    def render_menu(self):
        """Render the game menu"""
        self.screen.fill(pygame.Color("black"))  # todo color constant
        text = self.small_font.render(
            "You are in the Menu. Space to play. Esc exits.", True, (0, 255, 0)
        )
        self.screen.blit(text, (0, 0))
        pygame.display.flip()  # todo move flip to notify() before clock.tick()?

    def render_play(self):
        """Render the game play."""
        self.screen.fill(pygame.Color("black"))
        text = self.small_font.render(
            "You are playing the game. F1 for help.", True, pygame.Color("green")
        )
        self.screen.blit(text, (0, 0))

        pygame.display.flip()

    def render_help(self):
        """Render the help screen"""
        self.screen.fill(pygame.Color("black"))
        text = self.small_font.render(
            "Help is here. space, escape or return.", True, pygame.Color("green")
        )
        self.screen.blit(text, (0, 0))
        pygame.display.flip()

    def initialize(self):
        """Set up the pygame graphical display and loads graphical resources"""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.window_title)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 30)
        self.initialized = True
