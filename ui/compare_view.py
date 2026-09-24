"""
Compare View for Car Saga.
Side-by-side specification table for up to 4 cars.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.comparison_service import ComparisonService
from utils.helpers import format_currency, format_efficiency, get_vehicle_placeholder_image


class CompareView(ctk.CTkFrame):
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        user_id = self.app.current_user["id"]
        cars = ComparisonService.get_comparison(user_id)

        top_bar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(4, 8))

        ctk.CTkLabel(top_bar, text=f"Compare — {len(cars)} / 4 cars", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=14, pady=10)

        if cars:
            ctk.CTkButton(top_bar, text="Clear All", width=80, height=30, fg_color="#3a2a2a", hover_color="#4a2a2a", text_color="#cf6679", command=self.clear_all).pack(side="right", padx=14, pady=10)

        if not cars:
            empty = ctk.CTkFrame(self, fg_color="transparent")
            empty.pack(expand=True, pady=60)
            ctk.CTkLabel(empty, text="Your comparison list is empty.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#9e9e9e").pack(pady=(0, 6))
            ctk.CTkLabel(empty, text="Click '+ Comp' on any car card in the catalogue to add cars here.", font=ctk.CTkFont(size=13), text_color="#616161").pack(pady=(0, 16))
            ctk.CTkButton(empty, text="Browse Catalogue", fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", height=34, command=self.dashboard.show_catalogue).pack()
            return

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        spec_keys = [
            ("Price (Ex-Showroom)",  lambda c: format_currency(c["price"])),
            ("Fuel Type",            lambda c: c["fuel"]),
            ("Transmission",         lambda c: c["transmission"]),
            ("Body Style",           lambda c: c["body_type"]),
            ("Engine / Powertrain",  lambda c: c["engine_capacity"] or "Standard"),
            ("Max Power",            lambda c: c["power_kw"] or "N/A"),
            ("Peak Torque",          lambda c: c["torque"] or "N/A"),
            ("Efficiency / Range",   lambda c: format_efficiency(c["fuel"], c["mileage"], c["ev_range"])),
            ("Battery",              lambda c: c["battery_capacity"] if str(c["fuel"]).lower() == "electric" else "N/A"),
            ("Seating",              lambda c: f"{c['seating_capacity']} Seats"),
            ("Boot Space",           lambda c: c["boot_capacity"] or "Standard"),
            ("Ground Clearance",     lambda c: c["ground_clearance"] or "Standard"),
            ("Safety Info",          lambda c: c["safety_info"] or "Standard"),
            ("Key Features",         lambda c: ", ".join(c.get("features", [])) or "Standard Package"),
        ]

        num_cars = len(cars)
        table = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=12)
        table.pack(fill="both", expand=True, padx=4, pady=4)
        table.grid_columnconfigure(0, weight=1, minsize=160)
        for i in range(num_cars):
            table.grid_columnconfigure(i + 1, weight=2, minsize=210)

        # Header row
        ctk.CTkLabel(table, text="Specification", font=ctk.CTkFont(size=13, weight="bold"), text_color="#9e9e9e", anchor="w").grid(row=0, column=0, padx=14, pady=12, sticky="nw")

        for col_idx, car in enumerate(cars):
            head = ctk.CTkFrame(table, fg_color="#2a2a2a", corner_radius=10)
            head.grid(row=0, column=col_idx + 1, padx=6, pady=8, sticky="nsew")

            img = get_vehicle_placeholder_image(car["brand"], car["model"], car["fuel"], width=200, height=95)
            ctk.CTkLabel(head, image=img, text="").pack(padx=6, pady=(6, 2))
            ctk.CTkLabel(head, text=f"{car['brand']} {car['model']}", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e0e0e0").pack(padx=8, pady=(2, 0))
            ctk.CTkLabel(head, text=f"{car['variant']} • {car['model_year']}", font=ctk.CTkFont(size=11), text_color="#616161").pack(padx=8)

            cid = car["id"]
            ctk.CTkButton(head, text="Remove", height=26, width=76, fg_color="#3a2a2a", text_color="#cf6679", hover_color="#4a2a2a", command=lambda c=cid: self.remove_car(c)).pack(pady=(6, 8))

        # Spec rows
        for row_idx, (label, getter) in enumerate(spec_keys, start=1):
            bg = "#1a1a1a" if row_idx % 2 == 0 else "#1e1e1e"

            cell = ctk.CTkFrame(table, fg_color=bg, corner_radius=4)
            cell.grid(row=row_idx, column=0, padx=2, pady=1, sticky="nsew")
            ctk.CTkLabel(cell, text=label, font=ctk.CTkFont(size=12, weight="bold"), text_color="#9e9e9e", anchor="w").pack(fill="x", padx=12, pady=7)

            for col_idx, car in enumerate(cars):
                val_cell = ctk.CTkFrame(table, fg_color=bg, corner_radius=4)
                val_cell.grid(row=row_idx, column=col_idx + 1, padx=2, pady=1, sticky="nsew")
                ctk.CTkLabel(val_cell, text=str(getter(car)), font=ctk.CTkFont(size=12), text_color="#bdbdbd", wraplength=200, anchor="w", justify="left").pack(fill="x", padx=10, pady=7)

    def remove_car(self, car_id):
        ComparisonService.remove_from_comparison(self.app.current_user["id"], car_id)
        self.dashboard.update_compare_count()
        self.refresh()

    def clear_all(self):
        if messagebox.askyesno("Clear Comparison", "Clear your entire comparison list?"):
            ComparisonService.clear_comparison(self.app.current_user["id"])
            self.dashboard.update_compare_count()
            self.refresh()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()
        self.build_ui()
