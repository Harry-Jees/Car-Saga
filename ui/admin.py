"""
Admin Dashboard View for Car Saga.
Provides live database statistics, complete Car CRUD operations (Add/Edit/Status/Delete),
user roster inspection, and catalogue metadata management.
"""

import customtkinter as ctk
from tkinter import messagebox

from services.admin_service import AdminService
from services.car_service import CarService
from utils.helpers import format_currency, get_app_logo_image
from utils.validators import validate_year, validate_positive_number, validate_seating


class AdminDashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.pack(fill="both", expand=True)

        self.current_tab = "cars"
        self.build_ui()

    def build_ui(self):
        # 1. Top Navbar
        navbar = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        navbar.pack(fill="x", padx=10, pady=(6, 8))

        brand_box = ctk.CTkFrame(navbar, fg_color="transparent")
        brand_box.pack(side="left", padx=12, pady=6)

        logo_img = get_app_logo_image(size=(32, 32))
        if logo_img:
            ctk.CTkLabel(brand_box, image=logo_img, text="").pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            brand_box,
            text="Admin Console",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color="#e0e0e0",
        ).pack(side="left")

        # Tab Navigation Buttons
        tab_box = ctk.CTkFrame(navbar, fg_color="transparent")
        tab_box.pack(side="left", padx=10)

        self.tab_buttons = {}
        for tab_id, tab_label in [
            ("cars", "🚗 Manage Cars"),
            ("users", "👥 Registered Users"),
            ("metadata", "🏷️ Catalogue Data"),
        ]:
            btn = ctk.CTkButton(
                tab_box,
                text=tab_label,
                height=30,
                fg_color="#3a3a3a" if self.current_tab == tab_id else "transparent",
                hover_color="#2a2a2a",
                text_color="#e0e0e0" if self.current_tab == tab_id else "#9e9e9e",
                command=lambda t=tab_id: self.switch_tab(t),
            )
            btn.pack(side="left", padx=4)
            self.tab_buttons[tab_id] = btn

        # Switch to User View & Logout
        ctk.CTkButton(
            navbar,
            text="Logout",
            width=76,
            height=30,
            fg_color="#3a2a2a",
            hover_color="#4a2a2a",
            text_color="#cf6679",
            command=self.app.logout,
        ).pack(side="right", padx=(6, 14), pady=12)

        ctk.CTkButton(
            navbar,
            text="User View",
            width=84,
            height=30,
            fg_color="#2a2a2a",
            hover_color="#3a3a3a",
            text_color="#9e9e9e",
            command=self.app.show_dashboard,
        ).pack(side="right", padx=6, pady=12)

        # 2. Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=(0, 6))

        self.render_current_tab()

    def switch_tab(self, tab_id):
        self.current_tab = tab_id
        for t, btn in self.tab_buttons.items():
            btn.configure(
                fg_color="#3a3a3a" if t == tab_id else "transparent",
                text_color="#e0e0e0" if t == tab_id else "#9e9e9e",
            )
        self.render_current_tab()

    def clear_main(self):
        for child in self.main_container.winfo_children():
            child.destroy()

    def render_current_tab(self):
        self.clear_main()
        if self.current_tab == "cars":
            self.render_cars_tab()
        elif self.current_tab == "users":
            self.render_users_tab()
        elif self.current_tab == "metadata":
            self.render_metadata_tab()

    # =========================================================================
    # TAB 1: MANAGE CARS & STATS
    # =========================================================================
    def render_cars_tab(self):
        # Stats KPI Cards Banner
        stats = AdminService.get_dashboard_stats()

        kpi_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=(0, 10))
        kpi_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        kpi_data = [
            ("Total Cars",     stats["total_cars"],     "#9e9e9e"),
            ("Active Cars",    stats["active_cars"],    "#bdbdbd"),
            ("Users",          stats["total_users"],    "#9e9e9e"),
            ("Brands",         stats["total_brands"],   "#bdbdbd"),
            ("Favourites",     stats["total_favourites"], "#9e9e9e"),
            ("Saved Searches", stats["total_searches"], "#bdbdbd"),
        ]

        for idx, (label, val, accent) in enumerate(kpi_data):
            c = ctk.CTkFrame(kpi_frame, fg_color="#1e1e1e", corner_radius=12)
            c.grid(row=0, column=idx, padx=4, sticky="nsew")
            ctk.CTkLabel(c, text=label, font=ctk.CTkFont(size=11), text_color="#616161").pack(pady=(8, 0))
            ctk.CTkLabel(c, text=str(val), font=ctk.CTkFont(size=20, weight="bold"), text_color=accent).pack(pady=(0, 8))

        # Action bar
        action_bar = ctk.CTkFrame(self.main_container, fg_color="#1e1e1e", corner_radius=10)
        action_bar.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(action_bar, text="Vehicle Inventory", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=12, pady=8)

        ctk.CTkButton(
            action_bar,
            text="+ Add New Car",
            height=30,
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            text_color="#e0e0e0",
            command=self.open_add_car_dialog,
        ).pack(side="right", padx=12, pady=8)

        # Cars Table (Scrollable)
        table_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        table_scroll.pack(fill="both", expand=True)

        cars = AdminService.get_all_cars()
        if not cars:
            ctk.CTkLabel(table_scroll, text="No cars registered in catalogue.", font=ctk.CTkFont(size=16)).pack(pady=40)
            return

        # Table Header
        header_row = ctk.CTkFrame(table_scroll, fg_color="#2a2a2a", corner_radius=8, height=36)
        header_row.pack(fill="x", pady=(0, 4))
        header_row.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        cols = ["ID", "Brand & Model", "Variant", "Year", "Fuel", "Price", "Status", "Actions"]
        for i, col in enumerate(cols):
            ctk.CTkLabel(header_row, text=col, font=ctk.CTkFont(size=12, weight="bold"), text_color="#9e9e9e").grid(row=0, column=i, padx=6, pady=6)

        # Table Rows
        for car in cars:
            row = ctk.CTkFrame(table_scroll, fg_color="#1e1e1e", corner_radius=8)
            row.pack(fill="x", pady=2)
            row.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

            cid = car["id"]
            ctk.CTkLabel(row, text=str(cid), font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=6, pady=8)
            ctk.CTkLabel(row, text=f"{car['brand']} {car['model']}", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, padx=6, pady=8)
            ctk.CTkLabel(row, text=car["variant"] or "-", font=ctk.CTkFont(size=12)).grid(row=0, column=2, padx=6, pady=8)
            ctk.CTkLabel(row, text=str(car["model_year"]), font=ctk.CTkFont(size=12)).grid(row=0, column=3, padx=6, pady=8)
            ctk.CTkLabel(row, text=car["fuel"], font=ctk.CTkFont(size=12)).grid(row=0, column=4, padx=6, pady=8)
            ctk.CTkLabel(row, text=format_currency(car["price"]), font=ctk.CTkFont(size=12, weight="bold"), text_color="#bdbdbd").grid(row=0, column=5, padx=6, pady=8)

            # Status Badge
            is_act = car["is_active"] == 1
            status_text = "Active" if is_act else "Inactive"
            status_color = "#7cb98a" if is_act else "#cf6679"
            ctk.CTkLabel(row, text=status_text, font=ctk.CTkFont(size=12, weight="bold"), text_color=status_color).grid(row=0, column=6, padx=6, pady=8)

            # Actions Cell
            act_box = ctk.CTkFrame(row, fg_color="transparent")
            act_box.grid(row=0, column=7, padx=6, pady=4)

            ctk.CTkButton(act_box, text="Edit", width=44, height=26, fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#e0e0e0", command=lambda c=car: self.open_edit_car_dialog(c)).pack(side="left", padx=2)
            ctk.CTkButton(act_box, text="Deactivate" if is_act else "Activate", width=70, height=26, fg_color="#2a3a2a" if is_act else "#3a2a2a", text_color="#7cb98a" if is_act else "#cf6679", command=lambda c_id=cid: self.toggle_status(c_id)).pack(side="left", padx=2)
            ctk.CTkButton(act_box, text="Delete", width=50, height=26, fg_color="#3a2a2a", hover_color="#4a2a2a", text_color="#cf6679", command=lambda c_id=cid: self.delete_car(c_id)).pack(side="left", padx=2)

    def toggle_status(self, car_id):
        res = AdminService.toggle_car_status(car_id)
        if res["success"]:
            self.render_cars_tab()
        else:
            messagebox.showerror("Error", res["message"])

    def delete_car(self, car_id):
        if messagebox.askyesno("Delete Car", "Are you sure you want to permanently delete this car from the database?"):
            res = AdminService.delete_car(car_id)
            if res["success"]:
                self.render_cars_tab()
            else:
                messagebox.showerror("Error", res["message"])

    # =========================================================================
    # TAB 2: REGISTERED USERS
    # =========================================================================
    def render_users_tab(self):
        users = AdminService.get_users()

        header_bar = ctk.CTkFrame(self.main_container, fg_color="#1e1e1e", corner_radius=10)
        header_bar.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(header_bar, text=f"Registered Users ({len(users)})", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e0e0e0").pack(side="left", padx=12, pady=8)

        table_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        table_scroll.pack(fill="both", expand=True)

        # Header Row
        header_row = ctk.CTkFrame(table_scroll, fg_color="#2a2a2a", corner_radius=8, height=36)
        header_row.pack(fill="x", pady=(0, 4))
        header_row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        cols = ["ID", "Full Name", "Username", "Email", "Role", "Registered"]
        for i, col in enumerate(cols):
            ctk.CTkLabel(header_row, text=col, font=ctk.CTkFont(size=12, weight="bold"), text_color="#9e9e9e").grid(row=0, column=i, padx=8, pady=6)

        for u in users:
            row = ctk.CTkFrame(table_scroll, fg_color="#1e1e1e", corner_radius=8)
            row.pack(fill="x", pady=2)
            row.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

            ctk.CTkLabel(row, text=str(u["id"]), text_color="#9e9e9e").grid(row=0, column=0, padx=8, pady=8)
            ctk.CTkLabel(row, text=u["full_name"], font=ctk.CTkFont(weight="bold"), text_color="#e0e0e0").grid(row=0, column=1, padx=8, pady=8)
            ctk.CTkLabel(row, text=u["username"], text_color="#9e9e9e").grid(row=0, column=2, padx=8, pady=8)
            ctk.CTkLabel(row, text=u["email"], text_color="#9e9e9e").grid(row=0, column=3, padx=8, pady=8)

            role_col = "#e0e0e0" if u["role_name"] == "ADMIN" else "#616161"
            ctk.CTkLabel(row, text=u["role_name"], font=ctk.CTkFont(weight="bold"), text_color=role_col).grid(row=0, column=4, padx=8, pady=8)

            dt = str(u.get("created_at", ""))[:16]
            ctk.CTkLabel(row, text=dt).grid(row=0, column=5, padx=8, pady=8)

    # =========================================================================
    # TAB 3: CATALOGUE DATA MANAGER
    # =========================================================================
    def render_metadata_tab(self):
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scroll,
            text="Add New Catalogue Master Data",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(anchor="w", pady=(0, 12))

        sections = [
            ("Add New Brand", "brands", "e.g. Volkswagen, Ford, Audi"),
            ("Add New Body Type", "body_types", "e.g. Convertible, Coupe, Pickup"),
            ("Add New Fuel Type", "fuel_types", "e.g. CNG, Hydrogen"),
            ("Add New Transmission", "transmission_types", "e.g. Dual-Clutch, CVT"),
            ("Add New Feature", "features", "e.g. 360 Degree Camera, HUD"),
        ]

        for title, tbl, hint in sections:
            card = ctk.CTkFrame(scroll, fg_color="#1e1e1e", corner_radius=12)
            card.pack(fill="x", pady=6)

            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color="#e0e0e0").pack(anchor="w", padx=16, pady=(10, 4))

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(0, 12))

            var = ctk.StringVar()
            entry = ctk.CTkEntry(row, placeholder_text=hint, textvariable=var, width=320, height=32, fg_color="#2a2a2a", border_color="#424242")
            entry.pack(side="left", padx=(0, 8))

            ctk.CTkButton(
                row,
                text="Add",
                height=32,
                width=90,
                fg_color="#3a3a3a",
                hover_color="#4a4a4a",
                text_color="#e0e0e0",
                command=lambda t=tbl, v=var: self.add_metadata_item(t, v),
            ).pack(side="left")

    def add_metadata_item(self, table_name, str_var):
        val = str_var.get().strip()
        if not val:
            messagebox.showwarning("Input Needed", "Please enter a valid item name.")
            return

        res = AdminService.add_catalogue_item(table_name, val)
        if res["success"]:
            messagebox.showinfo("Success", res["message"])
            str_var.set("")
        else:
            messagebox.showerror("Error", res["message"])

    # =========================================================================
    # ADD / EDIT CAR MODAL POPUP
    # =========================================================================
    def open_add_car_dialog(self):
        self.show_car_form_window(mode="add")

    def open_edit_car_dialog(self, car):
        # Fetch complete car with features
        full_car = CarService.get_car_by_id(car["id"])
        self.show_car_form_window(mode="edit", car_data=full_car)

    def show_car_form_window(self, mode="add", car_data=None):
        win = ctk.CTkToplevel(self)
        win.title("Add New Car" if mode == "add" else f"Edit Car — {car_data['model']}")
        win.geometry("780x740")
        win.minsize(700, 600)
        win.grab_set()

        scroll = ctk.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        meta = AdminService.get_metadata_ids()
        brand_map = {b["name"]: b["id"] for b in meta["brands"]}
        fuel_map = {f["name"]: f["id"] for f in meta["fuels"]}
        trans_map = {t["name"]: t["id"] for t in meta["transmissions"]}
        body_map = {bt["name"]: bt["id"] for bt in meta["bodies"]}

        ctk.CTkLabel(
            scroll,
            text="Vehicle Information Form" if mode == "add" else f"Editing Car #{car_data['id']}: {car_data['model']}",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", pady=(0, 14))

        # Form fields
        entries = {}

        def add_field(label, key, default=""):
            box = ctk.CTkFrame(scroll, fg_color="transparent")
            box.pack(fill="x", pady=4)
            ctk.CTkLabel(box, text=label, width=160, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
            var = ctk.StringVar(value=str(default))
            ent = ctk.CTkEntry(box, textvariable=var, height=32)
            ent.pack(side="left", fill="x", expand=True)
            entries[key] = var
            return var

        def add_dropdown(label, key, options, default=""):
            box = ctk.CTkFrame(scroll, fg_color="transparent")
            box.pack(fill="x", pady=4)
            ctk.CTkLabel(box, text=label, width=160, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")
            var = ctk.StringVar(value=default if default in options else options[0])
            menu = ctk.CTkOptionMenu(box, variable=var, values=options, height=32)
            menu.pack(side="left", fill="x", expand=True)
            entries[key] = var
            return var

        c = car_data or {}
        # Basic fields
        add_dropdown("Brand", "brand_name", list(brand_map.keys()), c.get("brand", ""))
        add_field("Model Name", "model", c.get("model", ""))
        add_field("Variant", "variant", c.get("variant", ""))
        add_field("Model Year", "model_year", c.get("model_year", "2024"))
        add_field("Price (₹)", "price", int(c.get("price", 1000000)) if c.get("price") else "1000000")

        add_dropdown("Fuel Type", "fuel_name", list(fuel_map.keys()), c.get("fuel", ""))
        add_dropdown("Transmission", "trans_name", list(trans_map.keys()), c.get("transmission", ""))
        add_dropdown("Body Type", "body_name", list(body_map.keys()), c.get("body_type", ""))

        # Powertrain & Efficiency
        add_field("Engine / Motor", "engine_capacity", c.get("engine_capacity", "1.5L"))
        add_field("Power", "power_kw", c.get("power_kw", "115 hp"))
        add_field("Torque", "torque", c.get("torque", "144 Nm"))
        add_field("Mileage (km/l for ICE)", "mileage", c.get("mileage", "17.0"))
        add_field("EV Range (km for EV)", "ev_range", c.get("ev_range", "0.0"))
        add_field("Battery Capacity", "battery_capacity", c.get("battery_capacity", ""))

        # Practicality
        add_field("Seating Capacity", "seating_capacity", c.get("seating_capacity", "5"))
        add_field("Boot Space", "boot_capacity", c.get("boot_capacity", "430 L"))
        add_field("Ground Clearance", "ground_clearance", c.get("ground_clearance", "190 mm"))
        add_field("Safety Specifications", "safety_info", c.get("safety_info", "6 Airbags, ABS with EBD"))
        add_field("Description", "description", c.get("description", "Modern reliable family vehicle."))

        # Feature Checkboxes
        ctk.CTkLabel(scroll, text="Select Features Included:", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(12, 4))
        all_features = CarService.get_all_features()
        active_feat_names = set(c.get("features", []))

        feat_checkboxes = {}
        feat_grid = ctk.CTkFrame(scroll, fg_color="transparent")
        feat_grid.pack(fill="x", pady=4)
        feat_grid.grid_columnconfigure((0, 1), weight=1)

        for idx, f in enumerate(all_features):
            is_checked = f["name"] in active_feat_names
            cb_var = ctk.BooleanVar(value=is_checked)
            cb = ctk.CTkCheckBox(feat_grid, text=f["name"], variable=cb_var)
            cb.grid(row=idx // 2, column=idx % 2, padx=6, pady=4, sticky="w")
            feat_checkboxes[f["id"]] = cb_var

        # Submit button handler
        def on_submit():
            # Validate numeric fields
            try:
                yr = int(entries["model_year"].get().strip())
                if not validate_year(yr):
                    messagebox.showerror("Validation Error", "Please enter a valid year between 1990 and 2035.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Model year must be an integer.")
                return

            try:
                pr = float(entries["price"].get().strip())
                if pr <= 0:
                    messagebox.showerror("Validation Error", "Price must be a positive number.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid price entered.")
                return

            try:
                seats = int(entries["seating_capacity"].get().strip())
                if not validate_seating(seats):
                    messagebox.showerror("Validation Error", "Seating capacity must be at least 1.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid seating capacity.")
                return

            try:
                mil = float(entries["mileage"].get().strip() or 0)
                ev_r = float(entries["ev_range"].get().strip() or 0)
            except ValueError:
                messagebox.showerror("Validation Error", "Mileage and EV range must be numbers.")
                return

            payload = {
                "brand_id": brand_map[entries["brand_name"].get()],
                "model": entries["model"].get().strip(),
                "variant": entries["variant"].get().strip(),
                "model_year": yr,
                "price": pr,
                "fuel_id": fuel_map[entries["fuel_name"].get()],
                "transmission_id": trans_map[entries["trans_name"].get()],
                "body_id": body_map[entries["body_name"].get()],
                "engine_capacity": entries["engine_capacity"].get().strip(),
                "power_kw": entries["power_kw"].get().strip(),
                "torque": entries["torque"].get().strip(),
                "mileage": mil,
                "ev_range": ev_r,
                "battery_capacity": entries["battery_capacity"].get().strip(),
                "seating_capacity": seats,
                "boot_capacity": entries["boot_capacity"].get().strip(),
                "ground_clearance": entries["ground_clearance"].get().strip(),
                "safety_info": entries["safety_info"].get().strip(),
                "description": entries["description"].get().strip(),
                "availability": "Available",
            }

            selected_feat_ids = [fid for fid, var in feat_checkboxes.items() if var.get()]

            if mode == "add":
                res = AdminService.add_car(payload, selected_feat_ids)
            else:
                res = AdminService.update_car(car_data["id"], payload, selected_feat_ids)

            if res["success"]:
                messagebox.showinfo("Success", res["message"])
                win.destroy()
                self.render_cars_tab()
            else:
                messagebox.showerror("Error", res["message"])

        # Submit Bar
        submit_btn = ctk.CTkButton(
            scroll,
            text="Save Car to Database" if mode == "add" else "Update Car Specifications",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            text_color="#e0e0e0",
            command=on_submit,
        )
        submit_btn.pack(fill="x", pady=18)
