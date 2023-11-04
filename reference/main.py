import os
import tkinter as tk
from tkinter import messagebox
from main_window import MainWindow
from db_utils import connect


# Test the database connection
def test_database_connection():
    try:
        connection = connect()
        connection.close()
        return True
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return False


# This MainApp class acts as the primary controller for the GUI application.
class MainApp:
    # Constructor for the MainApp class.
    # Initializes the main application window.
    def __init__(self, root):
        # root is the primary window for the application.
        self.root = root


        # The main_window is an instance of the MainWindow class,
        # which represents the main interface of the application.
        self.main_window = MainWindow(root)

# This is the entry point of the program.
# If this script is run as the main module, the following code will execute.
if __name__ == "__main__":

    if not test_database_connection():
        messagebox.showerror("Error", "Failed to connect to the database. Exiting...")
        exit()
    else:
        print("connected to database")

    # Initialize the primary tkinter window.
    root = tk.Tk()
    # Create an instance of our main application class.
    app = MainApp(root)
    # Start the tkinter event loop.
    # This will display the window and make the program wait for user interactions.
    root.mainloop()
