from ex2 import StateMachine, Event, State


class E_on(Event):

    def __init__(self, data):
        super().__init__(data)
        pass


class E_off(Event):

    def __init__(self, data):
        super().__init__(data)
        pass


class E_random(Event):

    def __init__(self, data):
        super().__init__(data)
        pass


class S_initial(State):

    def __init__(self):
        self.is_initial = True


class S_off(State):
    pass


class S_on(State):
    pass


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


def test_state_machine():

    fsm_name = "example_FSM"
    sm1 = StateMachine(fsm_name)
    s_initial = S_initial()
    s_on = S_on()
    s_off = S_off()
    e_on = E_on("data1=3,data2=4")
    e_off = E_off("data1=3,data2=4")
    e_random = E_random("")

    """
    init ------ turn_on ----> on
    on ----- turn_off ----> off
    off ---- turn_on -----> on
    """
    sm1.add([s_initial, E_on, s_on, on_action])
    sm1.add([s_off, E_on, s_on, off_action])
    # redundant state transitions
    sm1.add([s_on, E_on, s_on, null_action])
    sm1.add([s_off, E_off, s_off, null_action])

    # TODO! There is a bug here in how the transition dict is built.  the ordering of the add matters. (it shouldn't)
    # s_on, e_on
    # s_on, e_off
    # s_off, e_on
    sm1.add([s_on, E_off, s_off, off_action])
    sm1.set_initial_state(s_initial)

    sm1.draw(output=f"/var/tmp/{fsm_name}.pdf")
    sm1.fire(e_on)
    sm1.fire(e_random)
    sm1.fire(e_off)
