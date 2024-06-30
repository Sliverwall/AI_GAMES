import random
import math


class RSP_Bot():
    def __init__(self, botID, traits=True) -> None:
        self.choices = ["R", "P", "S"]
        self.botID = botID
        self.votingHistory = []

        # bot traits
        self.soreLoser = traits # trait that causes bot to switch weights if lost twice in row
        self.shortMemory = traits # trait that causes bot to discard weights every 5th turn

        # Initialize methods
        self.methodList = [1,2,3,4,5,7,8,9, 10,11,12,13] # store use cases for main move method, exclude random
        self.botScore = {1:0, # random
                    2:0, #counter
                    3:0, #majority
                    4:0, #counterClockWise
                    5:0, #usualNextMove
                    7:0, #againstMajority
                    8:0, #copyCat
                    9:0, #assumeClockwise
                    10:0, #assumeCounterClockWise
                    11:0, # assumeBackAndForth
                    12:0, # beatRandomMoveBot
                    13:0 # againstUsualMove
                    }
        

        # reward points
        self.winBonus = 1
        self.loseBouns = -1
        self.drawBonus = -0.5
 
    def make_move(self, botInputHistory, userInputHistory,resultHistory):
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
                return self.votingBot(userInputHistory,botInputHistory,resultHistory)
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
        # get botInputHistory, then move counter clock-wise R <- P <- S
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
        # Keep track of current move
        currentMove = len(userInputHistory)

        votingList = [] # list to tally up votes

        # if not history just return random
        if currentMove == 0:
            for method in self.methodList:
                # initialize random votes for first round to keep voting history aligned
                vote = random.choice(self.choices)
                votingList.append(vote)
            # save votingList in voting batch history
            self.votingHistory.append(votingList)
            return votingList[0] # return first random
            

        # update bot scores based on previous history
        self.updateBotScores(userInputHistory, resultHisotry)


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
        for index, item in enumerate(votingList):
            currentMethod = self.methodList[index]
            currentScore = self.botScore[currentMethod]
            maxScoreKey = max(self.botScore, key=self.botScore.get)
            maxScore = self.botScore[maxScoreKey]

            votingPower = (math.e)**(currentScore - maxScore) # expo e to get voting power

            moveMap[item] += votingPower

        # DEBUGGING
        print(f"vote list: {votingList}") # print ballet for debuging
        print(f"botScores: {self.botScore}") # print method scores for debugging
        print(f"moveMap {moveMap}") # print for debugging purposes

        # bot's desired vote
        predictedBotMove = max(moveMap, key=moveMap.get)
        

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
        lastTwoMoves = userInputHistory[-2:]

        # assume the last two moves are pairs that will repeat
        predictedMove = lastTwoMoves[0]

        match predictedMove:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
    def beatRandomMoveBot(self):
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
        usualMoveOutcome = self.usualNextMoveBot(userInputHistory)

        match usualMoveOutcome:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"
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
    
    def updateBotScores(self, userInputHistory, resultHisotry):

        # Determine the range of moves to check if resetting history
        if self.shortMemory and len(userInputHistory) % 5 == 0:
            for key in self.botScore.keys():
                self.botScore[key] = 0

        # Sore Loser traint, flips weights if lost two in a row
        if self.soreLoser and len(resultHisotry) > 3 and sum(resultHisotry[-3:]) >= 4:
            print("FLIPING SIGNS")
            # reset scores if two loses in a row
            for key in self.botScore.keys():
                self.botScore[key] = self.botScore[key]*-1 # flip sign of score if losing 2 times in row 

                
        # Loop through each move in userInputHistory along with its corresponding vote batch
        for i, move in enumerate(userInputHistory):
            if i < len(self.votingHistory):
                voteBatch = self.votingHistory[i]
                # Loop through each vote in the vote batch
                for index, vote in enumerate(voteBatch):
                    bot = self.methodList[index]
                    outcome = self.evaluteResult(move, vote)  # 2 bot loses, 0 draw, 1 bot wins
                    # DEBUGGING
                    # print(f"Move: {move}, Vote: {vote}, Bot: {bot}, Outcome: {outcome}")
                    # Reward system
                    if outcome == 2:
                        self.botScore[bot] += self.loseBouns
                    elif outcome == 1:
                        self.botScore[bot] += self.winBonus
                    elif outcome == 0:
                        self.botScore[bot] += self.drawBonus
        return self.botScore
            