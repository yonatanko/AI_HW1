import search
import random
import math
import json

ids = ["212984801", "316111442"]


class TaxiProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""

        self.map = initial["map"]
        search.Problem.__init__(self, self.add_data_and_transform_to_json(initial))
        
    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        state = json.loads(state)  # transforming the state from json string to dictionary
        possible_actions = {}
        for taxi in state["taxis"].keys():
            # checking if the taxi can move in the grid
            if taxi["current_fuel"] > 0:
                possible_actions[taxi] = self.check_possible_grid_moves(taxi["location"], taxi)
            # checking if the taxi can pick up a passenger
            if taxi["current_capacity"] < taxi["capacity"]:
                possible_actions[taxi] = possible_actions[taxi] + self.check_if_contains_passenger(taxi["location"], state["passengers"], taxi)
            # checking if the taxi can drop off a passenger
            possible_actions[taxi] = possible_actions[taxi] + self.check_drop_off_passenger(taxi["location"], taxi["passengers"], taxi)






    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        return 0

    def h_1(self, node):
        """
        This is a simple heuristic
        """

    def h_2(self, node):
        """
        This is a slightly more sophisticated Manhattan heuristic
        """

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""

    def add_data_and_transform_to_json(self, initial):
        """
        adding data to the state and removing the map
        """""
        del(initial["map"])
        initial["taxis"]["passengers"] = []
        initial["taxis"]["current_fuel"] = initial["taxis"]["fuel"]
        initial["taxis"]["current_capacity"] = 0

        return json.dumps(initial)

    def check_possible_grid_moves(self, location, taxi_name):
        """
        check the possible moves in the grid
        """
        possible_moves = []
        x = location[0]
        y = location[1]
        if x > 0:
            possible_moves.append(("move", taxi_name, (x-1, y))) if self.map[x-1][y] != 'I' else None
        if x < len(self.map)-1:
            possible_moves.append(("move", taxi_name, (x+1, y))) if self.map[x+1][y] != 'I' else None
        if y > 0:
            possible_moves.append(("move", taxi_name, (x, y-1))) if self.map[x][y-1] != 'I' else None
        if y < len(self.map[0])-1:
            possible_moves.append(("move", taxi_name, (x, y+1))) if self.map[x][y+1] != 'I' else None

        return possible_moves

    def check_if_contains_passenger(self, location, passengers, taxi_name):
        """
        check if the location contains a passenger
        """
        passenger_actions = []
        for passenger in passengers.keys():
            if passenger["location"] == location:
                passenger_actions.append(("pick_up", taxi_name, passenger))
        return passenger_actions

    def check_drop_off_passenger(self, location, passengers_of_taxi, taxi_name, all_passengers):
        """
        check if the location contains a passenger
        """
        passenger_actions = []
        for passenger in passengers_of_taxi.keys():
            if all_passengers[passenger]["destination"] == location:
                passenger_actions.append(("drop_off", taxi_name, passenger))
        return passenger_actions






def create_taxi_problem(game):
    return TaxiProblem(game)

