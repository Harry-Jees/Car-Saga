"""
Catalogue View for Car Saga.
Search, filter, sort and browse cars with pagination.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.car_service import CarService
from services.favourite_service import FavouriteService
from services.comparison_service import ComparisonService
from services.shortlist_service import ShortlistService
from services.search_service import SearchService
from utils.helpers import format_currency, format_efficiency, get_vehicle_placeholder_image


class CatalogueView(ctk.CTkFrame):
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.pack(fill="both", expand=True)

        self.current_page = 1
        self.page_size = 6
        self.active_filters = {}
        self.current_sort = "price_asc"

        self.build_ui()
        self.load_cars()

    def build_ui(self):
        # Search bar
        top_bar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(4, 6))

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search brand, model, body type...",
            textvariable=self.search_var,
            width=300,
            height=34,
            fg_color="#2a2a2a",
            border_color="#424242",
        )
        self.search_entry.pack(side="left", padx=(10, 6), pady=8)
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        ctk.CTkButton(top_bar, text="Search", width=76, height=34, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=self.on_search).pack(side="left", padx=4)
        ctk.CTkButton(top_bar, text="Clear", width=60, height=34, fg_color="transparent", border_width=1, border_color="#424242", text_color="#9e9e9e", command=self.on_reset).pack(side="left", padx=4)
        ctk.CTkButton(top_bar, text="Save Search", width=100, height=34, fg_color="#2a2a2a", border_width=1, border_color="#424242", text_color="#9e9e9e", command=self.open_save_search_dialog).pack(side="left", padx=8)

        # Sort
        sort_box = ctk.CTkFrame(top_bar, fg_color="transparent")
        sort_box.pack(side="right", padx=10)
        ctk.CTkLabel(sort_box, text="Sort:", font=ctk.CTkFont(size=12), text_color="#9e9e9e").pack(side="left", padx=4)
        self.sort_options = {
            "Price: Low to High": "price_asc",
            "Price: High to Low": "price_desc",
            "Model: A to Z":      "name_asc",
            "Model: Z to A":      "name_desc",
            "Newest Year":        "year_desc",
            "Best Mileage":       "mileage_desc",
            "Highest EV Range":   "ev_range_desc",
        }
        self.sort_var = ctk.StringVar(value="Price: Low to High")
        ctk.CTkOptionMenu(
            sort_box,
            variable=self.sort_var,
            values=list(self.sort_options.keys()),
            command=self.on_sort_change,
            width=165,
            height=32,
            fg_color="#2a2a2a",
            button_color="#3a3a3a",
            button_hover_color="#4a4a4a",
        ).pack(side="left", padx=4)

        # Filter bar
        filter_bar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        filter_bar.pack(fill="x", padx=10, pady=(0, 8))

        opt_style = dict(height=30, fg_color="#2a2a2a", button_color="#3a3a3a", button_hover_color="#4a4a4a")

        brands = ["All Brands"] + CarService.get_brands()
        self.brand_var = ctk.StringVar(value="All Brands")
        ctk.CTkOptionMenu(filter_bar, variable=self.brand_var, values=brands, width=128, command=lambda v: self.apply_filters(), **opt_style).pack(side="left", padx=6, pady=8)

        fuels = ["All Fuels"] + CarService.get_fuel_types()
        self.fuel_var = ctk.StringVar(value="All Fuels")
        ctk.CTkOptionMenu(filter_bar, variable=self.fuel_var, values=fuels, width=110, command=lambda v: self.apply_filters(), **opt_style).pack(side="left", padx=6)

        trans = ["All Transmissions"] + CarService.get_transmissions()
        self.trans_var = ctk.StringVar(value="All Transmissions")
        ctk.CTkOptionMenu(filter_bar, variable=self.trans_var, values=trans, width=132, command=lambda v: self.apply_filters(), **opt_style).pack(side="left", padx=6)

        bodies = ["All Body Types"] + CarService.get_body_types()
        self.body_var = ctk.StringVar(value="All Body Types")
        ctk.CTkOptionMenu(filter_bar, variable=self.body_var, values=bodies, width=122, command=lambda v: self.apply_filters(), **opt_style).pack(side="left", padx=6)

        self.max_price_var = ctk.StringVar()
        ctk.CTkEntry(filter_bar, placeholder_text="Max Price (₹)", textvariable=self.max_price_var, width=120, height=30, fg_color="#2a2a2a", border_color="#424242").pack(side="left", padx=6)

        seats_opts = ["Any Seats", "4+ Seats", "5+ Seats", "7+ Seats"]
        self.seats_var = ctk.StringVar(value="Any Seats")
        ctk.CTkOptionMenu(filter_bar, variable=self.seats_var, values=seats_opts, width=108, command=lambda v: self.apply_filters(), **opt_style).pack(side="left", padx=6)

        ctk.CTkButton(filter_bar, text="Filter", width=66, height=30, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=self.apply_filters).pack(side="left", padx=6)

        # Car grid
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        # Pagination
        self.pagination_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10, height=42)
        self.pagination_frame.pack(fill="x", padx=10, pady=(0, 4))

        self.prev_btn = ctk.CTkButton(self.pagination_frame, text="< Prev", width=80, height=28, fg_color="#2a2a2a", hover_color="#3a3a3a", text_color="#9e9e9e", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=12, pady=6)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Page 1 of 1", font=ctk.CTkFont(size=12), text_color="#9e9e9e")
        self.page_label.pack(side="left", expand=True)

        self.next_btn = ctk.CTkButton(self.pagination_frame, text="Next >", width=80, height=28, fg_color="#2a2a2a", hover_color="#3a3a3a", text_color="#9e9e9e", command=self.next_page)
        self.next_btn.pack(side="right", padx=12, pady=6)

    def on_search(self):
        self.current_page = 1
        self.apply_filters()

    def on_reset(self):
        self.search_var.set("")
        self.brand_var.set("All Brands")
        self.fuel_var.set("All Fuels")
        self.trans_var.set("All Transmissions")
        self.body_var.set("All Body Types")
        self.max_price_var.set("")
        self.seats_var.set("Any Seats")
        self.sort_var.set("Price: Low to High")
        self.current_sort = "price_asc"
        self.current_page = 1
        self.active_filters = {}
        self.load_cars()

    def on_sort_change(self, choice):
        self.current_sort = self.sort_options.get(choice, "price_asc")
        self.current_page = 1
        self.load_cars()

    def apply_filters(self):
        filters = {}
        s = self.search_var.get().strip()
        if s:
            filters["search"] = s
        if self.brand_var.get() != "All Brands":
            filters["brand"] = self.brand_var.get()
        if self.fuel_var.get() != "All Fuels":
            filters["fuel"] = self.fuel_var.get()
        if self.trans_var.get() != "All Transmissions":
            filters["transmission"] = self.trans_var.get()
        if self.body_var.get() != "All Body Types":
            filters["body_type"] = self.body_var.get()

        p = self.max_price_var.get().strip()
        if p:
            try:
                filters["max_price"] = float(p)
            except ValueError:
                pass

        seats_val = self.seats_var.get()
        if "4" in seats_val:
            filters["min_seating"] = 4
        elif "5" in seats_val:
            filters["min_seating"] = 5
        elif "7" in seats_val:
            filters["min_seating"] = 7

        self.active_filters = filters
        self.current_page = 1
        self.load_cars()

    def load_cars(self):
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        result = CarService.get_catalogue(
            filters=self.active_filters,
            sort_by=self.current_sort,
            page=self.current_page,
            page_size=self.page_size,
        )

        cars = result["cars"]
        total = result["total"]
        total_pages = result["total_pages"]

        self.page_label.configure(text=f"Page {self.current_page} of {total_pages}  ({total} cars)")
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(state="normal" if self.current_page < total_pages else "disabled")

        if not cars:
            box = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            box.pack(pady=60)
            ctk.CTkLabel(box, text="No cars match your filters.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#9e9e9e").pack(pady=(0, 8))
            ctk.CTkButton(box, text="Reset Filters", fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=self.on_reset).pack()
            return

        grid = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

        user_id = self.app.current_user["id"]

        for idx, car in enumerate(cars):
            row, col = idx // 3, idx % 3

            card = ctk.CTkFrame(grid, corner_radius=12, fg_color="#1e1e1e", border_width=1, border_color="#424242")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            img = get_vehicle_placeholder_image(car["brand"], car["model"], car["fuel"], width=260, height=120)
            ctk.CTkLabel(card, image=img, text="").pack(fill="x", padx=6, pady=(6, 4))

            ctk.CTkLabel(card, text=f"{car['brand']} {car['model']}", font=ctk.CTkFont(size=15, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x", padx=12, pady=(2, 0))
            ctk.CTkLabel(card, text=f"{car['variant']} • {car['model_year']}", font=ctk.CTkFont(size=11), text_color="#9e9e9e", anchor="w").pack(fill="x", padx=12)
            ctk.CTkLabel(card, text=format_currency(car["price"]), font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x", padx=12, pady=(4, 2))

            eff = format_efficiency(car["fuel"], car["mileage"], car["ev_range"])
            ctk.CTkLabel(card, text=f"{car['fuel']} | {car['transmission']} | {eff}", font=ctk.CTkFont(size=11), text_color="#616161", anchor="w").pack(fill="x", padx=12, pady=(0, 6))

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=10, pady=(4, 10))

            cid = car["id"]
            ctk.CTkButton(btn_row, text="Details", width=72, height=28, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=lambda c=cid: self.dashboard.view_car_details(c)).pack(side="left", padx=2)

            is_fav = FavouriteService.is_favourite(user_id, cid)
            ctk.CTkButton(btn_row, text="♥" if is_fav else "♡", width=32, height=28, font=ctk.CTkFont(size=15), fg_color="#3a2a2a" if is_fav else "#2a2a2a", text_color="#cf6679", command=lambda c=cid: self.toggle_fav(c)).pack(side="left", padx=2)

            ctk.CTkButton(btn_row, text="+ Comp", width=62, height=28, fg_color="#2a2a2a", text_color="#9e9e9e", border_width=1, border_color="#424242", command=lambda c=cid: self.add_compare(c)).pack(side="left", padx=2)

            is_short = ShortlistService.is_shortlisted(user_id, cid)
            ctk.CTkButton(btn_row, text="★" if is_short else "☆", width=32, height=28, font=ctk.CTkFont(size=14), fg_color="#3a3a2a" if is_short else "#2a2a2a", text_color="#bdbdbd", command=lambda c=cid: self.toggle_shortlist(c)).pack(side="left", padx=2)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_cars()

    def next_page(self):
        self.current_page += 1
        self.load_cars()

    def toggle_fav(self, car_id):
        user_id = self.app.current_user["id"]
        if FavouriteService.is_favourite(user_id, car_id):
            FavouriteService.remove_favourite(user_id, car_id)
        else:
            FavouriteService.add_favourite(user_id, car_id)
        self.load_cars()

    def toggle_shortlist(self, car_id):
        user_id = self.app.current_user["id"]
        if ShortlistService.is_shortlisted(user_id, car_id):
            ShortlistService.remove_from_shortlist(user_id, car_id)
        else:
            ShortlistService.add_to_shortlist(user_id, car_id)
        self.load_cars()

    def add_compare(self, car_id):
        user_id = self.app.current_user["id"]
        res = ComparisonService.add_for_comparison(user_id, car_id)
        if res["success"]:
            self.dashboard.update_compare_count()
            messagebox.showinfo("Comparison", res["message"])
        else:
            messagebox.showwarning("Comparison", res["message"])

    def open_save_search_dialog(self):
        dialog = ctk.CTkInputDialog(text="Name for this saved search:", title="Save Search")
        name = dialog.get_input()
        if name and name.strip():
            res = SearchService.save_search(self.app.current_user["id"], name.strip(), self.active_filters)
            if res["success"]:
                messagebox.showinfo("Saved", res["message"])
            else:
                messagebox.showerror("Error", res["message"])

    def apply_saved_search_criteria(self, criteria):
        self.search_var.set(criteria.get("search_text", "") or "")
        self.brand_var.set(criteria.get("brand", "") or "All Brands")
        self.fuel_var.set(criteria.get("fuel", "") or "All Fuels")
        self.trans_var.set(criteria.get("transmission", "") or "All Transmissions")
        self.body_var.set(criteria.get("body_type", "") or "All Body Types")
        max_p = criteria.get("max_price", 0)
        self.max_price_var.set(str(int(max_p)) if max_p and float(max_p) > 0 else "")
        min_s = criteria.get("min_seating", 0)
        seat_map = {7: "7+ Seats", 5: "5+ Seats", 4: "4+ Seats"}
        self.seats_var.set(seat_map.get(min_s, "Any Seats"))
        self.apply_filters()
