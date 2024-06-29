import random

class RSP_Bot():
    def __init__(self, botID) -> None:
        self.choices = ["R", "P", "S"]
        self.botID = botID
        self.currentMethod = 5

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
                return self.counterClockWiseMove(botInputHistory)
            case 5:
                return self.usualNextMove(userInputHistory)
            case 6:
                return self.basicMixMove(botInputHistory,userInputHistory, botWinHisotry)
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
    def counterClockWiseMove(self, botInputHistory):
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
    
    def usualNextMove(self, userInputHistory):
        # botID = 5

        # Look at pairs of moves, and find the most common third response

        # before potentially imputing move, grab last userInputMove
        if userInputHistory != []:
            lastUserMove = userInputHistory[-1]
        else:
            lastUserMove = random.choice(self.choices)

        # if list length is not even, imput random move
        if len(userInputHistory) % 2 != 0:
            userInputHistory.append(random.choice(self.choices))
        if len(userInputHistory) < 2:
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
            pairedUserInput = ["".join(pair) for pair in zip(userInputHistory[0::2], userInputHistory[1::2])]

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
    def basicMixMove(self, userInputHistory, botInputHistory, botWinHistory):
        # Keep track of current move
        currentMove = len(userInputHistory)

        methodList = [3,5] # store use cases for main move method, exclude random

        # Switch between methods
        # use random moves while building history
        if currentMove < 5:
            self.currentMethod = 1
        
        if len(botWinHistory) >= 5 and sum(botWinHistory[-5:]) < 3:
            self.currentMethod = random.choice(methodList)
        
        # call from list of methods
        match self.currentMethod:
            case 1: 
                return self.randomBot()
            case 2:
                return self.counterBot(userInputHistory)
            case 3:
                return self.majorityBot(userInputHistory[-5:])
            case 4:
                return self.counterClockWiseMove(botInputHistory)
            case 5:
                return self.usualNextMove(userInputHistory[-5:])