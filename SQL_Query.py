import sqlite3

class SQL_Query():

    def __init__(self, name) -> None:
        self.dbName = f"{name}.db"

    # -------- user table queries -----------
    def getUserData(self, name):
        # Establish connection and cursor
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT userID, userName , password, email
                       FROM users
                       WHERE userName = '{name}'
                       ''')
        
        userNameRow = cursor.fetchone()
        
        conn.close()
        # If a result is found, return the password
        if userNameRow:
            return userNameRow
        else:
            return None
    def checkUser(self, name):
        userNameRow = self.getUserData(name)

        return userNameRow[1]
    
    def getUserUniqueID(self, name):
        userNameRow = self.getUserData(name)

        return userNameRow[0]
    def getUserPassword(self, name):
        userNameRow = self.getUserData(name)

        return userNameRow[2]
    def getUserEmail(self, name):
        userNameRow = self.getUserData(name)

        return userNameRow[3]


    def updateUser(self,name,password,email):

        # Establish connection and cursor
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        
        cursor.execute(f'''
        INSERT INTO users (userName, password, email)
        VALUES ('{name}', '{password}', '{email}')
    ''')
        conn.commit()
        conn.close()
    

    # -------- login_user and login_status table queries -----------

    def loginUser(self, userName):
        
        try:
            # Get userID to store to loginUser Table
            userID = self.getUserUniqueID(userName)

            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()


            # Add login history to login_users
            cursor.execute(f'''
                INSERT INTO login_users (userID)
                VALUES ('{userID}')
            ''')

            cursor.execute(f'''
                SELECT loginStatus
                FROM login_status
                WHERE userID = {userID}
            ''')
            login_status_row = cursor.fetchone()
            
            # Check whether loginStatus is True or False, if none, insert first login_status
            if login_status_row:
                if login_status_row[0] == "T":
                    conn.close()
                    return 0
                elif login_status_row[0] == "F":
                    cursor.execute(f'''
                        UPDATE login_status
                        SET loginStatus = 'T'
                        WHERE userID = {userID}
                    ''')
                    
            else:
                cursor.execute(f'''
                    INSERT INTO login_status (userID)
                    VALUES ('{userID}')
                ''')
            
            conn.commit()


            conn.commit()
            conn.close()
        except Exception as e:
            # Print the error message if an exception is caught
            print(f"An error occurred: {e}")

    def logoutUser(self, userName):

        try:
            # Get userID to store to loginUser Table
            userID = self.getUserUniqueID(userName)

            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()

            cursor.execute(f'''
                SELECT loginStatus
                FROM login_status
                WHERE userID = {userID}
            ''')
            login_status_row = cursor.fetchone()
            
            # Check whether loginStatus is True or False, if none, insert first login_status
            if login_status_row[0] == "F":
                conn.close()
                return 0
            else:
                cursor.execute(f'''
                        UPDATE login_status
                        SET loginStatus = 'F'
                        WHERE userID = {userID}
                    ''')
            conn.commit()
            conn.close
        except Exception as e:
            # Print the error message if an exception is caught
            print(f"An error occurred: {e}")

    def getLogin_StatusData(self, userName):
            # Get userID to store to loginUser Table
            userID = self.getUserUniqueID(userName)

            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()

            cursor.execute(f'''
                        SELECT *
                        FROM login_status
                        WHERE userID = {userID}
                    ''')
            loginStatusRows = cursor.fetchone()

            conn.close()
            return loginStatusRows
    
    def getLoginStatus(self, userName):
        loginStatus = self.getLogin_StatusData(userName)

        return loginStatus[2]
    # -------- games queries -----------

    def getCurrentGame(self):
        try:
            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            cursor.execute(f'''
                        SELECT MAX(gameID)
                        FROM rsp_games
                        ''')
            maxGameIDRows = cursor.fetchone()

            # max gameID should be most recently opened game
            maxGameID = maxGameIDRows[0]

            conn.close()
            return maxGameID
        except Exception as e:
            # Print the error message if an exception is caught
            print(f"An error occurred: {e}")

    def getGamesData(self):
        # get the current gameID
        currentGameID = self.getCurrentGame()
        try:
            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            
            cursor.execute(f'''
                            SELECT *
                            FROM rsp_games
                            WHERE gameID = {currentGameID}
                            ''')
            gameRows = cursor.fetchone()
            conn.close()

            return gameRows
        except Exception as e:
            # Print the error message if an exception is caught
            print(f"An error occurred: {e}")

    def createGame(self):
        try:
            # Establish connection and cursor
            conn = sqlite3.connect(self.dbName)
            cursor = conn.cursor()
            
            cursor.execute(f'''
                        INSERT INTO rsp_games (number_moves, number_wins, number_loses, number_draws)
                        VALUES (0, 0, 0, 0);

                            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            # Print the error message if an exception is caught
            print(f"An error occurred: {e}")
    
    def updateGame(self, gameID, status):
        # Establish connection and cursor
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()   

        # set conditional values
        win = 2
        draw = 0
        lose = 1
        statusColumn = {win : "number_wins",
                        draw : "number_draws",
                        lose : "number_loses"}
        cursor.execute(f'''
                        UPDATE rsp_games
                        SET {statusColumn[status]} = {statusColumn[status]} + 1,
                        number_moves = number_moves + 1
                        WHERE gameID = {gameID}
                    ''')
        

        conn.commit()
        conn.close

    def updateMoves(self,gameID, userID, botID, userMove, botMove, result):
        # Establish connection and cursor
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()   

        # set conditional values

        cursor.execute('''
                        INSERT INTO moves (gameID, userID, botID, userMove, botMove, result)
                        VALUES (?,?,?,?,?,?);

                            ''',(gameID, userID, botID, userMove, botMove, result))
        

        conn.commit()
        conn.close
    
    def getActiveUser(self):
        # Establish connection and cursor
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()

        cursor.execute(f'''
                       SELECT userID
                       FROM login_status
                       WHERE loginStatus = 'T'
                       ''')
        
        loginStatusRow = cursor.fetchone()
        
        # If a result is found, return the password
        if loginStatusRow:
            userID = loginStatusRow[0]
            cursor.execute(f'''
                       SELECT userName
                       FROM users
                       WHERE userID = {userID}
                       ''')
            userNameRow = cursor.fetchone()
            conn.close
            return userID, userNameRow[0]
        else:
            conn.close
            return None