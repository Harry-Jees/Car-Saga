"""
Car Service for Car Saga.
Handles car catalogue browsing, search, multi-criteria filtering,
whitelisted sorting, pagination, and car details retrieval.
"""

from database.connection import get_connection


class CarService:
    @staticmethod
    def get_catalogue(filters=None, sort_by="price_asc", page=1, page_size=6):
        filters = filters or {}
        page = max(1, int(page or 1))
        page_size = max(1, int(page_size or 6))
        offset = (page - 1) * page_size

        base_from = """
            FROM cars c
            JOIN brands b ON b.id = c.brand_id
            JOIN fuel_types f ON f.id = c.fuel_id
            JOIN transmission_types t ON t.id = c.transmission_id
            JOIN body_types bt ON bt.id = c.body_id
            WHERE c.is_active = 1
        """
        where_clauses = []
        params = []

        if filters.get("search"):
            term = f"%{filters['search'].strip()}%"
            where_clauses.append(
                "(b.name LIKE %s OR c.model LIKE %s OR c.variant LIKE %s OR bt.name LIKE %s OR f.name LIKE %s)"
            )
            params.extend([term, term, term, term, term])

        if filters.get("brand") and filters["brand"] != "All Brands":
            where_clauses.append("b.name = %s")
            params.append(filters["brand"])

        if filters.get("fuel") and filters["fuel"] != "All Fuels":
            where_clauses.append("f.name = %s")
            params.append(filters["fuel"])

        if filters.get("transmission") and filters["transmission"] != "All Transmissions":
            where_clauses.append("t.name = %s")
            params.append(filters["transmission"])

        if filters.get("body_type") and filters["body_type"] != "All Body Types":
            where_clauses.append("bt.name = %s")
            params.append(filters["body_type"])

        if filters.get("min_price"):
            try:
                where_clauses.append("c.price >= %s")
                params.append(float(filters["min_price"]))
            except (ValueError, TypeError):
                pass

        if filters.get("max_price"):
            try:
                where_clauses.append("c.price <= %s")
                params.append(float(filters["max_price"]))
            except (ValueError, TypeError):
                pass

        if filters.get("min_seating"):
            try:
                where_clauses.append("c.seating_capacity >= %s")
                params.append(int(filters["min_seating"]))
            except (ValueError, TypeError):
                pass

        if filters.get("model_year"):
            try:
                where_clauses.append("c.model_year >= %s")
                params.append(int(filters["model_year"]))
            except (ValueError, TypeError):
                pass

        if filters.get("min_mileage"):
            try:
                where_clauses.append("c.mileage >= %s")
                params.append(float(filters["min_mileage"]))
            except (ValueError, TypeError):
                pass

        if filters.get("min_ev_range"):
            try:
                where_clauses.append("c.ev_range >= %s")
                params.append(float(filters["min_ev_range"]))
            except (ValueError, TypeError):
                pass

        if filters.get("availability") and filters["availability"] != "All":
            where_clauses.append("c.availability = %s")
            params.append(filters["availability"])

        # Construct final WHERE clause
        extra_where = ""
        if where_clauses:
            extra_where = " AND " + " AND ".join(where_clauses)

        # SQL Sorting Whitelist
        sort_whitelist = {
            "price_asc": "c.price ASC",
            "price_desc": "c.price DESC",
            "name_asc": "b.name ASC, c.model ASC",
            "name_desc": "b.name DESC, c.model DESC",
            "year_desc": "c.model_year DESC",
            "mileage_desc": "c.mileage DESC",
            "ev_range_desc": "c.ev_range DESC",
        }
        order_by_sql = sort_whitelist.get(sort_by, "c.price ASC")

        count_query = f"SELECT COUNT(*) AS total {base_from} {extra_where}"
        data_query = f"""
            SELECT c.id, c.model, c.variant, c.model_year, c.price, c.mileage, c.ev_range,
                   c.battery_capacity, c.seating_capacity, c.boot_capacity, c.ground_clearance,
                   b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type,
                   c.image_url, c.description, c.availability
            {base_from} {extra_where}
            ORDER BY {order_by_sql}
            LIMIT %s OFFSET %s
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Execute Count with filter params
            cursor.execute(count_query, tuple(params))
            total_count = cursor.fetchone()["total"]

            # Execute Data with pagination params
            data_params = list(params) + [page_size, offset]
            cursor.execute(data_query, tuple(data_params))
            cars = cursor.fetchall()

            return {
                "cars": cars,
                "total": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, (total_count + page_size - 1) // page_size),
            }
        except Exception as e:
            print("CarService get_catalogue error:", e)
            return {"cars": [], "total": 0, "page": page, "page_size": page_size, "total_pages": 1}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_car_by_id(car_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.*, b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type
                FROM cars c
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE c.id = %s
                """,
                (car_id,),
            )
            car = cursor.fetchone()
            if not car:
                return None

            # Fetch feature names
            cursor.execute(
                """
                SELECT fe.name
                FROM car_features cf
                JOIN features fe ON fe.id = cf.feature_id
                WHERE cf.car_id = %s
                ORDER BY fe.name
                """,
                (car_id,),
            )
            car["features"] = [row["name"] for row in cursor.fetchall()]
            return car
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_brands():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM brands ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_fuel_types():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM fuel_types ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_transmissions():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM transmission_types ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_body_types():
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM body_types ORDER BY name")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_features():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, name FROM features ORDER BY name")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
