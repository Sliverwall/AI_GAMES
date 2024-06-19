import tkinter as tk
from tkinter import messagebox
from SQL_Query import SQL_Query
from Games import RockPaperScissors

class Menu_Actions():
    def __init__(self, root):
        self.root = root


# -------------- Shut down actions ----------------------------
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            database = SQL_Query("AI_Games")

            currentUserData = database.getActiveUser()
            if currentUserData:
                userName = currentUserData[1]

                database.logoutUser(userName)

                messagebox.showinfo("Logout confirmation", f"{userName} logging out.")
            self.root.destroy()
# ------------- FILE menu actions -----------------------------
    def new_file(self):
        # Placeholder for 'New File' functionality
        print("New File functionality")

    def open_file(self):
        # Placeholder for 'Open File' functionality
        print("Open File functionality")

    def save_file(self):
        # Placeholder for 'Save File' functionality
        print("Save File functionality")


# ------------- CONFIG menu actions -----------------------------
    def open_settings(self):
        # Placeholder for 'Open Settings' functionality
        print("Open Settings functionality")


# ------------- ACCOUNT menu actions -----------------------------
    def create_user(self):
        # Create a new toplevel window for the user form
        global createUser_form_window
        createUser_form_window = tk.Toplevel(self.root)
        createUser_form_window.title("Create User")

        # Username field
        tk.Label(createUser_form_window, text="Username:").grid(row=0, column=0, sticky='w')
        self.username_entry = tk.Entry(createUser_form_window)
        self.username_entry.grid(row=0, column=1)

        # Password field
        tk.Label(createUser_form_window, text="Password:").grid(row=1, column=0, sticky='w')
        self.password_entry = tk.Entry(createUser_form_window, show='*')
        self.password_entry.grid(row=1, column=1)

        # Confirm Password field
        tk.Label(createUser_form_window, text="Confirm Password:").grid(row=2, column=0, sticky='w')
        self.confirm_password_entry = tk.Entry(createUser_form_window, show='*')
        self.confirm_password_entry.grid(row=2, column=1)


        # Email address field
        tk.Label(createUser_form_window, text="Email Address:").grid(row=3, column=0, sticky='w')
        self.email_entry = tk.Entry(createUser_form_window)
        self.email_entry.grid(row=3, column=1)

        # Submit button
        submit_button = tk.Button(createUser_form_window, text="Submit", command=self.submit_user)
        submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_user(self):
        # Get values from entries
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()

        # Example: Storing values in variables
        self.username = username
        self.password = password
        self.confirm_password_entry = confirm_password
        self.email = email

        # Ensure password confirmation and unique username
        database = SQL_Query("AI_Games")
        if password == confirm_password and database.checkUser(username) == username:
            # Optionally, show a message box confirming user creation
            database.updateUser(username, password, email)
            messagebox.showinfo("User Created", f"User {username} created successfully!")

        else:
            messagebox.showinfo("User Not Created", "User not created")
        # close form
        createUser_form_window.destroy()

    def login_user(self):
        # Create a new toplevel window for the user form
        global login_form_window
        login_form_window = tk.Toplevel(self.root)
        login_form_window.title("Login")

        # Username field
        tk.Label(login_form_window, text="Username:").grid(row=0, column=0, sticky='w')
        self.username_entry = tk.Entry(login_form_window)
        self.username_entry.grid(row=0, column=1)

        # Password field
        tk.Label(login_form_window, text="Password:").grid(row=1, column=0, sticky='w')
        self.password_entry = tk.Entry(login_form_window, show='*')
        self.password_entry.grid(row=1, column=1)

        # Submit button
        submit_button = tk.Button(login_form_window, text="Submit", command=self.submit_login)
        submit_button.grid(row=2, columnspan=2, pady=10)

    def submit_login(self):
        # Get values from entries
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Example: Storing values in variables
        self.username = username
        self.password = password

        # Ensure password confirmation and unique username
        database = SQL_Query("AI_Games")
        correctPassword = database.getUserPassword(username)


        if password == correctPassword:
            # Optionally, show a message box confirming user creation
            database.loginUser(username)
            messagebox.showinfo("Login Success", f"{username} logged in!")

        else:
            print(correctPassword)
            messagebox.showinfo("Login Failed", "Incorrect username or password.")

        # close form    
        login_form_window.destroy()

    def logout_user(self):
        # Create a new toplevel window for the user form
        global logout_form_window
        logout_form_window = tk.Toplevel(self.root)
        logout_form_window.title("Logout")

        # Username field
        tk.Label(logout_form_window, text="Username:").grid(row=0, column=0, sticky='w')
        self.username_entry = tk.Entry(logout_form_window)
        self.username_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(logout_form_window, text="Submit", command=self.submit_logout)
        submit_button.grid(row=1, columnspan=2, pady=10)

    def submit_logout(self):
        # Get values from entries
        username = self.username_entry.get()

        # Example: Storing values in variables
        self.username = username

        # log user out
        database = SQL_Query("AI_Games")

        if database.getLoginStatus(username) == "T":
            database.logoutUser(username)
            messagebox.showinfo("Logout Success", f"User {username} logged-out successfully!")
        else:
            messagebox.showinfo("Logout Failed", f"User {username} not logged in.")
        logout_form_window.destroy()    

    # ------------ Game Menu -----------

    def show_rps_game(self):
        self.rps_game = RockPaperScissors(self.root)
        self.rps_game.pack(padx=20, pady=20)