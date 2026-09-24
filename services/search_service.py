"""
Saved Search Service for Car Saga.
Allows users to name and persist search & filter combinations.
"""

from database.connection import get_connection


class SearchService:
    @staticmethod
    def save_search(user_id, name, criteria):
        if not name or not name.strip():
            return {"success": False, "message": "Please give your search a name."}

        name = name.strip()
        search_text = criteria.get("search", "") or ""
        brand = criteria.get("brand", "") or ""
        fuel = criteria.get("fuel", "") or ""
        transmission = criteria.get("transmission", "") or ""
        body_type = criteria.get("body_type", "") or ""

        try:
            min_price = float(criteria.get("min_price", 0) or 0)
        except (ValueError, TypeError):
            min_price = 0.0

        try:
            max_price = float(criteria.get("max_price", 0) or 0)
        except (ValueError, TypeError):
            max_price = 0.0

        try:
            min_seating = int(criteria.get("min_seating", 0) or 0)
        except (ValueError, TypeError):
            min_seating = 0

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO saved_searches (
                    user_id, name, search_text, brand, fuel, transmission,
                    body_type, min_price, max_price, min_seating
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id, name, search_text, brand, fuel, transmission,
                    body_type, min_price, max_price, min_seating
                ),
            )
            conn.commit()
            return {"success": True, "message": f"Search '{name}' saved successfully!"}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not save search: {e}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_saved_searches(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT id, name, search_text, brand, fuel, transmission,
                       body_type, min_price, max_price, min_seating, created_at
                FROM saved_searches
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_saved_search(user_id, search_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM saved_searches WHERE id = %s AND user_id = %s",
                (search_id, user_id),
            )
            conn.commit()
            return {"success": True, "message": "Saved search deleted."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Could not delete search: {e}"}
        finally:
            cursor.close()
            conn.close()
