# Sep 5, 2024
import pygraphviz as pgv

debug = False


class NoState(Exception):
    pass


# callable classes
class Event(object):

    def __init__(self, data):
        self.data = data
        pass

    def __str__(self):
        return f"Event Type: {type(self)} data: {self.data}"


class State(object):

    is_initial = False

    def __init__(self):
        pass

    def add_event_handler(self, event):
        self.event_handler.append(event)


class S_initial(State):

    def __init__(self):
        self.is_initial = True


class S_off(State):
    pass


class S_on(State):
    pass


# state machine:
class StateMachine(object):

    def __init__(self, name):
        self.transitions = []
        self.dict_transition = {}
        self.name = name
        self.current_state = None
        pass

    def set_initial_state(self, state):
        self.current_state = state

    def add(self, transition):
        self.transitions.append(transition)

    def build_dict(self):
        for state, event, next_state, handler in self.transitions:
            self.dict_transition[state] = {}
            self.dict_transition[state][event] = [handler, next_state]
        if debug:
            print(self.dict_transition)

    def fire(self, event: Event):
        """
        Fire event into the machine.
        Depending on the state, the event may be handled or not.
        """
        print("\n=====Firing")
        if len(self.dict_transition.keys()) == 0:
            self.build_dict()

        event_type = type(event)
        table_entry = self.dict_transition.get(self.current_state, None)
        if table_entry is None:
            raise NoState(f"Internal error.  There is no state {self.current_state}")

        event_found = table_entry.get(event_type, None)
        if event_found:
            handler = event_found[0]
        else:
            print(
                f"there is no event type {event_type} defined for state {self.current_state}\nEvent = {event}"
            )
            return None

        result = handler(event)
        if result:
            next_state = table_entry.get(event_type)[1]
            if self.current_state != next_state:
                print(f"changing state from {self.current_state} to {next_state}")
                self.current_state = next_state
            else:
                print("no state change")

    def draw(self, output):
        """graphviz"""
        state_transitions = []
        initial_state_names = []
        for from_state, event, to_state, _ in self.transitions:
            if from_state.is_initial:
                initial_state_names.append(type(from_state).__name__)
            state_transitions.append(
                f"{type(from_state).__name__} -> "
                f"{type(to_state).__name__} "
                f'[label = "{event.__name__}"];'
            )
        state_transitions = "\n".join(state_transitions)
        print(f"inits {initial_state_names}")
        initial_state_names = " ".join(initial_state_names) + ";"

        gvz_commands = (
            f"""digraph {self.name} """
            + """{
                        fontname="Helvetica,Arial,sans-serif"
                        node [fontname="Helvetica,Arial,sans-serif"]
                        edge [fontname="Helvetica,Arial,sans-serif"]
                        rankdir=LR;"""
            + f"""
                        node [shape = doublecircle]; {initial_state_names}
                        node [shape = circle];
                        {state_transitions}
                        """
            + "}"
        )

        G = pgv.AGraph(gvz_commands)
        G.draw(output, prog="dot")


def off_action(event):
    print(f"On event: {event}")
    print(f"Result: OFF")
    return True


def on_action(event):
    print(f"On event: {event}")
    print(f"Result: ON")
    return True


def null_action(event):
    print(f"On event: {event}")
    print(f"Result: do nothing")
    return True
