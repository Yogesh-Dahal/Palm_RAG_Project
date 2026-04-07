def route(state):
    return "booking" if state["intent"] == "booking" else "qa"
