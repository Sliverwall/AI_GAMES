import numpy as np
import random
from Bots import RSP_Bot

class RL_Bot():

    def __init__(self):
        # Actions
        self.actions = ['rock', 'paper', 'scissors']

        self.userInputHistory = []
        self.botInputHistory = []
        self.resultHistory = []

        # Reward matrix: rows are agent's actions, columns are opponent's actions
        self.reward_matrix = np.array([
            [0, -1, 1],  # rock: 0 = tie, -1 = loss (rock vs paper), 1 = win (rock vs scissors)
            [1, 0, -1],  # paper: 1 = win (paper vs rock), 0 = tie, -1 = loss (paper vs scissors)
            [-1, 1, 0]   # scissors: -1 = loss (scissors vs rock), 1 = win (scissors vs paper), 0 = tie
        ])

        # Q-learning parameters
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01

        # Initialize Q-table
        self.q_table = np.zeros((3, 3))

    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2])  # Explore: choose a random action
        else:
            return np.argmax(self.q_table[state])  # Exploit: choose the best action

    def trainAgent(self, bot, num_episodes = 10000):
        # Train the agent
        for episode in range(num_episodes):
            maskedState = bot.make_move(self.botInputHistory, self.userInputHistory, self.resultHistory)  # Opponent's action (rock, paper, or scissors)
            self.botInputHistory.append(maskedState)

            state = self.maskedInput(maskedState)
            if state is None:
                print(f"Invalid masked state: {maskedState}")
                continue

            action = self.get_action(state)
            self.userInputHistory.append(self.maskOutput(action))  # Add maskedAction to userHistory

            # Opponent randomly chooses an action
            next_opponent_action = self.maskedInput(bot.make_move(self.botInputHistory, self.userInputHistory, self.resultHistory))  # Opponent's action (rock, paper, or scissors)
            if next_opponent_action is None:
                print(f"Invalid next masked state: {maskedState}")
                continue

            # Get the reward
            reward = self.reward_matrix[action][next_opponent_action]

            # Update Q-table
            next_state = next_opponent_action
            best_next_action = np.argmax(self.q_table[next_state])
            self.q_table[state][action] = self.q_table[state][action] + self.alpha * (reward + self.gamma * self.q_table[next_state][best_next_action] - self.q_table[state][action])

            # Decay epsilon
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def testAgent(self, bot, num_tests=100):
        # Test the trained agent
        num_tests = 100
        win, lose, tie = 0, 0, 0
        for _ in range(num_tests):
            maskedState = bot.make_move(self.botInputHistory, self.userInputHistory, self.resultHistory)  # Opponent's action (rock, paper, or scissors)
            self.botInputHistory.append(maskedState)

            state = self.maskedInput(maskedState)
            if state is None:
                print(f"Invalid masked state: {maskedState}")
                continue

            action = self.get_action(state)
            self.userInputHistory.append(self.maskOutput(action))  # Add maskedAction to userHistory

            opponent_action = self.maskedInput(bot.make_move(self.botInputHistory, self.userInputHistory, self.resultHistory))
            if opponent_action is None:
                print(f"Invalid masked state: {maskedState}")
                continue

            reward = self.reward_matrix[action][opponent_action]

            if reward == 1:
                win += 1
            elif reward == -1:
                lose += 1
            else:
                tie += 1

        print(f'Wins: {win}, Losses: {lose}, Ties: {tie}')

    def maskOutput(self, action):
        # Convert so multiarm bandit can use data
        match action:
            case 0:
                return "R"
            case 1:
                return "P"
            case 2:
                return "S"
    
    def maskedInput(self, state):
        # Convert multiarm bandit to int value so RL bot can use state data
        match state:
            case "R":
                return 0
            case "P":
                return 1
            case "S":
                return 2
            case _:
                return None

banditBot = RSP_Bot(100,greediness=0.2)
rlBot = RL_Bot()

rlBot.trainAgent(banditBot,100)
rlBot.testAgent(banditBot,10)
