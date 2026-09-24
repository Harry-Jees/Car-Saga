"""
Admin Service for Car Saga.
Handles administration metrics, car CRUD, user viewing, and catalogue data management.
"""

from database.connection import get_connection


class AdminService:
    @staticmethod
    def get_dashboard_stats():
        """Fetches live administrative statistics directly from MySQL."""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS count FROM cars")
            total_cars = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM cars WHERE is_active = 1")
            active_cars = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM users WHERE role_id = 2")
            total_users = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM brands")
            total_brands = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM favourites")
            total_favourites = cursor.fetchone()["count"]

            cursor.execute("SELECT COUNT(*) AS count FROM saved_searches")
            total_searches = cursor.fetchone()["count"]

            # Fuel breakdown
            cursor.execute(
                """
                SELECT f.name, COUNT(c.id) AS count
                FROM fuel_types f
                LEFT JOIN cars c ON c.fuel_id = f.id AND c.is_active = 1
                GROUP BY f.id, f.name
                """
            )
            fuel_stats = cursor.fetchall()

            # Body type breakdown
            cursor.execute(
                """
                SELECT bt.name, COUNT(c.id) AS count
                FROM body_types bt
                LEFT JOIN cars c ON c.body_id = bt.id AND c.is_active = 1
                GROUP BY bt.id, bt.name
                """
            )
            body_stats = cursor.fetchall()

            return {
                "total_cars": total_cars,
                "active_cars": active_cars,
                "total_users": total_users,
                "total_brands": total_brands,
                "total_favourites": total_favourites,
                "total_searches": total_searches,
                "fuel_stats": fuel_stats,
                "body_stats": body_stats,
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_cars():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.model_year, c.price, c.mileage, c.ev_range,
                       c.seating_capacity, c.is_active, c.availability,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type
                FROM cars c
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                ORDER BY c.id DESC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_car(car_data, feature_ids=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO cars (
                    brand_id, model, variant, model_year, price, fuel_id, transmission_id, body_id,
                    engine_capacity, power_kw, torque, mileage, ev_range, battery_capacity,
                    seating_capacity, boot_capacity, ground_clearance, safety_info, description,
                    image_url, availability, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                """,
                (
                    car_data["brand_id"], car_data["model"], car_data.get("variant", ""),
                    car_data["model_year"], car_data["price"], car_data["fuel_id"],
                    car_data["transmission_id"], car_data["body_id"],
                    car_data.get("engine_capacity", ""), car_data.get("power_kw", ""),
                    car_data.get("torque", ""), car_data.get("mileage", 0.0),
                    car_data.get("ev_range", 0.0), car_data.get("battery_capacity", ""),
                    car_data.get("seating_capacity", 5), car_data.get("boot_capacity", ""),
                    car_data.get("ground_clearance", ""), car_data.get("safety_info", ""),
                    car_data.get("description", ""), car_data.get("image_url", ""),
                    car_data.get("availability", "Available")
                ),
            )
            new_car_id = cursor.lastrowid

            if feature_ids:
                for fid in feature_ids:
                    cursor.execute(
                        "INSERT IGNORE INTO car_features (car_id, feature_id) VALUES (%s, %s)",
                        (new_car_id, fid),
                    )

            conn.commit()
            return {"success": True, "message": "Car added successfully!", "car_id": new_car_id}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not add car: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_car(car_id, car_data, feature_ids=None):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE cars SET
                    brand_id = %s, model = %s, variant = %s, model_year = %s, price = %s,
                    fuel_id = %s, transmission_id = %s, body_id = %s, engine_capacity = %s,
                    power_kw = %s, torque = %s, mileage = %s, ev_range = %s,
                    battery_capacity = %s, seating_capacity = %s, boot_capacity = %s,
                    ground_clearance = %s, safety_info = %s, description = %s,
                    availability = %s
                WHERE id = %s
                """,
                (
                    car_data["brand_id"], car_data["model"], car_data.get("variant", ""),
                    car_data["model_year"], car_data["price"], car_data["fuel_id"],
                    car_data["transmission_id"], car_data["body_id"],
                    car_data.get("engine_capacity", ""), car_data.get("power_kw", ""),
                    car_data.get("torque", ""), car_data.get("mileage", 0.0),
                    car_data.get("ev_range", 0.0), car_data.get("battery_capacity", ""),
                    car_data.get("seating_capacity", 5), car_data.get("boot_capacity", ""),
                    car_data.get("ground_clearance", ""), car_data.get("safety_info", ""),
                    car_data.get("description", ""), car_data.get("availability", "Available"),
                    car_id
                ),
            )

            if feature_ids is not None:
                cursor.execute("DELETE FROM car_features WHERE car_id = %s", (car_id,))
                for fid in feature_ids:
                    cursor.execute(
                        "INSERT IGNORE INTO car_features (car_id, feature_id) VALUES (%s, %s)",
                        (car_id, fid),
                    )

            conn.commit()
            return {"success": True, "message": "Car updated successfully!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not update car: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def toggle_car_status(car_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT is_active FROM cars WHERE id = %s", (car_id,))
            car = cursor.fetchone()
            if not car:
                return {"success": False, "message": "Car not found."}

            new_status = 0 if car["is_active"] == 1 else 1
            cursor.execute("UPDATE cars SET is_active = %s WHERE id = %s", (new_status, car_id))
            conn.commit()
            status_text = "Activated" if new_status == 1 else "Deactivated"
            return {"success": True, "message": f"Car {status_text} successfully!", "is_active": new_status}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_car(car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Delete dependent relations first for safe referential integrity
            cursor.execute("DELETE FROM car_features WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM favourites WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM recently_viewed WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM selected_cars WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM comparison_items WHERE car_id = %s", (car_id,))
            cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
            conn.commit()
            return {"success": True, "message": "Car deleted successfully."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not delete car: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_users():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT u.id, u.full_name, u.username, u.email, u.is_active, u.created_at, r.name AS role_name
                FROM users u
                JOIN roles r ON r.id = u.role_id
                ORDER BY u.id ASC
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_catalogue_item(table_name, name_val):
        whitelist = {
            "brands": "brands",
            "body_types": "body_types",
            "fuel_types": "fuel_types",
            "transmission_types": "transmission_types",
            "features": "features",
        }
        tbl = whitelist.get(table_name)
        if not tbl or not name_val or not name_val.strip():
            return {"success": False, "message": "Invalid table or item name."}

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO {tbl} (name) VALUES (%s)", (name_val.strip(),))
            conn.commit()
            return {"success": True, "message": f"Added '{name_val}' successfully!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not add: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_metadata_ids():
        """Returns lookup maps for brands, fuels, transmissions, and body types."""
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, name FROM brands ORDER BY name")
            brands = cursor.fetchall()
            cursor.execute("SELECT id, name FROM fuel_types ORDER BY name")
            fuels = cursor.fetchall()
            cursor.execute("SELECT id, name FROM transmission_types ORDER BY name")
            trans = cursor.fetchall()
            cursor.execute("SELECT id, name FROM body_types ORDER BY name")
            bodies = cursor.fetchall()
            return {
                "brands": brands,
                "fuels": fuels,
                "transmissions": trans,
                "bodies": bodies,
            }
        finally:
            cursor.close()
            conn.close()
