import tkinter as tk
from tkinter import messagebox
from Bots import RSP_Bot
from SQL_Query import SQL_Query
class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.database = SQL_Query("AI_Games")

        self.botInputHistory = []
        self.userInputHistory = []
        self.botWinHistory = []

        # initialize bot manually for now
        self.botID = 6
        self.bot = RSP_Bot(self.botID)

        
        rock = "R"
        paper = "P"
        scissors = "S"

        # get current user information
        userData = self.database.getActiveUser()
        if not userData:
            messagebox.showinfo("Task failed", "Please login to play!")
            
        self.userID, self.userName = userData[0], userData[1]
        
        self.database.createGame()

        # Get most current game
        gameData = self.database.getGamesData()

        # Initialize current game rows
        self.gameID, self.gameWins, self.gameLoses, self.gameDraws = gameData[0], gameData[2], gameData[3], gameData[4]

        self.winRate = 0.0
        self.totalMoves = 0

        # Labels for game display
        self.user_label = tk.Label(self.frame, text=f"Welcome to Rock, Paper, Scissiors {self.userName}!")
        self.user_label.pack(pady=10)

        self.game_label = tk.Label(self.frame, text=f"Game id: {self.gameID}, Score: {self.gameWins}/{self.gameDraws}/{self.gameLoses}, win rate: {self.winRate}%")
        self.game_label.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="Results displayed here: ")
        self.result_label.pack(side= tk.TOP, pady=10)

        self.rock_button = tk.Button(self.frame, text="Rock", command=lambda: self.play_game(rock))
        self.rock_button.pack(side=tk.LEFT, padx=10)
        
        self.paper_button = tk.Button(self.frame, text="Paper", command=lambda: self.play_game(paper))
        self.paper_button.pack(side=tk.LEFT, padx=10)
        
        self.scissors_button = tk.Button(self.frame, text="Scissors", command=lambda: self.play_game(scissors))
        self.scissors_button.pack(side=tk.LEFT, padx=10)
        

    def play_game(self, userInput):

        # determine bot move using custom bot's moves
        botInput = self.bot.make_move(self.botInputHistory,self.userInputHistory,self.botWinHistory)
        print(self.bot.currentMethod)

        # update current game's move history in memory
        self.botInputHistory.append(botInput)
        self.userInputHistory.append(userInput)

        # detemrine result
        result = self.evaluteResult(userInput, botInput)

        # update botHistoryWin
        if result == 1: 
            self.botWinHistory.append(1)
        else:
            self.botWinHistory.append(0)
            



        # Update game table
        self.database.updateGame(self.gameID, result)

        # set conditional values
        win = 2
        draw = 0
        lose = 1

        inputDisplay = {"R": "Rock",
                        "P": "Paper",
                        "S": "Scissors"}
        
        outcomeDisplay = {win: "You Won!",
                          draw: "Game Drew.",
                          lose: "You Lost!"}
        
        outcome = outcomeDisplay[result]
        self.result_label.config(text=f"Computer chose {inputDisplay[botInput]}. {outcome}")

        # update moves table
        self.database.updateMoves(self.gameID, self.userID, self.botID, userInput, botInput, result)

        # update display
        gameData = self.database.getGamesData()

        # re-Initialize current game rows
        self.gameID, self.gameWins, self.gameLoses, self.gameDraws = gameData[0], gameData[2], gameData[3], gameData[4]
        self.totalMoves = gameData[1]
        self.winRate = round((self.gameWins/self.totalMoves)*100,2)

        self.game_label.config(text=f"Game id: {self.gameID}, Score: {self.gameWins}/{self.gameDraws}/{self.gameLoses}, win rate: {self.winRate}%")

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
    


    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()

