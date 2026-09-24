"""
Shortlist View for Car Saga.
Shows cars the user has starred for their prospective purchase.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.shortlist_service import ShortlistService
from services.comparison_service import ComparisonService
from utils.helpers import format_currency, format_efficiency, get_vehicle_placeholder_image


class ShortlistView(ctk.CTkFrame):
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        user_id = self.app.current_user["id"]
        cars = ShortlistService.get_shortlist(user_id)

        top_bar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(4, 8))
        ctk.CTkLabel(top_bar, text=f"Shortlist ({len(cars)})", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(top_bar, text="Cars shortlisted for your purchase decision.", font=ctk.CTkFont(size=12), text_color="#616161").pack(side="left", padx=4)

        if not cars:
            empty = ctk.CTkFrame(self, fg_color="transparent")
            empty.pack(expand=True, pady=60)
            ctk.CTkLabel(empty, text="Your shortlist is empty.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#9e9e9e").pack(pady=(0, 6))
            ctk.CTkLabel(empty, text="Click ★ on any car to add it to your shortlist.", font=ctk.CTkFont(size=13), text_color="#616161").pack(pady=(0, 16))
            ctk.CTkButton(empty, text="Explore Catalogue", fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", height=34, command=self.dashboard.show_catalogue).pack()
            return

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        for car in cars:
            card = ctk.CTkFrame(scroll, corner_radius=12, fg_color="#1e1e1e", border_width=1, border_color="#424242")
            card.pack(fill="x", pady=6, padx=4)

            img = get_vehicle_placeholder_image(car["brand"], car["model"], car["fuel"], width=180, height=95)
            ctk.CTkLabel(card, image=img, text="").pack(side="left", padx=12, pady=10)

            center = ctk.CTkFrame(card, fg_color="transparent")
            center.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            ctk.CTkLabel(center, text=f"{car['brand']} {car['model']}  •  {car['variant']}", font=ctk.CTkFont(size=15, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x")

            eff = format_efficiency(car["fuel"], car["mileage"], car["ev_range"])
            ctk.CTkLabel(center, text=f"{format_currency(car['price'])}  |  {car['fuel']}  |  {car['transmission']}  |  {eff}", font=ctk.CTkFont(size=12), text_color="#9e9e9e", anchor="w").pack(fill="x", pady=(2, 2))
            ctk.CTkLabel(center, text=f"Shortlisted: {str(car.get('shortlisted_on', ''))[:16]}", font=ctk.CTkFont(size=11), text_color="#616161", anchor="w").pack(fill="x")

            right = ctk.CTkFrame(card, fg_color="transparent", width=110)
            right.pack(side="right", padx=14, pady=10)

            cid = car["id"]
            ctk.CTkButton(right, text="Details", width=96, height=28, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=lambda c=cid: self.dashboard.view_car_details(c)).pack(pady=2)
            ctk.CTkButton(right, text="+ Compare", width=96, height=28, fg_color="#2a2a2a", border_width=1, border_color="#424242", text_color="#9e9e9e", command=lambda c=cid: self.add_compare(c)).pack(pady=2)
            ctk.CTkButton(right, text="Remove", width=96, height=28, fg_color="#3a2a2a", text_color="#cf6679", hover_color="#4a2a2a", command=lambda c=cid: self.remove_car(c)).pack(pady=2)

    def remove_car(self, car_id):
        ShortlistService.remove_from_shortlist(self.app.current_user["id"], car_id)
        self.refresh()

    def add_compare(self, car_id):
        res = ComparisonService.add_for_comparison(self.app.current_user["id"], car_id)
        if res["success"]:
            self.dashboard.update_compare_count()
            messagebox.showinfo("Comparison", res["message"])
        else:
            messagebox.showwarning("Comparison", res["message"])

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()
        self.build_ui()
