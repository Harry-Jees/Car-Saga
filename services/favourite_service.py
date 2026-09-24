"""
Favourite Service for Car Saga.
Handles user-specific favourite cars.
"""

from database.connection import get_connection


class FavouriteService:
    @staticmethod
    def add_favourite(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id FROM favourites WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            if cursor.fetchone():
                return {"success": False, "message": "Car is already in your favourites."}

            cursor.execute(
                "INSERT INTO favourites (user_id, car_id) VALUES (%s, %s)",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Added to favourites!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not add favourite: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def remove_favourite(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM favourites WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True, "message": "Removed from favourites."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not remove favourite: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def is_favourite(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM favourites WHERE user_id = %s AND car_id = %s",
                (user_id, car_id),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_favourites(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.price, c.mileage, c.ev_range, c.model_year,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type,
                       fav.created_at AS added_on
                FROM favourites fav
                JOIN cars c ON c.id = fav.car_id
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE fav.user_id = %s AND c.is_active = 1
                ORDER BY fav.created_at DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
