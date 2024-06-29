from Bots import *


testBot = RSP_Bot(6)

userInputHistory = ["R", "R", "R", "R", "R","R"]
botInputHistory = ["S","R"]
botWinHistory = [0, 0]

print(testBot.majorityBot(userInputHistory))
print(testBot.usualNextMoveBot(userInputHistory))
            



