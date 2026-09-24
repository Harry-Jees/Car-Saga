# Car Saga — Desktop Automotive Discovery Platform
**Class 12 CBSE Computer Science Project**

Car Saga is a desktop application built with **Python 3.12**, **CustomTkinter**, and **MySQL**. It provides a car browsing, comparison, recommendation, and inventory management experience designed according to the CBSE Class 12 Computer Science syllabus.

---

## Key Features

1. **Role-Based Authentication & Security**:
   - Customer and Administrator accounts.
   - Password encryption using industry-standard `bcrypt`.
   - Comprehensive input validation and parameterized SQL (`%s`) preventing SQL injection.

2. **Vehicle Catalogue**:
   - Fast, offline-safe card rendering (no GUI network freezes).
   - Multi-criteria keyword search across Brand, Model, Variant, Body Type, and Fuel.
   - Filter by Brand, Fuel Type, Transmission, Body Type, Max Price, and Seating Capacity.
   - Whitelisted SQL sorting: Price Low-to-High, Price High-to-Low, Model A-Z, Model Z-A, Newest, Best Mileage, and Highest EV Range.
   - Dynamic pagination with accurate filtered car count.

3. **EV Specification Handling**:
   - Proper distinction between Electric Vehicles and Internal Combustion Engine (ICE) vehicles.
   - EVs display **Electric Range (km)** and **Battery Capacity (kWh)**.
   - ICE and Hybrid vehicles display **Fuel Mileage (km/l)**.

4. **Detailed Specifications Page**:
   - Performance, Efficiency, Practicality, and Safety cards.
   - Feature equipment tags.
   - One-click actions to Favourite, Compare, or Shortlist.
   - Automatically records into Recently Viewed history.

5. **Side-by-Side Comparison Matrix**:
   - Compare up to **4 cars** in a structured matrix.
   - Strict 4-car limit enforcement with clear user messaging.
   - Side-by-side spec alignment handling EV and ICE powertrains.

6. **Find My Car (Rule-Based Recommendations)**:
   - Transparent rule-based scoring matching budget, fuel, transmission, body type, and seating.
   - Explainable match checklists (e.g. `✓ Fits within budget`, `✓ Automatic transmission`, `✓ Long EV range`).
   - Match percentage badges.

7. **User Personalization**:
   - **Favourites**: Bookmark preferred vehicles.
   - **Recently Viewed**: Chronological inspection trail with timestamp and clear history option.
   - **Shortlisting ('Selected Cars')**: Persistent shortlisted cars kept separate from favourites.
   - **Saved Searches**: Save filter combinations and reload them in one click.

8. **Administrator Console**:
   - Live database analytics (Total Cars, Active Cars, Users, Brands, Favourites, Saved Searches).
   - Full Car CRUD: Add new car with feature checkboxes, edit specifications, toggle active/inactive status, delete vehicle.
   - User account roster.
   - Master catalogue data manager (Add Brand, Body Type, Fuel Type, Transmission Type, Feature).

---

## Database Architecture (14 Tables)

1. `roles`
2. `users`
3. `brands`
4. `body_types`
5. `fuel_types`
6. `transmission_types`
7. `cars`
8. `features`
9. `car_features`
10. `favourites`
11. `recently_viewed`
12. `saved_searches`
13. `selected_cars`
14. `comparison_items`

---

## Prerequisites & Installation

### 1. Requirements
- Python 3.10+
- Local MySQL Server (XAMPP / WAMP / MySQL 8.0+) running on port 3306

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Car Saga
```bash
python main.py
```
*The application automatically creates the `CarSaga` database and all 14 tables with seed data upon first startup.*

---

## Demo Login Credentials

- **Admin Account**:
  - Username: `admin`
  - Password: `admin123`
- **Customer Demo Account**:
  - Username: `demo`
  - Password: `demo123`

---

## Verification & Automated Tests
To run the automated 21-point test suite:
```bash
python test_verification.py
```
All 21 tests verify database integrity, bcrypt authentication, catalogue filters, pagination, comparison limits, recommendations, and admin CRUD.
