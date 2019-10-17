# todo poor OOP structure
class Event:
    """A superclass for any events that might be generated by an
    object and sent to the EventManager.
    """

    def __init__(self):
        self.name = "Generic event"

    def __str__(self):
        return self.name


class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit event"


class TickEvent(Event):
    def __init__(self):
        self.name = "Tick event"


class InputEvent(Event):
    """Keyboard or mouse input event"""

    def __init__(self, unicode_char, click_pos):
        self.name = "Input event"
        self.char = unicode_char
        self.click_pos = click_pos

    def __str__(self):
        return f"{self.name}, char={self.char}, clickpos={self.click_pos}"


class InitializeEvent(Event):
    """Tells all listeners to initialize themselves.
    This includes loading libraries and resources.

    Avoid initializing such things within listener __init__ calls
    to minimize snafus todo ???
    (if some rely on others being yet created)
    """
    def __init__(self):
        self.name = "Initialize event"


class StateChangeEvent(Event):
    """Change the model state machine.
    Given a None state will pop() instead of push
    """
    def __init__(self, state):
        self.name = "State change event"
        self.state = state

    def __str__(self):
        if self.state:
            return f'{self.name} pushed {self.state}'
        else:
            return f'{self.name} popped'


class EventManager:
    """
    Coordinates the communication between the Model, View and Controller
    """
    def __init__(self):
        # todo local import ?
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        """Adds a listener to our spam list
        It will receive Post()ed events through its notify(event) call
        """

        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        """Remove a listener from our spam list.
        This is implemented byt hardly used.
        Our weak ref spam list will auto remove any listener who stops existing
        """
        if listener in self.listeners.keys():
            del self.listeners[listener]

    def Post(self, event):
        if not isinstance(event, TickEvent):
            # print the event (unless it is TickEvent)
            print(str(event))

        # todo is .keys() needed
        for listener in self.listeners.keys():
            listener.notify(event)
