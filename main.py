"""
Car Saga — Master Application Entry Point
CBSE Class 12 Computer Science Project.
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from database.connection import initialize_database
from ui.login_register import LoginRegisterFrame


class CarSagaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Car Saga — Automotive Discovery & Selection Platform")
        self.geometry("1320x840")
        self.minsize(1080, 720)

        self.current_user = None

        self.root_container = ctk.CTkFrame(self, fg_color="transparent")
        self.root_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.show_login()

    def clear_root(self):
        for child in self.root_container.winfo_children():
            child.destroy()

    def show_login(self):
        self.clear_root()
        LoginRegisterFrame(self.root_container, self)

    def show_dashboard(self):
        if not self.current_user:
            self.show_login()
            return
        self.clear_root()
        from ui.dashboard import UserDashboardFrame
        UserDashboardFrame(self.root_container, self)

    def show_admin_dashboard(self):
        if not self.current_user or self.current_user.get("role") != "ADMIN":
            messagebox.showwarning("Access Denied", "Administrator privileges required to access this console.")
            self.show_dashboard()
            return
        self.clear_root()
        from ui.admin import AdminDashboardFrame
        AdminDashboardFrame(self.root_container, self)

    def logout(self):
        self.current_user = None
        self.show_login()


if __name__ == "__main__":
    # CustomTkinter theme setup
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    # Safe Database Initialization
    db_initialized = initialize_database()
    if not db_initialized:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Database Connection Error",
            "Could not connect to the local MySQL server on localhost:3306.\n\n"
            "Please ensure MySQL is running with:\n"
            "• User: root\n"
            "• Password: student\n"
            "• Port: 3306\n\n"
            "Start your MySQL service (e.g. via XAMPP or MySQL Server) and relaunch Car Saga.",
        )
        root.destroy()
    else:
        app = CarSagaApp()
        app.mainloop()
