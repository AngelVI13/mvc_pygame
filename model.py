import pygame
from eventmanager import *


class GameEngine:
    """
    Tracks the game state
    """

    def __init__(self, event_manager):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        """
        self.event_manager = event_manager
        event_manager.RegisterListener(self)
        # True while the engine is online. Changed via QuitEvent()
        self.running = False
        self.state = StateMachine()

    def notify(self, event):
        """Called by an event in the message queue."""
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.event_manager.Post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

    def run(self):
        """Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QUitEvent in notify()
        """
        self.running = True
        self.event_manager.Post(InitializeEvent())
        # we push our first state to the stack
        # we out menu is always the first game state
        # the game always starts from the main menu
        self.state.push(STATE_MENU)
        while self.running:
            new_tick = TickEvent()
            self.event_manager.Post(new_tick)


# State machine constants for the StateMachine class below
STATE_INTRO = 1
STATE_MENU = 2
STATE_HELP = 3
STATE_ABOUT = 4
STATE_PLAY = 5


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
        return state  # todo ???