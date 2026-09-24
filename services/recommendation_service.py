"""
Recommendation Service for Car Saga ("Find My Car").
Uses a transparent, rule-based scoring algorithm suitable for Class 12 CBSE Computer Science.
Ranks cars based on budget, fuel, transmission, body type, and seating capacity,
providing explainable match justifications for each recommendation.
"""

from database.connection import get_connection


class RecommendationService:
    @staticmethod
    def find_my_car(user_requirements):
        """
        Calculates rule-based scores for active cars and returns ranked matches
        with transparent explanation checklists.
        """
        # Parse user inputs safely
        try:
            budget = float(user_requirements.get("budget", 0) or 0)
        except (ValueError, TypeError):
            budget = 0.0

        preferred_fuel = (user_requirements.get("fuel") or "").strip()
        preferred_trans = (user_requirements.get("transmission") or "").strip()
        preferred_body = (user_requirements.get("body_type") or "").strip()

        try:
            min_seats = int(user_requirements.get("seating", 0) or 0)
        except (ValueError, TypeError):
            min_seats = 0

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.id, c.model, c.variant, c.model_year, c.price, c.mileage, c.ev_range,
                       c.seating_capacity, c.boot_capacity, c.ground_clearance,
                       b.name AS brand, f.name AS fuel, t.name AS transmission, bt.name AS body_type
                FROM cars c
                JOIN brands b ON b.id = c.brand_id
                JOIN fuel_types f ON f.id = c.fuel_id
                JOIN transmission_types t ON t.id = c.transmission_id
                JOIN body_types bt ON bt.id = c.body_id
                WHERE c.is_active = 1
                """
            )
            all_cars = cursor.fetchall()

            scored_results = []
            max_possible_score = 0
            if budget > 0:
                max_possible_score += 30
            if preferred_fuel and preferred_fuel != "Any":
                max_possible_score += 20
            if preferred_trans and preferred_trans != "Any":
                max_possible_score += 20
            if preferred_body and preferred_body != "Any":
                max_possible_score += 15
            if min_seats > 0:
                max_possible_score += 15

            if max_possible_score == 0:
                max_possible_score = 100

            for car in all_cars:
                score = 0
                reasons = []

                # 1. Budget Evaluation (30 pts)
                if budget > 0:
                    if float(car["price"]) <= budget:
                        score += 30
                        reasons.append(f"✓ Fits within budget of ₹{int(budget):,}")
                    elif float(car["price"]) <= budget * 1.10:
                        # Close to budget (within 10%)
                        score += 15
                        reasons.append("✓ Close to budget range (within 10%)")
                else:
                    score += 20  # neutral points if user did not specify budget

                # 2. Fuel Type Evaluation (20 pts)
                if preferred_fuel and preferred_fuel != "Any":
                    if car["fuel"].lower() == preferred_fuel.lower():
                        score += 20
                        reasons.append(f"✓ Matches preferred {preferred_fuel} fuel")
                else:
                    score += 15

                # 3. Transmission Evaluation (20 pts)
                if preferred_trans and preferred_trans != "Any":
                    if car["transmission"].lower() == preferred_trans.lower():
                        score += 20
                        reasons.append(f"✓ Matches {preferred_trans} transmission")
                else:
                    score += 15

                # 4. Body Type Evaluation (15 pts)
                if preferred_body and preferred_body != "Any":
                    if car["body_type"].lower() == preferred_body.lower():
                        score += 15
                        reasons.append(f"✓ {preferred_body} body design")
                else:
                    score += 10

                # 5. Seating Capacity Evaluation (15 pts)
                if min_seats > 0:
                    if int(car["seating_capacity"] or 0) >= min_seats:
                        score += 15
                        reasons.append(f"✓ Seats {car['seating_capacity']} passengers (Min required: {min_seats})")
                else:
                    score += 10

                # Efficiency bonus (5 pts)
                if car["fuel"].lower() == "electric" and float(car["ev_range"] or 0) >= 400:
                    reasons.append(f"✓ Long EV range ({int(car['ev_range'])} km)")
                elif float(car["mileage"] or 0) >= 20.0:
                    reasons.append(f"✓ Outstanding fuel efficiency ({car['mileage']} km/l)")

                # Calculate match percentage
                match_percentage = min(100, int((score / max_possible_score) * 100))

                scored_results.append({
                    "car": car,
                    "score": score,
                    "match_percentage": match_percentage,
                    "reasons": reasons,
                })

            # Sort descending by score
            scored_results.sort(key=lambda item: item["score"], reverse=True)
            return scored_results
        finally:
            cursor.close()
            conn.close()
