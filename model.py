import pygame
from enum import Enum, auto

from eventmanager import *


class GameEngine(Listener):
    """
    Tracks the game state
    """

    def __init__(self, event_manager):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        """
        super().__init__(event_manager)  # Register listener to event manager
        # True while the engine is online. Changed via QuitEvent()
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        """Called by an event in the message queue."""
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            if event.state:
                # push a new state on the stack
                self.state.push(event.state)
                return

            # pop request
            # false if no more states are left
            if not self.state.pop():
                self.event_manager.post(QuitEvent())
                
    def run(self):
        """Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QUitEvent in notify()
        """
        self.running = True
        self.event_manager.post(InitializeEvent())
        # we push our first state to the stack
        # our menu is always the first game state
        # the game always starts from the main menu
        self.state.push(States.STATE_MENU)
        while self.running:
            new_tick = TickEvent()
            self.event_manager.post(new_tick)


class States(Enum):
    """
    State machine constants for the StateMachine class
    """
    STATE_INTRO = auto()
    STATE_MENU = auto()
    STATE_HELP = auto()
    STATE_ABOUT = auto()
    STATE_PLAY = auto()


class StateMachine:
    """Manages a stack-based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None,
    """

    def __init__(self):
        self.state_stack = []

    def peek(self):
        """Returns the current state without altering the stack.
        Returns None if the stack is empty
        """
        try:
            return self.state_stack[-1]
        except IndexError:
            return None  # empty stack

    def pop(self):
        """Remove the current state from the stack.
        Return true if there are any states in the stack else False.
        Returns None if the stack is empty.
        """
        try:
            self.state_stack.pop()
        except IndexError:
            return None
        else:
            # returns if there are any states
            # if the game is running there should
            # be always at least 1 state present
            return len(self.state_stack) > 0

    def push(self, state):
        """Push a new state onto the stack.
        Returns the pushed value
        """
        self.state_stack.append(state)
