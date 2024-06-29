import random
import math


class RSP_Bot():
    def __init__(self, botID) -> None:
        self.choices = ["R", "P", "S"]
        self.botID = botID
        self.votingHistory = [] # keep voting history
        self.methodList = [1,2,3,4,5,7] # store use cases for main move method, exclude random
        self.botScore = {1:0, # random
                    2:0, #counter
                    3:0, #majority
                    4:0, #counterClockWise
                    5:0, #usualNextMove
                    7:0 #againstMajority
                    }
 
    def make_move(self, botInputHistory, userInputHistory, botWinHisotry):
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
                return self.votingBot(userInputHistory,botInputHistory,botWinHisotry)
            case 7:
                return self.againstMajorityBot(userInputHistory)
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
    def votingBot(self, userInputHistory, botInputHistory, botWinHistory):
        # Keep track of current move
        currentMove = len(userInputHistory)

        # if not history just return random
        if currentMove == 0:
            return random.choice(self.choices)

        # update bot scores based on previous history
        self.updateBotScores(userInputHistory, self.methodList)


        # Voting stage
        votingList = [] # list to tally up votes

        storeBotID = self.botID # will change botID while cycling methods

        # print(f"bothistory: {botInputHistory}\n,userHistory: {userInputHistory}\n,botWinHistory : {botWinHistory}")
        for method in self.methodList:
            self.botID = method
            vote = self.make_move(botInputHistory,userInputHistory,botWinHistory)
            votingList.append(vote)
        

        print(votingList) # print ballet for debuging
        print(self.botScore) # print method scores for debugging

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

        print(moveMap) # print for debugging purposes
        
        # bot's desired vote
        predictedBotMove = max(moveMap, key=moveMap.get)

        # save votingList in voting batch history
        self.votingHistory.append(votingList)

        return predictedBotMove
    

    def againstMajorityBot(self, userInputHistory):
        majorityVote = self.majorityBot(userInputHistory)

        # choose the losing move from majority bot's perspective
        match majorityVote:
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
    
    def updateBotScores(self, userInputHistory, methodList):
        for move in userInputHistory:
            for voteBatch in self.votingHistory:
                for index, vote in enumerate(voteBatch):
                    bot = methodList[index]
                    outcome = self.evaluteResult(move, vote) # 2 bot loses, 0 draw, 1 bot wins
                    # penalize loses, record scores, do not punish or reward draws
                    if outcome == 2:
                        self.botScore[bot] -=1
                    elif outcome == 1:
                        self.botScore[bot] +=1
                    elif outcome == 0:
                        self.botScore[bot] -= 0.5 # take away half a point for drawing

            