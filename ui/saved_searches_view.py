"""
Saved Searches View for Car Saga.
Lists saved filter presets that can be re-applied to the catalogue.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.search_service import SearchService
from utils.helpers import format_currency


class SavedSearchesView(ctk.CTkFrame):
    def __init__(self, parent, dashboard):
        super().__init__(parent, fg_color="transparent")
        self.dashboard = dashboard
        self.app = dashboard.app
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        user_id = self.app.current_user["id"]
        searches = SearchService.get_saved_searches(user_id)

        top_bar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        top_bar.pack(fill="x", padx=10, pady=(4, 8))
        ctk.CTkLabel(top_bar, text=f"Saved Searches ({len(searches)})", font=ctk.CTkFont(size=16, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=14, pady=10)
        ctk.CTkLabel(top_bar, text="Saved filter presets you can re-run anytime.", font=ctk.CTkFont(size=12), text_color="#616161").pack(side="left", padx=4)

        if not searches:
            empty = ctk.CTkFrame(self, fg_color="transparent")
            empty.pack(expand=True, pady=60)
            ctk.CTkLabel(empty, text="No saved searches yet.", font=ctk.CTkFont(size=18, weight="bold"), text_color="#9e9e9e").pack(pady=(0, 6))
            ctk.CTkLabel(empty, text="Set up filters in the catalogue and click 'Save Search'.", font=ctk.CTkFont(size=13), text_color="#616161").pack(pady=(0, 16))
            ctk.CTkButton(empty, text="Open Catalogue", fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", height=34, command=self.dashboard.show_catalogue).pack()
            return

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        for item in searches:
            card = ctk.CTkFrame(scroll, corner_radius=12, fg_color="#1e1e1e", border_width=1, border_color="#424242")
            card.pack(fill="x", pady=6, padx=4)

            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True, padx=16, pady=12)

            ctk.CTkLabel(info, text=item["name"], font=ctk.CTkFont(size=15, weight="bold"), text_color="#e0e0e0", anchor="w").pack(fill="x")

            # Build criteria summary
            tags = []
            if item.get("search_text"):  tags.append(f"Keyword: \"{item['search_text']}\"")
            if item.get("brand"):        tags.append(f"Brand: {item['brand']}")
            if item.get("fuel"):         tags.append(f"Fuel: {item['fuel']}")
            if item.get("transmission"): tags.append(f"Transmission: {item['transmission']}")
            if item.get("body_type"):    tags.append(f"Body: {item['body_type']}")
            if item.get("max_price") and float(item["max_price"]) > 0:
                tags.append(f"Max: {format_currency(item['max_price'])}")
            if item.get("min_seating") and int(item["min_seating"]) > 0:
                tags.append(f"Seats: {item['min_seating']}+")

            criteria_str = "  |  ".join(tags) if tags else "All cars (no restrictions)"
            ctk.CTkLabel(info, text=criteria_str, font=ctk.CTkFont(size=12), text_color="#9e9e9e", anchor="w").pack(fill="x", pady=(2, 2))
            ctk.CTkLabel(info, text=f"Saved: {str(item.get('created_at', ''))[:16]}", font=ctk.CTkFont(size=11), text_color="#616161", anchor="w").pack(fill="x")

            right = ctk.CTkFrame(card, fg_color="transparent")
            right.pack(side="right", padx=16, pady=12)

            sid = item["id"]
            ctk.CTkButton(right, text="Load & Apply", width=104, height=30, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=lambda s=item: self.apply_search(s)).pack(side="left", padx=4)
            ctk.CTkButton(right, text="Delete", width=76, height=30, fg_color="#3a2a2a", text_color="#cf6679", hover_color="#4a2a2a", command=lambda s_id=sid: self.delete_search(s_id)).pack(side="left", padx=4)

    def apply_search(self, search_item):
        self.dashboard.show_catalogue_with_search(search_item)

    def delete_search(self, search_id):
        if messagebox.askyesno("Delete", "Delete this saved search?"):
            SearchService.delete_saved_search(self.app.current_user["id"], search_id)
            self.refresh()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()
        self.build_ui()
