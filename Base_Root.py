import tkinter as tk
from Menu_Root import Menu_Root
from Menu_Actions import Menu_Actions


class Base_Root:
    def __init__(self, root):
        self.root = root
        MAIN_TITLE = "GAME HUB"
        self.root.title(MAIN_TITLE)

        # Main landing page (could be any widget)
        MAIN_HEIGHT = 300
        MAIN_WIDTH = 500

        
        self.root.geometry(f"{MAIN_WIDTH}x{MAIN_HEIGHT}")

        # Create the menu actions
        self.menu_actions = Menu_Actions(self.root)
        
        # Create the menu options
        self.menu_options = Menu_Root(self.root, self.menu_actions)

