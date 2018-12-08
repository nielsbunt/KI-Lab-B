# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # stack[0] = problem
    # stack[1] = pad naar huidige situatie
    stack = util.Stack()
    stack.push((problem.getStartState(), []))
    closed = []

    # zolang er nog opties zijn: ...
    while not stack.isEmpty():
        top = stack.pop()
        # return het pad naar deze locatie als het het doel is
        if problem.isGoalState(top[0]):
            return top[1]

        # zoek anders verder in alle vertakkingen (en geef aan dat deze locatie al bekeken is)
        if top[0] not in closed:
            closed.append(top[0])

            for p in problem.getSuccessors(top[0]):
                stack.push((p[0], top[1] + [p[1]]))

    # alle opties zijn bekeken, er is geen oplossing -> doe niks
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # queue[0] = problem
    # queue[1] = pad naar huidige situatie
    queue = util.Queue()
    queue.push((problem.getStartState(), []))
    closed = []

    # zolang er nog opties zijn: ...
    while not queue.isEmpty():
        top = queue.pop()
        # return het pad naar deze locatie als het het doel is
        if problem.isGoalState(top[0]):
            return top[1]

        # zoek anders verder in alle vertakkingen (en geef aan dat deze locatie al bekeken is)
        if top[0] not in closed:
            closed.append(top[0])

            for p in problem.getSuccessors(top[0]):
                queue.push((p[0], top[1] + [p[1]]))

    # alle opties zijn bekeken, er is geen oplossing -> doe niks
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(), []), 0)
    closed = []

    # zolang er nog opties zijn: ...
    while not pqueue.isEmpty():
        cheapest = pqueue.pop()
        # return het pad naar deze locatie als het het doel is
        if problem.isGoalState(cheapest[0]):
            return cheapest[1]

        # zoek anders verder in alle vertakkingen (en geef aan dat deze locatie al bekeken is)
        if cheapest[0] not in closed:
            closed.append(cheapest[0])

            for p in problem.getSuccessors(cheapest[0]):
                pqueue.update((p[0], cheapest[1] + [p[1]]), problem.getCostOfActions(cheapest[1] + [p[1]]))

    # alle opties zijn bekeken, er is geen oplossing -> doe niks
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def f((state, path)):
        return problem.getCostOfActions(path) + heuristic(state, problem)

    # pqueue[0] = problem
    # pqueue[1] = pad naar huidige situatie
    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(), []), 0)
    closed = []

    # zolang er nog opties zijn: ...
    while not pqueue.isEmpty():
        best = pqueue.pop()
        # return het pad naar deze locatie als het het doel is
        if problem.isGoalState(best[0]):
            return best[1]

            # zoek anders verder in alle vertakkingen (en geef aan dat deze locatie al bekeken is)
        if best[0] not in closed:
            closed.append(best[0])

            for p in problem.getSuccessors(best[0]):
                item = (p[0], best[1] + [p[1]])
                pqueue.push(item, f(item))

    # alle opties zijn bekeken, er is geen oplossing -> doe niks
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
