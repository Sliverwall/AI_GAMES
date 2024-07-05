import tkinter as tk
from tkinter import messagebox
from Bots import RSP_Bot
from SQL_Query import SQL_Query
from random import choice
class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(self.root)
        self.database = SQL_Query("AI_Games")

        self.botInputHistory = []
        self.userInputHistory = []
        self.resultHistory = []

        # initialize bot manually for now
        self.botID = 6
        self.bot = RSP_Bot(self.botID)

        self.choices = [0, 1, 2]
        rock = 0
        paper = 1
        scissors = 2

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
        
        if self.userName == "random":
            userInput = choice(self.choices)
        # determine bot move using custom bot's moves
        botInput = self.bot.make_move(self.botInputHistory,self.userInputHistory,self.resultHistory)

        # update current game's move history in memory
        self.botInputHistory.append(botInput)
        self.userInputHistory.append(userInput)

        # detemrine result
        result = self.evaluteResult(userInput, botInput)

        # result history
        self.resultHistory.append(result)    

        # Update game table
        self.database.updateGame(self.gameID, result)

        # set conditional values
        win = 2
        draw = 0
        lose = 1

        # return lost history


        inputDisplay = {0: "Rock",
                        1: "Paper",
                        2: "Scissors"}
        
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

        # R = 0, P = 1, S = 2
        # win = 2, lose = 1, draw = 0
         
        resultMatrix = [
             [0,0,0], # rock vs rock = 0 draw
             [0,1,1], # rock vs paper = 1 lose
             [0,2,2], # rock vs scissiors = 2 win

             [1,0,2], # paper vs rock = 2 win
             [1,1,0], # paper vs paper = 0 draw
             [1,2,1], # paper vs scissiors = 1 lose

             [2,0,1], # scissors vs rock = 1 lose
             [2,1,2], # scissors vs paper = 2 win
             [2,2,0]  # scissors vs scissors = 0 draw
         ]

        # Determine outcome using resultMatrix
        for entry in resultMatrix:
            if entry[0] == userInput and entry[1] == botInput:
                result = entry[2]  # Return the result (0 for draw, 1 for lose, 2 for win)

        return result
    


    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()

