import pygame
import model
from eventmanager import *


class Keyboard(Listener):
    """Handles keyboard input"""

    def __init__(self, event_manager, model_object):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model_object: Pointer to GameEngine: a strong reference to the game Model
        """
        super().__init__(event_manager)  # Register listener to event manager
        self.model = model_object

        self.keydown_state_map = {
            model.STATE_MENU: self.keydown_menu,
            model.STATE_HELP: self.keydown_help,
            model.STATE_PLAY: self.keydown_play,
        }

    def notify(self, event):
        """Receives events posted to the message queue"""

        if not isinstance(event, TickEvent):
            return

        # called for each game tick. We check our keyboard presses here
        for event in pygame.event.get():
            # handle window manager closing our window
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())
            # handle key down events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.event_manager.post(StateChangeEvent(None))
                else:
                    current_state = self.model.state.peek()

                    try:
                        handler = self.keydown_state_map[current_state]
                    except KeyError:
                        raise Exception(f"Unknown state: {current_state}. No handling defined for state.")
                    else:
                        handler(event)

    def keydown_menu(self, event):
        """Handles menu key events."""

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))  # todo shady. not intuitive that this pops the state

        # space plays the game
        if event.key == pygame.K_SPACE:
            self.event_manager.post(StateChangeEvent(model.STATE_PLAY))

    def keydown_help(self, event):
        """Handles help key events"""
        # space, enter or escape pops the help
        if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
            self.event_manager.post(StateChangeEvent(None))

    def keydown_play(self, event):
        """Handles play key events"""
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))

        # F1 shows the help
        if event.key == pygame.K_F1:
            self.event_manager.post(StateChangeEvent(model.STATE_HELP))
        else:
            self.event_manager.post(InputEvent(event.unicode, None))
