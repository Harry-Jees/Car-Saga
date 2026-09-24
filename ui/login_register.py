"""
Login & Registration screen for Car Saga.
"""

import customtkinter as ctk
from services.auth_service import AuthService
from utils.helpers import get_app_logo_image


class LoginRegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.pack(fill="both", expand=True)

        # Centred card
        self.card = ctk.CTkFrame(self, width=480, corner_radius=18, fg_color="#1e1e1e")
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # App Logo & Title
        logo_img = get_app_logo_image(size=(110, 110))
        if logo_img:
            ctk.CTkLabel(self.card, image=logo_img, text="").pack(pady=(28, 4))
            title_pady = (0, 2)
        else:
            title_pady = (36, 4)

        ctk.CTkLabel(
            self.card,
            text="Car Saga",
            font=ctk.CTkFont(family="Arial", size=28, weight="bold"),
            text_color="#e0e0e0",
        ).pack(pady=title_pady)

        self.subtitle = ctk.CTkLabel(
            self.card,
            text="Sign in to continue",
            font=ctk.CTkFont(size=14),
            text_color="#9e9e9e",
        )
        self.subtitle.pack(pady=(0, 24))

        # Form variables
        self.full_name_var = ctk.StringVar()
        self.username_var = ctk.StringVar()
        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.confirm_var = ctk.StringVar()

        # Fields
        self.full_name_label = ctk.CTkLabel(self.card, text="Full Name", anchor="w", text_color="#9e9e9e")
        self.full_name_entry = ctk.CTkEntry(self.card, placeholder_text="John Doe", textvariable=self.full_name_var, height=38, fg_color="#2a2a2a", border_color="#424242")

        self.username_label = ctk.CTkLabel(self.card, text="Username", anchor="w", text_color="#9e9e9e")
        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="demo", textvariable=self.username_var, height=38, fg_color="#2a2a2a", border_color="#424242")

        self.email_label = ctk.CTkLabel(self.card, text="Email", anchor="w", text_color="#9e9e9e")
        self.email_entry = ctk.CTkEntry(self.card, placeholder_text="you@email.com", textvariable=self.email_var, height=38, fg_color="#2a2a2a", border_color="#424242")

        self.password_label = ctk.CTkLabel(self.card, text="Password", anchor="w", text_color="#9e9e9e")
        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="••••••••", show="*", textvariable=self.password_var, height=38, fg_color="#2a2a2a", border_color="#424242")

        self.confirm_label = ctk.CTkLabel(self.card, text="Confirm Password", anchor="w", text_color="#9e9e9e")
        self.confirm_entry = ctk.CTkEntry(self.card, placeholder_text="••••••••", show="*", textvariable=self.confirm_var, height=38, fg_color="#2a2a2a", border_color="#424242")

        self.submit_btn = ctk.CTkButton(
            self.card,
            text="Sign In",
            height=40,
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            text_color="#e0e0e0",
            command=self.submit,
        )

        self.switch_btn = ctk.CTkButton(
            self.card,
            text="Don't have an account? Register",
            fg_color="transparent",
            hover_color="#2a2a2a",
            text_color="#9e9e9e",
            height=30,
            command=self.toggle_mode,
        )

        self.status_label = ctk.CTkLabel(self.card, text="", text_color="#cf6679", wraplength=330)

        self.demo_hint = ctk.CTkLabel(
            self.card,
            text="Demo: demo / demo123  •  Admin: admin / admin123",
            font=ctk.CTkFont(size=11),
            text_color="#616161",
        )

        self.username_entry.bind("<Return>", lambda e: self.submit())
        self.password_entry.bind("<Return>", lambda e: self.submit())
        self.confirm_entry.bind("<Return>", lambda e: self.submit())

        self.mode = "login"
        self.set_mode("login")

    def toggle_mode(self):
        self.set_mode("register" if self.mode == "login" else "login")

    def set_mode(self, mode):
        self.mode = mode
        self.status_label.configure(text="")

        is_login = mode == "login"
        self.subtitle.configure(text="Sign in to continue" if is_login else "Create a new account")

        # Clear all widgets below subtitle
        for w in [
            self.full_name_label, self.full_name_entry,
            self.email_label, self.email_entry,
            self.username_label, self.username_entry,
            self.password_label, self.password_entry,
            self.confirm_label, self.confirm_entry,
            self.submit_btn, self.switch_btn,
            self.status_label, self.demo_hint,
        ]:
            w.pack_forget()

        px = dict(padx=36)

        if is_login:
            self.username_label.pack(**px, pady=(4, 2), anchor="w")
            self.username_entry.pack(**px, pady=(0, 10), fill="x")
            self.password_label.pack(**px, pady=(4, 2), anchor="w")
            self.password_entry.pack(**px, pady=(0, 16), fill="x")
        else:
            self.full_name_label.pack(**px, pady=(4, 2), anchor="w")
            self.full_name_entry.pack(**px, pady=(0, 8), fill="x")
            self.username_label.pack(**px, pady=(4, 2), anchor="w")
            self.username_entry.pack(**px, pady=(0, 8), fill="x")
            self.email_label.pack(**px, pady=(4, 2), anchor="w")
            self.email_entry.pack(**px, pady=(0, 8), fill="x")
            self.password_label.pack(**px, pady=(4, 2), anchor="w")
            self.password_entry.pack(**px, pady=(0, 8), fill="x")
            self.confirm_label.pack(**px, pady=(4, 2), anchor="w")
            self.confirm_entry.pack(**px, pady=(0, 14), fill="x")

        self.submit_btn.configure(text="Sign In" if is_login else "Register")
        self.submit_btn.pack(**px, pady=(0, 8), fill="x")
        self.switch_btn.configure(text="Don't have an account? Register" if is_login else "Already registered? Sign in")
        self.switch_btn.pack(**px, pady=(0, 4), fill="x")
        self.status_label.pack(**px, pady=(2, 8))
        self.demo_hint.pack(pady=(0, 20))

    def submit(self):
        self.status_label.configure(text="", text_color="#cf6679")

        if self.mode == "login":
            result = AuthService.login(self.username_var.get().strip(), self.password_var.get())
            if result["success"]:
                self.app.current_user = result["user"]
                if result["user"]["role"] == "ADMIN":
                    self.app.show_admin_dashboard()
                else:
                    self.app.show_dashboard()
            else:
                self.status_label.configure(text=result["message"])
        else:
            result = AuthService.register_user(
                self.full_name_var.get(),
                self.username_var.get(),
                self.email_var.get(),
                self.password_var.get(),
                self.confirm_var.get(),
            )
            if result["success"]:
                self.status_label.configure(text=result["message"], text_color="#7cb98a")
                self.set_mode("login")
                self.password_var.set("")
            else:
                self.status_label.configure(text=result["message"])
