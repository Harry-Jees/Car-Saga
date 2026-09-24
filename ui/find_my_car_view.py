"""
Find My Car View for Car Saga.
Takes user preferences and shows ranked car recommendations
using a rule-based scoring system.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.recommendation_service import RecommendationService
from services.comparison_service import ComparisonService
from utils.helpers import format_currency, format_efficiency, get_vehicle_placeholder_image


class FindMyCarView(ctk.CTkFrame):
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.run_recommendations()

    def build_ui(self):
        # Header
        banner = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        banner.pack(fill="x", padx=10, pady=(4, 8))
        ctk.CTkLabel(banner, text="Find My Car", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(banner, text="Enter your preferences and we'll rank the best matching cars.", font=ctk.CTkFont(size=12), text_color="#616161").pack(side="left", padx=4)

        # Preferences form
        form_panel = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        form_panel.pack(fill="x", padx=10, pady=(0, 8))

        form_grid = ctk.CTkFrame(form_panel, fg_color="transparent")
        form_grid.pack(fill="x", padx=16, pady=12)
        form_grid.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        opt_style = dict(height=30, fg_color="#2a2a2a", button_color="#3a3a3a", button_hover_color="#4a4a4a")

        def field(parent, col, label, widget_fn):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.grid(row=0, column=col, padx=6, pady=4, sticky="nsew")
            ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="#9e9e9e").pack(anchor="w")
            widget_fn(f)

        self.budget_var = ctk.StringVar(value="1800000")
        field(form_grid, 0, "Max Budget (₹)", lambda f: ctk.CTkEntry(f, textvariable=self.budget_var, height=30, fg_color="#2a2a2a", border_color="#424242").pack(fill="x", pady=(2, 0)))

        self.fuel_var = ctk.StringVar(value="Any")
        field(form_grid, 1, "Fuel", lambda f: ctk.CTkOptionMenu(f, variable=self.fuel_var, values=["Any", "Petrol", "Diesel", "Electric", "Hybrid"], **opt_style).pack(fill="x", pady=(2, 0)))

        self.trans_var = ctk.StringVar(value="Any")
        field(form_grid, 2, "Transmission", lambda f: ctk.CTkOptionMenu(f, variable=self.trans_var, values=["Any", "Automatic", "Manual"], **opt_style).pack(fill="x", pady=(2, 0)))

        self.body_var = ctk.StringVar(value="Any")
        field(form_grid, 3, "Body Style", lambda f: ctk.CTkOptionMenu(f, variable=self.body_var, values=["Any", "SUV", "Sedan", "Hatchback", "MPV"], **opt_style).pack(fill="x", pady=(2, 0)))

        self.seat_var = ctk.StringVar(value="5 Seats")
        field(form_grid, 4, "Min Seating", lambda f: ctk.CTkOptionMenu(f, variable=self.seat_var, values=["Any", "4 Seats", "5 Seats", "7 Seats"], **opt_style).pack(fill="x", pady=(2, 0)))

        # Quick actions
        btn_box = ctk.CTkFrame(form_panel, fg_color="transparent")
        btn_box.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkButton(btn_box, text="Find Matches", font=ctk.CTkFont(size=13, weight="bold"), fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", height=32, width=120, command=self.run_recommendations).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_box, text="Under ₹10L", height=28, fg_color="transparent", border_width=1, border_color="#424242", text_color="#9e9e9e", command=lambda: self.quick_budget("1000000")).pack(side="left", padx=4)
        ctk.CTkButton(btn_box, text="Under ₹15L", height=28, fg_color="transparent", border_width=1, border_color="#424242", text_color="#9e9e9e", command=lambda: self.quick_budget("1500000")).pack(side="left", padx=4)
        ctk.CTkButton(btn_box, text="Under ₹25L", height=28, fg_color="transparent", border_width=1, border_color="#424242", text_color="#9e9e9e", command=lambda: self.quick_budget("2500000")).pack(side="left", padx=4)

        self.results_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.results_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

    def quick_budget(self, amt):
        self.budget_var.set(amt)
        self.run_recommendations()

    def run_recommendations(self):
        for child in self.results_scroll.winfo_children():
            child.destroy()

        seat_raw = self.seat_var.get()
        seating = 5 if "5" in seat_raw else 7 if "7" in seat_raw else 4 if "4" in seat_raw else 0

        criteria = {
            "budget": self.budget_var.get().strip(),
            "fuel": self.fuel_var.get(),
            "transmission": self.trans_var.get(),
            "body_type": self.body_var.get(),
            "seating": seating,
        }

        results = RecommendationService.find_my_car(criteria)
        if not results:
            ctk.CTkLabel(self.results_scroll, text="No matches found. Try relaxing your preferences.", font=ctk.CTkFont(size=15), text_color="#9e9e9e").pack(pady=40)
            return

        user_id = self.app.current_user["id"]

        for item in results:
            car = item["car"]
            match_pct = item["match_percentage"]
            reasons = item["reasons"]

            card = ctk.CTkFrame(self.results_scroll, corner_radius=12, fg_color="#1e1e1e", border_width=1, border_color="#424242")
            card.pack(fill="x", pady=6, padx=4)

            img = get_vehicle_placeholder_image(car["brand"], car["model"], car["fuel"], width=200, height=105)
            ctk.CTkLabel(card, image=img, text="").pack(side="left", padx=10, pady=10)

            center = ctk.CTkFrame(card, fg_color="transparent")
            center.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(center, text=f"{car['brand']} {car['model']}  •  {car['variant']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0").pack(anchor="w")

            eff = format_efficiency(car["fuel"], car["mileage"], car["ev_range"])
            ctk.CTkLabel(center, text=f"{format_currency(car['price'])}  |  {car['fuel']}  |  {car['transmission']}  |  {eff}", font=ctk.CTkFont(size=12), text_color="#9e9e9e", anchor="w").pack(fill="x", pady=(2, 4))

            reasons_row = ctk.CTkFrame(center, fg_color="transparent")
            reasons_row.pack(fill="x")
            for r in reasons[:4]:
                ctk.CTkLabel(reasons_row, text=r, font=ctk.CTkFont(size=11), text_color="#7cb98a").pack(side="left", padx=(0, 10))

            right = ctk.CTkFrame(card, fg_color="transparent", width=130)
            right.pack(side="right", padx=14, pady=10)

            # Match score badge
            score_bg = "#2a3a2a" if match_pct >= 75 else "#2a2a3a" if match_pct >= 50 else "#3a2a2a"
            score_tc = "#7cb98a" if match_pct >= 75 else "#bdbdbd" if match_pct >= 50 else "#cf6679"
            badge = ctk.CTkFrame(right, fg_color=score_bg, corner_radius=8)
            badge.pack(pady=(0, 8))
            ctk.CTkLabel(badge, text=f"{match_pct}% Match", font=ctk.CTkFont(size=12, weight="bold"), text_color=score_tc).pack(padx=10, pady=4)

            cid = car["id"]
            ctk.CTkButton(right, text="View Details", height=28, width=100, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=lambda c=cid: self.dashboard.view_car_details(c)).pack(pady=2)
            ctk.CTkButton(right, text="+ Compare", height=28, width=100, fg_color="#2a2a2a", border_width=1, border_color="#424242", text_color="#9e9e9e", command=lambda c=cid: self.add_compare(c)).pack(pady=2)

    def add_compare(self, car_id):
        res = ComparisonService.add_for_comparison(self.app.current_user["id"], car_id)
        if res["success"]:
            self.dashboard.update_compare_count()
            messagebox.showinfo("Comparison", res["message"])
        else:
            messagebox.showwarning("Comparison", res["message"])
