"""
Shortlist Service for Car Saga ("Selected Cars").
Maintains persistent, user-specific shortlisted cars independently from Favourites and Compare.
"""

from database.connection import get_connection


class ShortlistService:
    @staticmethod
    def add_to_shortlist(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM selected_cars WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            if cursor.fetchone():
                return {"success": False, "message": "Car is already shortlisted."}

            cursor.execute(
                "INSERT INTO selected_cars (user_id, car_id) VALUES (%s, %s)",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Added to your shortlist!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not shortlist car: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_from_shortlist(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM selected_cars WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Removed from shortlist."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not remove from shortlist: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def is_shortlisted(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM selected_cars WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_shortlist(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.price, c.mileage, c.ev_range, c.model_year,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type,
                       sc.created_at AS shortlisted_on
                FROM selected_cars sc
                JOIN cars c ON c.id = sc.car_id
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE sc.user_id = %s AND c.is_active = 1
                ORDER BY sc.created_at DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
