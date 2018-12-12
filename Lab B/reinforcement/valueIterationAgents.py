# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, next_state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()

        # Write value iteration code here
        for i in range(iterations):
            new_values = util.Counter()

            for state in mdp.getStates():
                alpha = 1  # TODO voor alpha moet waarschijnlijk iets van 1/(n+1)
                old_value = self.values[state]
                action_values = util.Counter()

                for action in mdp.getPossibleActions(state):
                    for next_state, prob in mdp.getTransitionStatesAndProbs(state, action):
                        # TODO fix
                        # if i > 1 and self.values[next_state] != 0:
                            # TODO fix
                            action_values[action] += prob * alpha * (mdp.getReward(state, action, next_state) + discount * self.getValue(next_state) - old_value)

                new_values[state] = old_value + action_values[action_values.argMax()]

            self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # Bepaal in welke state we waarschijnlijk terechtkomen
        # TODO volgens mij mag dit, misschien moet kans mee worden genomen
        highest_prob = 0
        next_state = state

        for neighbour, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            if prob > highest_prob:
                highest_prob = prob
                next_state = neighbour

        # Geef de waarde van de betreffende state terug
        return self.values[next_state]

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        highest_value = 0
        best_action = None

        # Voor elke actie vanaf deze state...
        for action in self.mdp.getPossibleActions(state):
            # Bepaal in welke state we waarschijnlijk terechtkomen
            # TODO volgens mij mag dit, misschien moet kans mee worden genomen
            highest_prob = 0
            for neighbour, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                if prob > highest_prob:
                    highest_prob = prob
                    next_state = neighbour

            # Check of deze state de beste value heeft
            if self.values[next_state] > highest_value:
                highest_value = self.values[next_state]
                best_action = action

        # Geef de actie terug die naar de state leid die de beste value heeft
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
