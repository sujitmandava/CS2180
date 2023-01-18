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
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    from util import Stack
    # Initializing frontier and expanded nodes list
    dfsFrontierList = Stack()
    dfsExploredList = []

    # Path from start to goal state
    dfsSolution = []

    # Path from start state to current node; This will be the solution when currentState = Goal
    dfsPath = Stack()

    # Setting initial parameters for the problem; Appending start state to frontier list
    currentState = problem.getStartState()

    """
    The algorithm is designed such that for each state that is pushed into the frontier list, the actions taken to reach that state
    are pushed at the same index in the form of a list.
    The loop terminates when the popped state is a goal state; The corresponding list of actions is a goal state and hence is popped
    and saved as the final solution.
    For Depth-First Search, the exploration follows a LIFO approach; Thus, the frontier list is implemented as a stack data structure
    """

    while(not problem.isGoalState(currentState)):

        # If state is already explored and is not a goal state, it indicates that we encountered a loop;
        # No need to further add the successors to the frontier list

        if currentState not in dfsExploredList:
            dfsExploredList.append(currentState)
            successors = problem.getSuccessors(currentState)

            for successor, action, cost in successors:
                dfsFrontierList.push(successor)
                # Temp variable used to push the whole list of actions taken to reach a particular successor;
                path = dfsSolution[:]
                path.append(action)
                dfsPath.push(path)

        currentState = dfsFrontierList.pop()
        dfsSolution = dfsPath.pop()

    return dfsSolution


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    # Initializing frontier and expanded nodes list
    bfsFrontierList = Queue()
    bfsExploredList = []

    # Path from start to goal state
    bfsSolution = []

    # Path from start state to current node; This will be the solution when currentState = Goal
    bfsPath = Queue()

    # Setting initial parameters for the problem; Appending start state to frontier list
    currentState = problem.getStartState()
    """
    The algorithm is designed such that for each state that is pushed into the frontier list, the actions taken to reach that state
    are pushed at the same index in the form of a list.
    The loop terminates when the popped state is a goal state; The corresponding list of actions is a goal state and hence is popped
    and saved as the final solution.
    For Breadth-First Search, the exploration follows a FIFO approach; Thus, the frontier list is implemented as a queue data structure
    """

    while(not problem.isGoalState(currentState)):

        # If state is already explored and is not a goal state, it indicates that we encountered a loop;
        # No need to further add the successors to the frontier list

        if currentState not in bfsExploredList:
            bfsExploredList.append(currentState)
            successors = problem.getSuccessors(currentState)

            for successor, action, cost in successors:
                bfsFrontierList.push(successor)
                # Temp variable used to push the whole list of actions taken to reach a particular successor;
                path = bfsSolution[:]
                path.append(action)
                bfsPath.push(path)

        currentState = bfsFrontierList.pop()
        bfsSolution = bfsPath.pop()

    return bfsSolution
    # util.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # Initializing frontier and expanded nodes list

    ufcFrontierList = PriorityQueue()
    ufcExploredList = []

    # Path from start to goal state
    ufcSolution = []

    # Path from start state to current node; This will be the solution when currentState = Goal
    # Priority Queue is in the same order
    ufcPath = PriorityQueue()

    # Setting initial parameters for the problem; Appending start state to frontier list
    currentState = problem.getStartState()

    """
    The algorithm is designed such that for each state that is pushed into the frontier list, the actions taken to reach that state
    are pushed at the same index in the form of a list.
    The loop terminates when the popped state is a goal state; The corresponding list of actions is a goal state and hence is popped
    and saved as the final solution.
    For Uniform Cost Search, the states with equal cost to explore are explored first, before moving to states that are further away;
    Thus, the frontier list is implemented using a priority queue, whose priority order is defined by the cost of the actions taken
    to reach a particular state.
    """

    while(not problem.isGoalState(currentState)):

        # If state is already explored and is not a goal state, it indicates that we encountered a loop;
        # No need to further add the successors to the frontier list

        if currentState not in ufcExploredList:
            ufcExploredList.append(currentState)
            successors = problem.getSuccessors(currentState)

            for successor, action, cost in successors:
                # Temp variable used to push the whole list of actions taken to reach a particular successor;
                path = ufcSolution[:]
                path.append(action)
                # The queues of both the frontier list and the path associated with each node are both in the order of the cost associated
                # with the path; Hence, the order will be maintained
                ufcFrontierList.push(successor, problem.getCostOfActions(path))
                ufcPath.push(path, problem.getCostOfActions(path))

        currentState = ufcFrontierList.pop()
        ufcSolution = ufcPath.pop()

    return ufcSolution
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # Initializing frontier and expanded nodes list

    ufcFrontierList = PriorityQueue()
    ufcExploredList = []

    # Path from start to goal state
    ufcSolution = []

    # Path from start state to current node; This will be the solution when currentState = Goal
    # Priority Queue is in the same order
    ufcPath = PriorityQueue()

    # Setting initial parameters for the problem; Appending start state to frontier list
    currentState = problem.getStartState()

    """
    The algorithm is designed such that for each state that is pushed into the frontier list, the actions taken to reach that state
    are pushed at the same index in the form of a list.
    The loop terminates when the popped state is a goal state; The corresponding list of actions is a goal state and hence is popped
    and saved as the final solution.
    For Uniform Cost Search, the states with equal cost to explore are explored first, before moving to states that are further away;
    Thus, the frontier list is implemented using a priority queue, whose priority order is defined by sum of the cost of the actions taken
    to reach a particular state and the heuristic.
    """

    while(not problem.isGoalState(currentState)):

        # If state is already explored and is not a goal state, it indicates that we encountered a loop;
        # No need to further add the successors to the frontier list

        if currentState not in ufcExploredList:
            ufcExploredList.append(currentState)
            successors = problem.getSuccessors(currentState)

            for successor, action, cost in successors:
                # Temp variable used to push the whole list of actions taken to reach a particular successor;
                path = ufcSolution[:]
                path.append(action)
                ufcFrontierList.push(successor, problem.getCostOfActions(
                    path) + heuristic(successor, problem))
                ufcPath.push(path, problem.getCostOfActions(
                    path) + heuristic(successor, problem))

        currentState = ufcFrontierList.pop()
        ufcSolution = ufcPath.pop()

    return ufcSolution

    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
