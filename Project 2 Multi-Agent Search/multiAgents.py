# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostList = [ghostState.getPosition() for ghostState in newGhostStates]
        ghostDistance = [manhattanDistance(newPos, ghost) for ghost in ghostList]
        foodList = newFood.asList()
        foodDistance = [manhattanDistance(newPos, food) for food in foodList]

        if successorGameState.isWin():
            return 100000
        elif min(ghostDistance) < 2:
            return -1000
        elif currentGameState.hasFood(newPos[0], newPos[1]):
            return 1000
        else:
            return 500 / min(foodDistance)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgent = gameState.getNumAgents()

        def helperMinimax(state, agent, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), "End")

            nextAgent = agent + 1
            nextDepth = depth

            if agent == 0:
                maxVal = -1000000
                act = "NULL"
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperMinimax(successor, nextAgent, nextDepth)
                    if val > maxVal:
                        maxVal, act = val, step
                return maxVal, act

            else:
                minVal = 1000000
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperMinimax(successor, nextAgent, nextDepth)
                    if val < minVal:
                        minVal, act = val, step
                return minVal, act

        value, action = helperMinimax(gameState, 0, 0)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgent = gameState.getNumAgents()

        def helperAlphaBeta(state, agent, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), "End")

            nextAgent = agent + 1
            nextDepth = depth

            if agent == 0:
                maxVal = -1000000
                act = "NULL"
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperAlphaBeta(successor, nextAgent, nextDepth, alpha, beta)
                    if val > beta:
                        return val, step
                    if val > maxVal:
                        maxVal, act = val, step
                    alpha = max(alpha, maxVal)
                return maxVal, act

            else:
                minVal = 1000000
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperAlphaBeta(successor, nextAgent, nextDepth, alpha, beta)
                    if val < alpha:
                        return val, step
                    if val < minVal:
                        minVal, act = val, step
                    beta = min(beta, minVal)
                return minVal, act

        value, action = helperAlphaBeta(gameState, 0, 0, -10000, 10000)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgent = gameState.getNumAgents()

        def helperExpectimax(state, agent, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return (self.evaluationFunction(state), "End")

            nextAgent = agent + 1
            nextDepth = depth

            if agent == 0:
                maxVal = -1000000
                act = "NULL"
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperExpectimax(successor, nextAgent, nextDepth)
                    if val > maxVal:
                        maxVal, act = val, step
                return maxVal, act

            else:
                expValue = []
                if nextAgent >= numAgent:
                    nextAgent = 0
                    nextDepth += 1

                for step in state.getLegalActions(agent):
                    successor = state.generateSuccessor(agent, step)
                    val, action = helperExpectimax(successor, nextAgent, nextDepth)
                    expValue.append(val)
                return sum(expValue) / len(expValue), "act"

        value, action = helperExpectimax(gameState, 0, 0)
        return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return 1000000000000
    if currentGameState.isLose():
        return -100000000000

    food = currentGameState.getFood().asList()
    pacPos = currentGameState.getPacmanPosition()
    pacFoodDis = [manhattanDistance(pacPos, foodPos) for foodPos in food]
    ghost = currentGameState.getGhostStates()
    ghoPos = [ghost1.getPosition() for ghost1 in ghost]
    scared = [ghost1.scaredTimer for ghost1 in ghost]

    score = currentGameState.getScore()
    score += 1000000 / currentGameState.getNumFood()
    score -= min(pacFoodDis)

    for i in range(len(scared)):
        dis = manhattanDistance(pacPos, ghoPos[i])
        if scared[i] > 1:
            if dis == 0:
                score += 10000000
            else:
                score += 100000 / dis
        else:
            if dis <= 1:
                score -= 1000
    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

