"""
Comparison Service for Car Saga.
Handles user comparison lists, enforcing the strict 4-car maximum.
"""

from database.connection import get_connection


class ComparisonService:
    @staticmethod
    def add_for_comparison(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Enforce 4-car limit
            cursor.execute("SELECT COUNT(*) FROM comparison_items WHERE user_id = %s", (user_id,))
            count = cursor.fetchone()[0]
            if count >= 4:
                return {
                    "success": False,
                    "message": "You can compare a maximum of 4 cars. Please remove one first.",
                }

            # Check duplicate
            cursor.execute(
                "SELECT id FROM comparison_items WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            if cursor.fetchone():
                return {"success": False, "message": "This car is already in your comparison list."}

            cursor.execute(
                "INSERT INTO comparison_items (user_id, car_id) VALUES (%s, %s)",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Added to comparison list!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not add car to comparison: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_from_comparison(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM comparison_items WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Removed from comparison."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not remove from comparison: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_comparison(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.model_year, c.price, c.mileage, c.ev_range,
                       c.battery_capacity, c.seating_capacity, c.boot_capacity, c.ground_clearance,
                       c.engine_capacity, c.power_kw, c.torque, c.safety_info,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type
                FROM comparison_items ci
                JOIN cars c ON c.id = ci.car_id
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE ci.user_id = %s
                ORDER BY ci.created_at ASC
                """,
                (user_id,),
            )
            cars = cursor.fetchall()

            # Attach features list to each car
            for car in cars:
                cursor.execute(
                    """
                    SELECT fe.name
                    FROM car_features cf
                    JOIN features fe ON fe.id = cf.feature_id
                    WHERE cf.car_id = %s
                    ORDER BY fe.name
                    """,
                    (car["id"],),
                )
                car["features"] = [row["name"] for row in cursor.fetchall()]

            return cars
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def clear_comparison(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM comparison_items WHERE user_id = %s", (user_id,))
            conn.commit()
            return {"success": True, "message": "Comparison list cleared."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not clear comparison: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_comparison_count(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM comparison_items WHERE user_id = %s", (user_id,))
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()
