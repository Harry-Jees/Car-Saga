"""
Car Details View for Car Saga.
Full specs, features, and user actions for a single car.
Automatically records the view in Recently Viewed.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.car_service import CarService
from services.favourite_service import FavouriteService
from services.comparison_service import ComparisonService
from services.shortlist_service import ShortlistService
from services.recently_viewed_service import RecentlyViewedService
from utils.helpers import format_currency, format_efficiency, get_vehicle_placeholder_image


class CarDetailsFrame(ctk.CTkFrame):
    def __init__(self, parent, dashboard, car_id):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.car_id = car_id
        self.pack(fill="both", expand=True)

        RecentlyViewedService.add_recent_view(self.app.current_user["id"], car_id)
        self.car = CarService.get_car_by_id(car_id)
        self.build_ui()

    def build_ui(self):
        if not self.car:
            ctk.CTkLabel(self, text="Car could not be loaded.", font=ctk.CTkFont(size=18), text_color="#9e9e9e").pack(pady=40)
            ctk.CTkButton(self, text="Back", fg_color="#3a3a3a", text_color="#e0e0e0", command=self.dashboard.show_catalogue).pack()
            return

        user_id = self.app.current_user["id"]
        cid = self.car["id"]

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        toolbar.pack(fill="x", padx=10, pady=(4, 8))

        ctk.CTkButton(toolbar, text="< Back", width=72, height=32, fg_color="#2a2a2a", hover_color="#3a3a3a", text_color="#9e9e9e", command=self.dashboard.show_catalogue).pack(side="left", padx=10, pady=8)

        is_fav = FavouriteService.is_favourite(user_id, cid)
        self.fav_btn = ctk.CTkButton(
            toolbar, text="♥ Favourite", width=108, height=32,
            fg_color="#3a2a2a" if is_fav else "#2a2a2a",
            text_color="#cf6679",
            command=self.toggle_fav,
        )
        self.fav_btn.pack(side="left", padx=6, pady=8)

        ctk.CTkButton(toolbar, text="+ Compare", width=110, height=32, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=self.add_compare).pack(side="left", padx=6, pady=8)

        is_short = ShortlistService.is_shortlisted(user_id, cid)
        self.shortlist_btn = ctk.CTkButton(
            toolbar, text="★ Shortlist", width=108, height=32,
            fg_color="#3a3a2a" if is_short else "#2a2a2a",
            text_color="#bdbdbd",
            command=self.toggle_shortlist,
        )
        self.shortlist_btn.pack(side="left", padx=6, pady=8)

        # Scrollable content
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        # Hero card
        hero = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=14)
        hero.pack(fill="x", pady=(0, 10))

        hero_left = ctk.CTkFrame(hero, fg_color="transparent")
        hero_left.pack(side="left", fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(hero_left, text=f"{self.car['brand']} {self.car['model']}", font=ctk.CTkFont(size=24, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x")
        ctk.CTkLabel(hero_left, text=f"{self.car['variant']} • {self.car['model_year']} • {self.car['body_type']} • {self.car['availability']}", font=ctk.CTkFont(size=13), text_color="#9e9e9e", anchor="w").pack(fill="x", pady=(2, 8))
        ctk.CTkLabel(hero_left, text=f"{format_currency(self.car['price'])} (Ex-Showroom)", font=ctk.CTkFont(size=20, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x")

        hero_img = get_vehicle_placeholder_image(self.car["brand"], self.car["model"], self.car["fuel"], width=280, height=130)
        ctk.CTkLabel(hero, image=hero_img, text="").pack(side="right", padx=16, pady=16)

        # Spec grid (2 columns x 2 rows)
        specs_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        specs_grid.pack(fill="x", pady=(0, 10))
        specs_grid.grid_columnconfigure((0, 1), weight=1, uniform="sc")

        self._spec_section(specs_grid, "Performance & Powertrain", 0, 0, [
            ("Engine / Powertrain", self.car.get("engine_capacity") or "Standard"),
            ("Max Power", self.car.get("power_kw") or "N/A"),
            ("Peak Torque", self.car.get("torque") or "N/A"),
            ("Transmission", self.car.get("transmission")),
        ])

        is_ev = str(self.car.get("fuel", "")).lower() == "electric"
        if is_ev:
            eff_items = [
                ("Fuel", "Pure Electric (EV)"),
                ("Range", f"{int(float(self.car.get('ev_range') or 0))} km"),
                ("Battery", self.car.get("battery_capacity") or "Li-Ion"),
                ("Emissions", "Zero Tailpipe"),
            ]
        else:
            eff_items = [
                ("Fuel", self.car.get("fuel")),
                ("ARAI Mileage", f"{float(self.car.get('mileage') or 0):.2f} km/l"),
                ("Emission Norm", "BS6 Phase 2"),
                ("Fuel Tank", "Standard"),
            ]
        self._spec_section(specs_grid, "Efficiency & Range", 0, 1, eff_items)

        self._spec_section(specs_grid, "Practicality", 1, 0, [
            ("Seating", f"{self.car.get('seating_capacity', 5)} Seats"),
            ("Boot Space", self.car.get("boot_capacity") or "Spacious"),
            ("Ground Clearance", self.car.get("ground_clearance") or "Standard"),
            ("Body Style", self.car.get("body_type")),
        ])

        self._spec_section(specs_grid, "Safety", 1, 1, [
            ("Safety Package", self.car.get("safety_info") or "Standard"),
            ("Braking", "ABS with EBD"),
            ("Airbags", "Multi-Airbag System"),
            ("Structure", "High-Strength Steel"),
        ])

        # Features
        feat_card = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=12)
        feat_card.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(feat_card, text="Key Features", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x", padx=16, pady=(12, 8))

        features_list = self.car.get("features", [])
        if features_list:
            pill_box = ctk.CTkFrame(feat_card, fg_color="transparent")
            pill_box.pack(fill="x", padx=14, pady=(0, 12))
            for feat in features_list:
                pill = ctk.CTkFrame(pill_box, fg_color="#2a2a2a", corner_radius=8)
                pill.pack(side="left", padx=4, pady=4)
                ctk.CTkLabel(pill, text=f"✓ {feat}", font=ctk.CTkFont(size=12), text_color="#9e9e9e").pack(padx=8, pady=4)
        else:
            ctk.CTkLabel(feat_card, text="Standard manufacturer equipment.", font=ctk.CTkFont(size=12), text_color="#616161", anchor="w").pack(fill="x", padx=16, pady=(0, 12))

        # Description
        desc_card = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=12)
        desc_card.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(desc_card, text="Overview", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x", padx=16, pady=(12, 6))
        ctk.CTkLabel(desc_card, text=self.car.get("description") or "No description.", font=ctk.CTkFont(size=13), text_color="#9e9e9e", wraplength=880, justify="left", anchor="w").pack(fill="x", padx=16, pady=(0, 14))

    def _spec_section(self, parent, title, row, col, items):
        frame = ctk.CTkFrame(parent, fg_color="#1e1e1e", corner_radius=12)
        frame.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x", padx=14, pady=(10, 6))
        for label, val in items:
            line = ctk.CTkFrame(frame, fg_color="transparent")
            line.pack(fill="x", padx=14, pady=2)
            ctk.CTkLabel(line, text=label, font=ctk.CTkFont(size=12), text_color="#616161", anchor="w", width=130).pack(side="left")
            ctk.CTkLabel(line, text=str(val), font=ctk.CTkFont(size=12, weight="bold"), text_color="#bdbdbd", anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(frame, text="", height=4).pack()

    def toggle_fav(self):
        user_id = self.app.current_user["id"]
        cid = self.car["id"]
        if FavouriteService.is_favourite(user_id, cid):
            FavouriteService.remove_favourite(user_id, cid)
            self.fav_btn.configure(fg_color="#2a2a2a")
        else:
            FavouriteService.add_favourite(user_id, cid)
            self.fav_btn.configure(fg_color="#3a2a2a")

    def toggle_shortlist(self):
        user_id = self.app.current_user["id"]
        cid = self.car["id"]
        if ShortlistService.is_shortlisted(user_id, cid):
            ShortlistService.remove_from_shortlist(user_id, cid)
            self.shortlist_btn.configure(fg_color="#2a2a2a")
        else:
            ShortlistService.add_to_shortlist(user_id, cid)
            self.shortlist_btn.configure(fg_color="#3a3a2a")

    def add_compare(self):
        res = ComparisonService.add_for_comparison(self.app.current_user["id"], self.car["id"])
        if res["success"]:
            self.dashboard.update_compare_count()
            messagebox.showinfo("Comparison", res["message"])
        else:
            messagebox.showwarning("Comparison", res["message"])
