import ex1
import search
import time
import ex1_testing
from dataclasses import dataclass, field
import pprint
import sys


def timeout_exec(func, args=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default

        def run(self):
            # try:
            self.result = func(*args, **kwargs)
            # except Exception as e:
            #    self.result = (-3, -3, e)

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.is_alive():
        return default
    else:
        return it.result


def check_problem(p, search_method, timeout):
    """ Constructs a problem using ex1.create_wumpus_problem,
    and solves it using the given search_method with the given timeout.
    Returns a tuple of (solution length, solution time, solution)"""

    """ (-2, -2, None) means there was a timeout
    (-3, -3, ERR) means there was some error ERR during search """

    t1 = time.time()
    s = timeout_exec(search_method, args=[p], timeout_duration=timeout)
    t2 = time.time()

    if isinstance(s, search.Node):
        solve = s
        solution = list(map(lambda n: n.action, solve.path()))[1:]
        return (len(solution), t2 - t1, solution)
    elif s is None:
        return (-2, -2, None)
    else:
        return s


def solve_problems(problems, type_of_h):
    solved = 0
    for problem in problems:
        try:
            p = ex1_testing.create_taxi_problem(problem, type_of_h)
        except Exception as e:
            print("Error creating problem: ", e)
            return None
        timeout = 600
        result = check_problem(p, (lambda p: search.astar_search(p, p.h)), timeout)
        print("A*: ", result)
        if result[2] != None:
            if result[0] != -3:
                solved = solved + 1
        else:
            break


def main(type_of_h, first):
    printer = pprint.PrettyPrinter()
    if first:
        print(ex1.ids)
    """Here goes the input you want to check"""
    problems = [

        {
            "map": [['P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P'],
                    ['P', 'I', 'G', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "taxis": {'taxi 1': {"location": (3, 3),
                                 "fuel": 15,
                                 "capacity": 2}},

            "passengers": {'Yossi': {"location": (0, 0),
                                     "destination": (2, 3)},
                           'Moshe': {"location": (3, 1),
                                     "destination": (0, 0)}
                           }
        },

        {
            "map": [['P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P'],
                    ['P', 'I', 'G', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "taxis": {'taxi 1': {"location": (3, 3),
                                 "fuel": 15,
                                 "capacity": 2},
                      'taxi 2': {"location": (3, 1),
                                 "fuel": 15,
                                 "capacity": 2}},
            "passengers": {'Dana': {"location": (0, 0),
                                    "destination": (2, 3)},
                           'Yael': {"location": (3, 1),
                                    "destination": (0, 0)},
                           'Yori': {"location": (1, 0),
                                    "destination": (1, 3)}
                           }

        },
    ]
    if first:
        print("Problems:")
        printer.pprint(problems)

    print()
    print("Solving problems with h = ", type_of_h)
    solve_problems(problems, type_of_h)


if __name__ == '__main__':
    # sys.stdout = open('output.txt', 'w')
    # main("euclidean", True)
    # main("manhattan", False)
    main("h_2", True)
    # main("h_1", False)
    # main("max of h_1 and h_2", False)
    # main("max of euclidean and manhattan", False)
    # main("zero", False)
    # sys.stdout.close()
