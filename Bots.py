import random
import math
import numpy as np

class RSP_Bot():
    def __init__(self, botID, greediness=0.3) -> None:
        self.choices = ["R", "P", "S"]
        self.botID = botID
        self.votingHistory = []

        # bot traits
        self.shortMemory = False  # trait that causes bot to discard weights every 5th turn
        self.winnerTakesAll = False  # bot with highest score decides alone
        self.greediness = greediness  # eplsion factor to determine how often to exploit strat

        # Initialize methods
        self.methodList = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]  # store use cases for main move method, exclude random

        self.botScore = {1: 0,  # random
                         2: 0,  # counter
                         3: 0,  # majority
                         4: 0,  # counterClockWise
                         5: 0,  # usualNextMove
                         7: 0,  # againstMajority
                         8: 0,  # copyCat
                         9: 0,  # assumeClockwise
                         10: 0,  # assumeCounterClockWise
                         11: 0,  # assumeBackAndForth
                         12: 0,  # beatRandomMoveBot
                         13: 0,  # againstUsualMove
                         14: 0,  # winAgainMoveBot
                         15: 0,  # ZJCBot
                         16: 0,  # assumeRepeatDrawBot
                         17: 0  # assumeThreeMoveSequence
                         }

        # store info
        self.pulledGreed = 0  # number of times decided to exploit
        self.methodPulled = np.zeros(len(self.methodList))  # number of times method was best method to choose

        # reward points
        self.winBonus = 1
        self.loseBonus = -1
        self.drawBonus = 0

    def make_move(self, botInputHistory, userInputHistory, resultHistory):
        # determine method to use based off botID

        match self.botID:
            case 1:
                return self.randomBot()
            case 2:
                return self.counterBot(userInputHistory)
            case 3:
                return self.majorityBot(userInputHistory)
            case 4:
                return self.counterClockWiseMoveBot(botInputHistory)
            case 5:
                return self.usualNextMoveBot(userInputHistory)
            case 6:
                return self.votingBot(userInputHistory, botInputHistory, resultHistory)
            case 7:
                return self.againstMajorityBot(userInputHistory)
            case 8:
                return self.copyCatBot(userInputHistory)
            case 9:
                return self.assumeClockWiseMoveBot(userInputHistory)
            case 10:
                return self.assumeCounterClockWiseMoveBot(userInputHistory)
            case 11:
                return self.backAndForthMoveBot(userInputHistory)
            case 12:
                return self.beatRandomMoveBot()
            case 13:
                return self.againstUsualMoveBot(userInputHistory)
            case 14:
                return self.winAgainMoveBot(userInputHistory, resultHistory)
            case 15:
                return self.ZJCBot(botInputHistory, resultHistory)
            case 16:
                return self.assumeRepeatDrawBot(botInputHistory, resultHistory)
            case 17:
                return self.assumeThreeMoveSequence(userInputHistory)
            case 100:
                return self.votingBot(userInputHistory, botInputHistory, resultHistory)
    
    def randomBot(self):
        # bot id = 1
        return random.choice(self.choices)
    
    def counterBot(self, userInputHistory):
        # bot id = 2
        # get last user move, if none give user random move
        if userInputHistory != []:
            lastUserMove = userInputHistory[-1]
        else:
            lastUserMove = random.choice(self.choices)
        
        # beat last user move
        match lastUserMove:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def majorityBot(self, userInputHistory):
        # bot id = 3
        # get history of user input, take most common move to be expected move
        if userInputHistory == []:
            predictedUserInput = random.choice(self.choices)
        else:
            # init hashMap
            moveMap = {"R": 0,
                       "P": 0,
                       "S": 0}
            for userMove in userInputHistory:
                moveMap[userMove] += 1
            # predict userInput based on majority input.
            predictedUserInput = max(moveMap, key=moveMap.get)

        # beat predicted user input
        match predictedUserInput:
            case "R":
                  return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def counterClockWiseMoveBot(self, botInputHistory):
        # bot id = 4
        # assume player is moving counter clock-wise
        if botInputHistory == []:
            lastBotMove = random.choice(self.choices)
        else:
            # get last bot move
            lastBotMove = botInputHistory[-1]
            # match case then move counter clock-wise
        match lastBotMove:
            case "R":
                return "S"
            case "P":
                return "R"
            case "S":
                return "P"
    
    def usualNextMoveBot(self, userInputHistory):
        # botID = 5

        # Look at pairs of moves, and find the most common third response
        # clone userInputHistory as to not mutate actual list
        clonedUserInputHistory = userInputHistory.copy()

        # before potentially imputing move, grab last userInputMove
        if clonedUserInputHistory != []:
            lastUserMove = clonedUserInputHistory[-1]
        else:
            lastUserMove = random.choice(self.choices)

        if len(clonedUserInputHistory) < 2:
            predictedUserMove = random.choice(self.choices)
        else:
            # init hashMap
            moveMap = {"RR": 0,
                       "RP": 0,
                       "RS": 0,
                       "PR": 0,
                       "PP": 0,
                       "PS": 0,
                       "SR": 0,
                       "SP": 0,
                       "SS": 0}
            # sort userInput into pairs
            # Pair each letter with its next neighbor using zip
            pairedUserInput = ["".join(pair) for pair in zip(clonedUserInputHistory[0::2], clonedUserInputHistory[1::2])]

            for pair in pairedUserInput:
                # only count pairs related to lastUserInput

                if pair[0] == lastUserMove:
                    moveMap[pair] += 1
            
            # predict userInput based on majority input.
            predictedPair = max(moveMap, key=moveMap.get)
            predictedUserMove = predictedPair[1] # right char is the predicted move
        match predictedUserMove:
            case "R":
                  return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def votingBot(self, userInputHistory, botInputHistory,resultHisotry):


        # Ensure at least 3 game history entries
        while len(userInputHistory) < 3:
            userRandomChoice = random.choice(self.choices)
            botRandomChoice = random.choice(self.choices)
            userInputHistory.append(userRandomChoice)
            botInputHistory.append(botRandomChoice)
            resultHisotry.append(self.evaluteResult(userRandomChoice, botRandomChoice))
            votingList = [random.choice(self.choices) for _ in self.methodList]
            self.votingHistory.append(votingList)

        votingList = [] # list to tally up votes
            

        # update bot scores based on previous history
        self.updateBotScores(userInputHistory)


        # Voting stage

        storeBotID = self.botID # will change botID while cycling methods

        for method in self.methodList:
            self.botID = method
            vote = self.make_move(botInputHistory,userInputHistory,resultHisotry)
            votingList.append(vote)
        

        self.botID = storeBotID # reassign botID
        # init hashMap
        moveMap = {"R": 0,
                    "P": 0,
                    "S": 0}
        
        # scale voting power based on past performance
        bestMethod, bestScore, bestVote = 1,0, "R" 
        for index, item in enumerate(votingList):
            currentMethod = self.methodList[index]
            currentScore = self.botScore[currentMethod]
            maxScoreKey = max(self.botScore, key=self.botScore.get)
            maxScore = self.botScore[maxScoreKey]
            # grab with vote from the maxScoring method
            if maxScore == currentScore:
                bestVote = item
            # store maxScoreKey in variable for later
            bestMethod, bestScore = maxScoreKey, maxScore

            votingPower = (math.e)**(currentScore - maxScore) # expo e to get voting power

            moveMap[item] += votingPower

        # DEBUGGING
        # print(f"vote list: {votingList}") # print ballet for debuging
        # print(f"User last move: {userInputHistory[-1]}")
        # print(f"botScores: {self.botScore}") # print method scores for debugging
        # print(f"moveMap {moveMap}") # print for debugging purposes
        # print(f"Current best method: {bestMethod}, with score of: {bestScore} with vote of {bestVote}")

        # bot's desired 
        beRandom = random.random()
        if self.greediness <= beRandom:
            print(f"GREEDY BOY. Greediness: {self.greediness} vs random pull {beRandom}")
            if self.winnerTakesAll:
                predictedBotMove = bestVote
            else:
                predictedBotMove = max(moveMap, key=moveMap.get)
        else:
            predictedBotMove = random.choice(self.choices)

        # save votingList in voting batch history
        self.votingHistory.append(votingList)
        


        return predictedBotMove
    

    def againstMajorityBot(self, userInputHistory):
        # bot id = 7
        majorityVote = self.majorityBot(userInputHistory)

        # choose the losing move from majority bot's perspective
        match majorityVote:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def copyCatBot(self, userInputHistory):
        # bot id = 8
        if userInputHistory == []:
            lastMove = random.choice(self.choices)
        else:
            lastMove = userInputHistory[-1]
        return lastMove
    
    def assumeClockWiseMoveBot(self, userInputHistory):
        # bot id = 9
        if userInputHistory == []:
            lastMove = random.choice(self.choices)
        else:
            lastMove = userInputHistory[-1]
        # assume next move will be clockwise R -> P -> S
        match lastMove:
            case "R":
                nextMove = "P"
            case "P":
                nextMove = "S"
            case "S":
                nextMove = "R"
        # Beat next predicted move
        match nextMove:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R" 
    def assumeCounterClockWiseMoveBot(self, userInputHistory):
        # bot id = 10
        if userInputHistory == []:
            lastMove = random.choice(self.choices)
        else:
            lastMove = userInputHistory[-1]
        # assume next move will be clockwise R <- P <- S
        match lastMove:
            case "R":
                nextMove = "S"
            case "P":
                nextMove = "R"
            case "S":
                nextMove = "P"
        # Beat next predicted move
        match nextMove:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"     

    def backAndForthMoveBot(self, userInputHistory):
        # bot id = 11
        # assume the last two moves are pairs that will repeat
        if len(userInputHistory) < 3:
            return random.choice(self.choices)
        predictedMove = userInputHistory[-2]

        match predictedMove:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def beatRandomMoveBot(self):
        # bot id = 12
        # assume user is using psudoGenerator
        predicatedUserChoice = random.choice(self.choices)

        match predicatedUserChoice:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def againstUsualMoveBot(self, userInputHistory):
        # bot id = 13
        usualMoveOutcome = self.usualNextMoveBot(userInputHistory)

        match usualMoveOutcome:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    
    def winAgainMoveBot(self, userInputHistory, resultHistory):
        # bot id = 14
        # assumes user will repeat winning moves and drawing moves, and avoid losing moves
        # similar to counter-clockwise bot, but only believes counter-clockwise pattern if user is losing
        if resultHistory == 0:
            return random.choice(self.choices) # vote for random move if no history
        else:
            lastMove = userInputHistory[-1]
            if resultHistory[-1] == 1: # if user lost, assume they will make what would have been the winning move
                match lastMove:
                    case "R":
                        return "S" # if rock lost, then that means winning move was paper
                    case "P":
                        return "R"
                    case "S":
                        return "P"
            else: # user either tied or won so assume will repeat move
                match lastMove:
                    case "R":
                        return "P"
                    case "P":
                        return "S"
                    case "S":
                        return "R"

    def ZJCBot(self, botInputHistory, resultHistory):
        # bot id = 15
        # The Zhejiang Cycle. Method developed from studying 18k games.
        # if winning or losing, move counter clock-wise. If draw, just repeat
        if resultHistory == 0:
            return random.choice(self.choices) # vote for random move if no history
        else:
            lastMove = botInputHistory[-1]
            if resultHistory[-1] == 1 or resultHistory[-1] == 2 : # if bot wins or loses, go counter clock-wise, else repeat
                match lastMove:
                    case "R":
                        return "S" 
                    case "P":
                        return "R"
                    case "S":
                        return "P"
            else: # bot tied, so just repeat
                return lastMove
    
    def assumeRepeatDrawBot(self, botInputHistory, resultInputHistory):
        # bot id = 16
        # if there is a drawer, assumes player will repeat move. Otherwise just repeat last move

        if resultInputHistory == []:
            return random.choice(self.choices)
        
        if resultInputHistory[-1] == 0:
            predictedMove = botInputHistory[-1]
            match predictedMove:
                case "R":
                    return "P"
                case "P":
                    return "S"
                case "S":
                    return "R"
        else:
            return botInputHistory[-1]

    def assumeThreeMoveSequence(self, userInputHistory):
        # bot id = 17
        if len(userInputHistory) < 3:
            vote = random.choice(self.choices)
        else:
            predictedMove = userInputHistory[-3]
            match predictedMove:
                case "R":
                    vote = "P"
                case "P":
                    vote = "S"
                case "S":
                    vote = "R"
        return vote


    # --------------------helper methods-------------------------------------------
    def evaluteResult(self, userInput, botInput):

        joinedInput = f"{userInput}_{botInput}"

        # set conditional values
        win = 2
        draw = 0
        lose = 1
        # resultDict to store user vs bot outcomes posibilities
        resultDict = {"R_R": draw,
                    "R_P": lose,
                    "R_S": win,
                    "P_R": win,
                    "P_P": draw,
                    "P_S": lose,
                    "S_R": lose,
                    "S_P": win,
                    "S_S": draw}
        # user result as stored in resultDict
        userResult = resultDict[joinedInput] # botResult = 0 - userResult

        return userResult
    
    def updateBotScores(self, userInputHistory):
        # # reset scores as they will loop over entire set again
        for key in self.botScore.keys():
            self.botScore[key] = 0
        
        # Loop through each move in userInputHistory along with its corresponding vote batch
        for i, move in enumerate(userInputHistory[-1]):
            if i < len(self.votingHistory[-1]):
                voteBatch = self.votingHistory[i]
                # Loop through each vote in the vote batch
                for index, vote in enumerate(voteBatch):
                    bot = self.methodList[index]
                    outcome = self.evaluteResult(move, vote)  # 2 bot loses, 0 draw, 1 bot wins
                    # DEBUGGING
                    print(f"Move: {move}, Vote: {vote}, Bot: {bot}, Outcome: {outcome}")
                    # Reward system
                    if outcome == 2:
                        self.botScore[bot] += self.loseBonus
                    elif outcome == 1:
                        self.botScore[bot] += self.winBonus
                    elif outcome == 0:
                        self.botScore[bot] += self.drawBonus
        return self.botScore
            