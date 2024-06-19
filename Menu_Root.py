import tkinter as tk
from tkinter import Menu

class Menu_Root:
    def __init__(self, root, actions):
        self.root = root
        self.actions = actions


        # On Shutdown

        self.root.protocol("WM_DELETE_WINDOW", self.actions.on_closing)
        # Configure taskbar
        self.menu_bar = Menu(self.root)

        # Account menu
        self.account_menu = Menu(self.menu_bar, tearoff=0)
        self.account_menu.add_command(label="Login", command=self.actions.login_user)
        self.account_menu.add_command(label="Logout", command=self.actions.logout_user)
        self.account_menu.add_command(label="Create Account", command=self.actions.create_user)
        self.menu_bar.add_cascade(label="Account", menu=self.account_menu)

        # Games menu
        self.games_menu = Menu(self.menu_bar, tearoff=0)
        self.games_menu.add_command(label="Rock, Paper, Scissors", command=self.actions.show_rps_game)
        self.menu_bar.add_cascade(label="Games", menu=self.games_menu)
        

        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.actions.new_file)
        self.file_menu.add_command(label="Open", command=self.actions.open_file)
        self.file_menu.add_command(label="Save", command=self.actions.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Config menu
        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Settings", command=self.actions.open_settings)
        self.menu_bar.add_cascade(label="Config", menu=self.config_menu)

        # Add menu bar to root
        self.root.config(menu=self.menu_bar)