
def evaluteResult(userInput, botInput):

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

def updateBotScores(userInputHistory, methodList,votingHistory,botScore):
    # Loop through each move in userInputHistory along with its corresponding vote batch
    for i, move in enumerate(userInputHistory):
        if i < len(votingHistory):
            voteBatch = votingHistory[i]
            # Loop through each vote in the vote batch
            for index, vote in enumerate(voteBatch):
                bot = methodList[index]
                outcome = evaluteResult(move, vote)  # 2 bot loses, 0 draw, 1 bot wins
                if bot == 4:
                    print(f"move {move}, vote {vote}, outcome {outcome}")
                # Penalize losses, record scores, do not punish or reward draws
                if outcome == 2:
                    botScore[bot] -= 1
                elif outcome == 1:
                    botScore[bot] += 1
                elif outcome == 0:
                    botScore[bot] -= 1  # penalty for drawing
    return botScore


votingHistory = [['S', 'P', 'P', 'P', 'P', 'S'],
                    ['S', 'P', 'P', 'S', 'P', 'S']] # keep voting history
methodList = [1,2,3,4,5,7] # store use cases for main move method, exclude random
botScore = {1:0, # random
            2:0, #counter
            3:0, #majority
            4:0, #counterClockWise
            5:0, #usualNextMove
            7:0 #againstMajority
            }
userInputHistory = ["R", "P"]
print(updateBotScores(userInputHistory, methodList, votingHistory, botScore))
