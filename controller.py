import pygame
import model
from eventmanager import *


class Keyboard:
    """Handles keyboard input"""

    def __init__(self, event_manager, model):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model: Pointer to GameEngine: a strong reference to the game Model
        """
        self.event_manager = event_manager
        event_manager.RegisterListener(self)
        self.model = model

    def notify(self, event):
        """Receives events posted to the message queue"""

        if isinstance(event, TickEvent):
            # called for each game tick. We check our keyboard presses here
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.event_manager.Post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.event_manager.Post(StateChangeEvent(None))
                    else:
                        # todo use map instead of multiple ifs ?
                        current_state = self.model.state.peek()
                        if current_state == model.STATE_MENU:
                            self.keydown_menu(event)
                        if current_state == model.STATE_PLAY:
                            self.keydown_play(event)
                        if current_state == model.STATE_HELP:
                            self.keydown_help(event)

    def keydown_menu(self, event):
        """Handles menu key events."""

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))  # todo shady. not intuitive that this pops the state

        # space plays the game
        if event.key == pygame.K_SPACE:
            self.event_manager.Post(StateChangeEvent(model.STATE_PLAY))

    def keydown_help(self, event):
        """Handles help key events"""
        # space, enter or escape pops the help
        if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
            self.event_manager.Post(StateChangeEvent(None))

    def keydown_play(self, event):
        """Handles play key events"""
        if event.key == pygame.K_ESCAPE:
            self.event_manager.Post(StateChangeEvent(None))

        # F1 shows the help
        if event.key == pygame.K_F1:
            self.event_manager.Post(StateChangeEvent(model.STATE_HELP))
        else:
            self.event_manager.Post(InputEvent(event.unicode, None))
