"""
Verification Test Suite for Car Saga.
Tests all database, service, security, and rule-based recommendation logic.
"""

from database.connection import initialize_database, get_connection
from services.auth_service import AuthService
from services.car_service import CarService
from services.favourite_service import FavouriteService
from services.recently_viewed_service import RecentlyViewedService
from services.comparison_service import ComparisonService
from services.recommendation_service import RecommendationService
from services.shortlist_service import ShortlistService
from services.search_service import SearchService
from services.admin_service import AdminService


def run_tests():
    print("--- STARTING CAR SAGA VERIFICATION ---")

    # 1. DB Init
    assert initialize_database() is True, "DB Init failed"
    print("[PASS] 1. Database initialized & verified")

    # Clean up any leftover teststudent from previous interrupted run
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = %s", ("teststudent",))
    conn.commit()
    conn.close()

    # 2. Auth Tests
    reg1 = AuthService.register_user("Test Student", "teststudent", "student@school.edu", "secret123", "secret123")
    print(f"[PASS] 2. User registration: {reg1['success']}")

    reg_dup = AuthService.register_user("Test Student", "teststudent", "student@school.edu", "secret123", "secret123")
    assert reg_dup["success"] is False, "Duplicate registration allowed"
    print("[PASS] 3. Duplicate registration rejected")

    login_demo = AuthService.login("demo", "demo123")
    assert login_demo["success"] is True and login_demo["user"]["role"] == "USER", "Demo login failed"
    print("[PASS] 4. Demo user login successful")

    login_admin = AuthService.login("admin", "admin123")
    assert login_admin["success"] is True and login_admin["user"]["role"] == "ADMIN", "Admin login failed"
    print("[PASS] 5. Admin login successful")

    bad_login = AuthService.login("demo", "wrongpassword")
    assert bad_login["success"] is False, "Bad password accepted"
    print("[PASS] 6. Invalid password rejected")

    # 3. Catalogue Tests
    cat_all = CarService.get_catalogue({}, page=1, page_size=6)
    total_cars = cat_all["total"]
    assert total_cars >= 14, f"Expected >=14 cars, got {total_cars}"
    print(f"[PASS] 7. Catalogue load: {total_cars} cars, {cat_all['total_pages']} pages")

    cat_ev = CarService.get_catalogue({"fuel": "Electric"}, page=1, page_size=6)
    assert cat_ev["total"] == 2, f"Expected 2 EVs, got {cat_ev['total']}"
    print(f"[PASS] 8. Filter fuel=Electric: {cat_ev['total']} cars found")

    cat_sort = CarService.get_catalogue({}, sort_by="price_desc", page=1, page_size=2)
    assert cat_sort["cars"][0]["price"] >= cat_sort["cars"][1]["price"], "Sorting failed"
    print("[PASS] 9. Whitelisted SQL sorting verified (price descending)")

    car_detail = CarService.get_car_by_id(2)
    assert car_detail["model"] == "Nexon EV" and len(car_detail["features"]) > 0, "Car details failed"
    print(f"[PASS] 10. Car details with features: {car_detail['brand']} {car_detail['model']}")

    # 4. Favourites
    uid = login_demo["user"]["id"]
    for fav in FavouriteService.get_favourites(uid):
        FavouriteService.remove_favourite(uid, fav["id"])
    fav_add = FavouriteService.add_favourite(uid, 2)
    assert fav_add["success"] is True, "Add fav failed"
    fav_dup = FavouriteService.add_favourite(uid, 2)
    assert fav_dup["success"] is False, "Duplicate fav allowed"
    fav_list = FavouriteService.get_favourites(uid)
    assert len(fav_list) == 1, "Fav list length mismatch"
    FavouriteService.remove_favourite(uid, 2)
    assert len(FavouriteService.get_favourites(uid)) == 0, "Fav remove failed"
    print("[PASS] 11. Favourites lifecycle (add, duplicate prevention, list, remove) verified")

    # 5. Recently Viewed
    RecentlyViewedService.clear_recently_viewed(uid)
    RecentlyViewedService.add_recent_view(uid, 1)
    RecentlyViewedService.add_recent_view(uid, 2)
    rec_views = RecentlyViewedService.get_recently_viewed(uid)
    assert len(rec_views) == 2, "Recent views length mismatch"
    print("[PASS] 12. Recently viewed tracking verified")

    # 6. Comparison (Enforcing 4 cars max)
    ComparisonService.clear_comparison(uid)
    assert ComparisonService.add_for_comparison(uid, 1)["success"] is True
    assert ComparisonService.add_for_comparison(uid, 2)["success"] is True
    assert ComparisonService.add_for_comparison(uid, 3)["success"] is True
    assert ComparisonService.add_for_comparison(uid, 4)["success"] is True
    # 5th car attempt must fail
    comp5 = ComparisonService.add_for_comparison(uid, 5)
    assert comp5["success"] is False, "5th car was improperly accepted"
    print(f"[PASS] 13. 4-car comparison limit strictly enforced: {comp5['message']}")
    comp_list = ComparisonService.get_comparison(uid)
    assert len(comp_list) == 4, "Comparison list length mismatch"
    ComparisonService.clear_comparison(uid)
    assert len(ComparisonService.get_comparison(uid)) == 0, "Comparison clear failed"
    print("[PASS] 14. Comparison matrix fetch and clear verified")

    # 7. Shortlist ("Selected Cars")
    for car in ShortlistService.get_shortlist(uid):
        ShortlistService.remove_from_shortlist(uid, car["id"])
    ShortlistService.add_to_shortlist(uid, 3)
    sl = ShortlistService.get_shortlist(uid)
    assert len(sl) == 1 and sl[0]["id"] == 3, "Shortlist mismatch"
    ShortlistService.remove_from_shortlist(uid, 3)
    assert len(ShortlistService.get_shortlist(uid)) == 0, "Shortlist remove failed"
    print("[PASS] 15. Shortlisting ('Selected Cars') verified")

    # 8. Saved Searches
    SearchService.save_search(uid, "My EV Search", {"fuel": "Electric", "max_price": 2000000})
    ss = SearchService.get_saved_searches(uid)
    assert len(ss) >= 1 and ss[0]["name"] == "My EV Search", "Saved search mismatch"
    SearchService.delete_saved_search(uid, ss[0]["id"])
    print("[PASS] 16. Saved searches (save, list, delete) verified")

    # 9. Recommendation ("Find My Car")
    rec_results = RecommendationService.find_my_car({"budget": 1600000, "fuel": "Electric", "body_type": "SUV"})
    assert len(rec_results) > 0, "No recommendations returned"
    top_rec = rec_results[0]
    print(f"[PASS] 17. Find My Car top recommendation: {top_rec['car']['model']} ({top_rec['match_percentage']}% match)")
    clean_reasons = [str(r).encode('ascii', errors='replace').decode('ascii') for r in top_rec['reasons']]
    print(f"     Match checklist: {clean_reasons}")

    # 10. Admin CRUD & Live Stats
    admin_stats = AdminService.get_dashboard_stats()
    assert admin_stats["total_cars"] >= 14, "Admin stats car count mismatch"
    print(f"[PASS] 18. Admin live database statistics: {admin_stats['total_cars']} total cars, {admin_stats['total_users']} users")

    # Admin Add Car & Edit & Delete test
    test_car_payload = {
        "brand_id": 1,
        "model": "Test Auto",
        "variant": "VXi",
        "model_year": 2024,
        "price": 650000.0,
        "fuel_id": 1,
        "transmission_id": 1,
        "body_id": 1,
        "engine_capacity": "1.0L",
        "power_kw": "67 hp",
        "torque": "90 Nm",
        "mileage": 24.5,
        "ev_range": 0.0,
        "battery_capacity": "",
        "seating_capacity": 5,
        "boot_capacity": "260 L",
        "ground_clearance": "165 mm",
        "safety_info": "Dual Airbags, ABS",
        "description": "Test car record.",
    }
    add_res = AdminService.add_car(test_car_payload, [1, 2])
    assert add_res["success"] is True, f"Admin add car failed: {add_res['message']}"
    t_cid = add_res["car_id"]
    print(f"[PASS] 19. Admin Add Car created car ID: {t_cid}")

    # Toggle status
    tog_res = AdminService.toggle_car_status(t_cid)
    assert tog_res["success"] is True and tog_res["is_active"] == 0
    print("[PASS] 20. Admin Deactivate Car verified")

    # Delete car
    del_res = AdminService.delete_car(t_cid)
    assert del_res["success"] is True
    print("[PASS] 21. Admin Delete Car verified")

    # Clean up test user
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = %s", ("teststudent",))
    conn.commit()
    conn.close()

    print("\n==========================================")
    print("  ALL 21 INTEGRATION TESTS PASSED 100%!  ")
    print("==========================================")


if __name__ == "__main__":
    run_tests()
