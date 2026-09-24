"""
User Dashboard for Car Saga.
Central navigation hub for all views.
"""

import customtkinter as ctk

from ui.catalogue_view import CatalogueView
from ui.car_details import CarDetailsFrame
from ui.compare_view import CompareView
from ui.find_my_car_view import FindMyCarView
from ui.favourites_view import FavouritesView
from ui.recently_viewed_view import RecentlyViewedView
from ui.shortlist_view import ShortlistView
from ui.saved_searches_view import SavedSearchesView
from services.comparison_service import ComparisonService
from utils.helpers import get_app_logo_image


class UserDashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.pack(fill="both", expand=True)

        self.current_view_name = "catalogue"
        self.catalogue_view_ref = None
        self.nav_buttons = {}

        self.build_shell()
        self.show_catalogue()

    def build_shell(self):
        # Top nav bar
        self.topbar = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e1e1e")
        self.topbar.pack(fill="x", padx=10, pady=(6, 8))

        brand_box = ctk.CTkFrame(self.topbar, fg_color="transparent")
        brand_box.pack(side="left", padx=12, pady=6)

        logo_img = get_app_logo_image(size=(32, 32))
        if logo_img:
            ctk.CTkLabel(brand_box, image=logo_img, text="").pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            brand_box,
            text="Car Saga",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="#e0e0e0",
        ).pack(side="left")

        nav_items = [
            ("catalogue",     "Catalogue"),
            ("favourites",    "Favourites"),
            ("recent",        "Recent"),
            ("compare",       "Compare"),
            ("find_my_car",   "Find My Car"),
            ("shortlist",     "Shortlist"),
            ("saved_searches","Saved"),
        ]

        nav_box = ctk.CTkFrame(self.topbar, fg_color="transparent")
        nav_box.pack(side="left", padx=8)

        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav_box,
                text=label,
                height=30,
                fg_color="transparent",
                hover_color="#2a2a2a",
                text_color="#9e9e9e",
                command=lambda k=key: self.navigate_to(k),
            )
            btn.pack(side="left", padx=2)
            self.nav_buttons[key] = btn

        # Right side
        right_box = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right_box.pack(side="right", padx=14, pady=8)

        user_info = self.app.current_user or {}
        username = user_info.get("username", "User")
        role = user_info.get("role", "USER")

        if role == "ADMIN":
            ctk.CTkButton(
                right_box,
                text="Admin",
                height=30,
                fg_color="#3a3a3a",
                hover_color="#4a4a4a",
                text_color="#e0e0e0",
                command=self.app.show_admin_dashboard,
            ).pack(side="left", padx=6)

        ctk.CTkLabel(
            right_box,
            text=username,
            font=ctk.CTkFont(size=12),
            text_color="#9e9e9e",
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            right_box,
            text="Logout",
            width=70,
            height=30,
            fg_color="#3a2a2a",
            hover_color="#4a2a2a",
            text_color="#cf6679",
            command=self.app.logout,
        ).pack(side="left", padx=4)

        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.update_compare_count()

    def update_compare_count(self):
        if self.app.current_user and "compare" in self.nav_buttons:
            count = ComparisonService.get_comparison_count(self.app.current_user["id"])
            self.nav_buttons["compare"].configure(text=f"Compare ({count}/4)")

    def clear_content(self):
        for child in self.content_container.winfo_children():
            child.destroy()

    def update_active_nav(self, active_key):
        self.current_view_name = active_key
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(fg_color="#3a3a3a", text_color="#e0e0e0")
            else:
                btn.configure(fg_color="transparent", text_color="#9e9e9e")
        self.update_compare_count()

    def navigate_to(self, view_key):
        nav_map = {
            "catalogue":      self.show_catalogue,
            "favourites":     self.show_favourites,
            "recent":         self.show_recently_viewed,
            "compare":        self.show_compare,
            "find_my_car":    self.show_find_my_car,
            "shortlist":      self.show_shortlist,
            "saved_searches": self.show_saved_searches,
        }
        if view_key in nav_map:
            nav_map[view_key]()

    def show_catalogue(self):
        self.clear_content()
        self.update_active_nav("catalogue")
        self.catalogue_view_ref = CatalogueView(self.content_container, self)

    def show_catalogue_with_search(self, criteria):
        self.clear_content()
        self.update_active_nav("catalogue")
        self.catalogue_view_ref = CatalogueView(self.content_container, self)
        self.catalogue_view_ref.apply_saved_search_criteria(criteria)

    def view_car_details(self, car_id):
        self.clear_content()
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent", text_color="#9e9e9e")
        CarDetailsFrame(self.content_container, self, car_id)

    def show_favourites(self):
        self.clear_content()
        self.update_active_nav("favourites")
        FavouritesView(self.content_container, self)

    def show_recently_viewed(self):
        self.clear_content()
        self.update_active_nav("recent")
        RecentlyViewedView(self.content_container, self)

    def show_compare(self):
        self.clear_content()
        self.update_active_nav("compare")
        CompareView(self.content_container, self)

    def show_find_my_car(self):
        self.clear_content()
        self.update_active_nav("find_my_car")
        FindMyCarView(self.content_container, self)

    def show_shortlist(self):
        self.clear_content()
        self.update_active_nav("shortlist")
        ShortlistView(self.content_container, self)

    def show_saved_searches(self):
        self.clear_content()
        self.update_active_nav("saved_searches")
        SavedSearchesView(self.content_container, self)
