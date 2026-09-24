"""
Recently Viewed Service for Car Saga.
Tracks cars inspected by each user and maintains a chronological history.
"""

from database.connection import get_connection


class RecentlyViewedService:
    @staticmethod
    def add_recent_view(user_id, car_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO recently_viewed (user_id, car_id, viewed_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE viewed_at = CURRENT_TIMESTAMP
                """,
                (user_id, car_id),
            )
            conn.commit()
            return {"success": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_recently_viewed(user_id, limit=10):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.price, c.mileage, c.ev_range, c.model_year,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type,
                       rv.viewed_at
                FROM recently_viewed rv
                JOIN cars c ON c.id = rv.car_id
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE rv.user_id = %s AND c.is_active = 1
                ORDER BY rv.viewed_at DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def clear_recently_viewed(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM recently_viewed WHERE user_id = %s", (user_id,))
            conn.commit()
            return {"success": True}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()
