# Car Saga — Build & Architecture Verification Notes
**CBSE Class 12 Computer Science Project**

## 1. Environment & Execution
- **Python**: 3.12+
- **GUI Framework**: CustomTkinter
- **Database**: MySQL Server on `localhost:3306`
  - Host: `localhost`
  - Port: `3306`
  - User: `root`
  - Password: `student`
  - Database: `CarSaga`

## 2. Launching the Application
```powershell
cd c:\Users\project\Desktop\Car2
python main.py
```

## 3. Demo Credentials
- **Admin**: Username: `admin` | Password: `admin123` (Access to Admin Console & CRUD)
- **User**: Username: `demo` | Password: `demo123` (Full customer discovery experience)

## 4. Database Architecture (14 Tables)
The system uses the 14-table architecture specified in `rebuild.md`:
1. `roles`: Role definitions (`ADMIN`, `USER`)
2. `users`: Registered users with bcrypt passwords
3. `brands`: Automotive brand names (Tata, Hyundai, Maruti Suzuki, Mahindra, Toyota, etc.)
4. `body_types`: SUV, Sedan, Hatchback, MPV
5. `fuel_types`: Petrol, Diesel, Electric, Hybrid
6. `transmission_types`: Manual, Automatic
7. `cars`: Vehicle specifications, pricing, EV range, battery capacity, mileage
8. `features`: Equipment and safety feature catalog
9. `car_features`: Many-to-many relationship mapping cars to features
10. `favourites`: User-specific favourite vehicles
11. `recently_viewed`: Chronological vehicle inspection history
12. `saved_searches`: User search & filter preset configurations
13. `selected_cars`: User shortlisted cars (separate from favourites)
14. `comparison_items`: Side-by-side comparison list (strictly enforcing max 4 cars)

## 5. Verification Status
- Full compilation: `python -m compileall .` passed with 0 errors.
- Automated Test Suite: `python test_verification.py` passed all 21 tests (100%).
- EV data verified: Tata Nexon EV & MG ZS EV properly display Electric Range (km) & Battery (kWh), without mislabeling as fuel mileage (km/l).
