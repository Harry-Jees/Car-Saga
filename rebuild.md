# CAR SAGA — MASTER BUILD PROMPT

Build **Car Saga**, a polished **Class 12 CBSE Computer Science desktop application** for discovering, filtering, comparing and selecting cars.

## 1. NON-NEGOTIABLE REQUIREMENT

This is a **Class 12 CBSE project**.

The application may look professional and advanced, but the **source code must remain Class 12 level**:

* Simple and readable Python
* Basic functions and classes
* Basic OOP where useful
* Lists, dictionaries, loops, conditions
* Straightforward SQL
* Basic exception handling
* Clear variable/function names
* Comments for important logic

**Do NOT over-engineer the project.**

Avoid unnecessary:

* Design patterns
* Complex abstractions
* Async programming
* Multithreading
* ORMs
* Advanced frameworks
* Complicated algorithms
* AI/ML unless explicitly requested

Every important part of the code should be explainable by a Class 12 student in a CBSE viva.

---

# 2. TECHNOLOGY

Use:

* Python 3.x
* CustomTkinter for GUI
* MySQL
* mysql-connector-python
* bcrypt
* Pillow/PIL

Database:

```text
Host: localhost
Port: 3306
Username: root
Password: student
Database: CarSaga
```

Create the `CarSaga` database automatically if it does not exist.

Never delete or overwrite an existing database automatically.

---

# 3. APPLICATION CONCEPT

Car Saga is a **car discovery and selection desktop application**.

A user should be able to:

* Register/login
* Browse cars
* Search
* Filter
* Sort
* View detailed specifications
* Favourite cars
* View recently viewed cars
* Save searches
* Compare cars
* Find suitable cars using requirements
* Shortlist/select cars

An administrator should be able to:

* Login
* View dashboard statistics
* Manage cars
* Add/edit/deactivate cars
* Manage catalogue information
* View users

Use proper role-based access so normal users cannot access admin functions.

---

# 4. DATABASE

Maintain the existing **14-table Car Saga database architecture** if an existing project is supplied.

The schema should cover entities for:

* Users
* Roles
* Brands
* Cars
* Body types
* Fuel types
* Transmission types
* Car images
* Features
* Car-feature relationships
* Favourites
* Recently viewed
* Saved searches
* Comparison/selection functionality

Use:

* Primary keys
* Foreign keys
* Appropriate constraints
* Useful indexes
* Referential integrity

Do not rename existing tables unnecessarily.

---

# 5. CAR INFORMATION

Cars should support, where applicable:

* Brand
* Model
* Variant
* Year
* Price
* Fuel type
* Transmission
* Body type
* Engine
* Power
* Torque
* Mileage
* EV range
* Battery capacity
* Seating capacity
* Boot capacity
* Ground clearance
* Safety
* Features
* Description
* Image
* Availability/status

---

# 6. EV HANDLING

Treat EVs correctly.

EVs should support:

* Battery capacity
* Electric range
* Motor power
* Charging information where available

Do **not** display EV range as petrol/diesel mileage.

Example:

```text
Electric Range: 450 km
Battery: 60 kWh
```

not:

```text
Mileage: 450 km/l
```

EV range must also work correctly in filtering, comparison and recommendations.

---

# 7. USER FEATURES

## Catalogue

Create a clean car-card based catalogue showing:

* Image
* Brand/model
* Price
* Fuel
* Transmission
* Mileage/range
* Favourite
* Compare
* Details

## Search

Search by relevant fields such as:

* Brand
* Model
* Variant
* Body type
* Fuel

Use parameterized SQL.

## Filters

Support combinations of:

* Brand
* Price range
* Fuel
* Transmission
* Body type
* Seats
* Year
* Mileage
* EV range
* Power
* Availability

## Sorting

Support:

* Price low-high
* Price high-low
* Name A-Z
* Name Z-A
* Newest
* Highest mileage
* Highest EV range

Use a whitelist for SQL sorting.

## Pagination

Use pagination for catalogue results and make it work together with search, filters and sorting.

---

# 8. CAR DETAILS

Create a detailed car page containing:

### Overview

Brand, model, variant, price, year, body type

### Performance

Engine/motor, power, torque, transmission

### Efficiency

Mileage, EV range, battery

### Practicality

Seats, boot, ground clearance

### Features

Comfort, technology, convenience

### Safety

Safety specifications

### Description

Actions:

* Favourite
* Compare
* Shortlist/select
* Back

Opening a car should update Recently Viewed.

---

# 9. FAVOURITES

Users can add/remove cars from favourites.

Favourites must be user-specific.

Prevent duplicate favourite records.

---

# 10. RECENTLY VIEWED

When a user opens a car, record:

* User
* Car
* Date/time

Display the user's recent cars only.

---

# 11. SAVED SEARCHES

Allow users to save their current search/filter configuration.

Store relevant criteria such as:

* Search text
* Brand
* Price
* Fuel
* Transmission
* Body type
* Seats
* Mileage
* EV range

Allow:

* Save
* Load/run
* Delete

Saved searches must be user-specific.

---

# 12. COMPARE

Allow a maximum of **4 cars**.

Users can:

* Add
* Remove
* Clear
* Compare

Attempting to add a fifth car must be prevented with a clear message.

Comparison should show common specifications such as:

* Price
* Fuel
* Transmission
* Power
* Torque
* Mileage
* EV range
* Battery
* Seats
* Boot
* Ground clearance
* Engine

Handle missing/irrelevant values properly.

---

# 13. FIND MY CAR

Create a feature called **Find My Car**.

User enters requirements such as:

* Budget
* Fuel
* Transmission
* Body type
* Seating
* Mileage/range
* Performance preference

Use a **simple rule-based scoring system**, not complicated AI.

Example:

```python
score = 0

if car_price <= budget:
    score += 30

if car_fuel == preferred_fuel:
    score += 20
```

Rank suitable cars based on the requirements.

Each recommendation should explain why it matched, for example:

```text
✓ Within budget
✓ Automatic
✓ SUV
✓ 5 seats
✓ Preferred fuel
```

Call this a **rule-based recommendation system**, not AI.

---

# 14. SHORTLISTING

Allow users to select/shortlist cars.

Shortlisting must be persistent and user-specific.

Keep these separate:

* Favourite
* Recently Viewed
* Compare
* Shortlisted

---

# 15. ADMIN

Create a separate professional Admin Dashboard.

Show useful statistics such as:

* Total cars
* Active cars
* Total users
* Brands
* Favourites
* Saved searches

Optional charts:

* Cars by fuel
* Cars by body type
* Cars by brand

Statistics must come from the database.

## Admin CRUD

Admin can:

* Add cars
* View cars
* Edit cars
* Deactivate/delete cars where safe
* View users
* Manage catalogue data

Use confirmation dialogs for destructive operations.

---

# 16. UI DESIGN

Use a modern automotive interface.

Design direction:

* Dark/neutral professional theme
* Rounded cards
* Clean typography
* Consistent spacing
* Professional car images
* Clear icons
* Modern dashboard
* Minimal clutter

Use CustomTkinter.

The UI should look significantly more polished than a basic school project while keeping the implementation simple.

Make long pages scrollable and support reasonable window resizing.

---

# 17. AUTHENTICATION & SECURITY

Use bcrypt for passwords.

Never store plaintext passwords.

Use parameterized SQL for all user-controlled values.

Example:

```python
cursor.execute(
    "SELECT * FROM cars WHERE brand_id = %s",
    (brand_id,)
)
```

Never construct SQL using raw user input.

For dynamic sorting, use a predefined whitelist.

Validate:

* Required fields
* Email
* Password
* Price
* Year
* Seats
* Mileage
* EV range
* Other numeric fields

Hide technical errors from users.

---

# 18. DATABASE HANDLING

Create a simple centralized database connection utility.

It should handle:

* Connection
* Commit
* Rollback
* Closing cursors/connections
* Connection errors

Use transactions when multiple related records are inserted/updated.

Do not destroy existing data during startup.

---

# 19. SEED DATA

Provide realistic sample data containing:

* Multiple brands
* Multiple body types
* Petrol
* Diesel
* EV
* Hybrid if supported
* Manual
* Automatic
* Different price ranges
* Different seating
* Different mileage
* Different EV ranges

Include enough cars to demonstrate pagination, filtering, comparison and recommendations.

---

# 20. ERROR & EMPTY STATES

Handle gracefully:

* MySQL unavailable
* Invalid login
* Duplicate account
* Invalid input
* No search results
* Missing image
* Database errors
* Unauthorized access

Examples:

```text
No cars match your current filters.
```

```text
You haven't added any favourites yet.
```

```text
You can compare a maximum of 4 cars.
```

Never show raw Python tracebacks, SQL queries or database credentials.

---

# 21. PROJECT STRUCTURE

Use a simple modular structure such as:

```text
Car_Saga/
│
├── main.py
├── requirements.txt
├── README.md
├── build.md
│
├── database/
│   ├── connection.py
│   ├── schema.sql
│   └── seed.sql
│
├── services/
│   ├── auth.py
│   ├── cars.py
│   ├── favourites.py
│   ├── comparison.py
│   ├── recommendations.py
│   └── searches.py
│
├── ui/
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── catalogue.py
│   ├── car_details.py
│   ├── compare.py
│   ├── favourites.py
│   ├── find_my_car.py
│   └── admin/
│
├── utils/
│   ├── validators.py
│   └── helpers.py
│
└── assets/
    ├── images/
    └── icons/
```

Adapt this if the supplied repository already has a working structure.

---

# 22. IF AN EXISTING CAR SAGA PROJECT IS PROVIDED

Do not rebuild blindly.

First inspect:

1. Project structure
2. Existing Python code
3. Database schema
4. Seed data
5. SQL queries
6. UI modules
7. Authentication
8. Existing features

Preserve working functionality.

Fix inconsistencies instead of unnecessarily rewriting everything.

---

# 23. REQUIRED CROSSCHECK

Before declaring the project finished, verify every feature through:

```text
UI
↓
Python Function
↓
SQL Query
↓
Database Table
↓
Database Column
↓
Foreign Key
```

Check for:

* Nonexistent tables
* Nonexistent columns
* Incorrect joins
* Wrong foreign keys
* Wrong data types
* Broken UI callbacks
* Missing functions
* Incorrect SQL
* Missing validation
* Authorization problems

Also verify that every database field used by the UI actually exists.

---

# 24. TESTING

Test at minimum:

### Authentication

* Registration
* Duplicate registration
* Login
* Invalid login
* Admin login
* Logout

### Catalogue

* Search
* Filters
* Multiple filters
* Sorting
* Pagination
* Details

### User Features

* Favourites
* Recently viewed
* Saved searches
* Compare
* Four-car limit
* Shortlisting

### Find My Car

* Budget
* Fuel
* Transmission
* Body type
* Seating
* EV range
* No-match case

### Admin

* Dashboard
* Add car
* Edit car
* Deactivate/delete
* Users
* Authorization

---

# 25. IMPORTANT CLASS 12 RULE

The finished code must be something a Class 12 CBSE student can realistically understand and explain.

If there are two ways to implement something:

**Choose the simpler implementation.**

Do not make the code unnecessarily sophisticated just because the application looks professional.

The complexity should be in the **features and UI**, not in unnecessarily complicated Python.

---

# 26. FINAL ACCEPTANCE CRITERIA

The project is complete only when:

* Application launches correctly
* MySQL connects correctly
* `CarSaga` initializes safely
* Registration works
* Login works
* Roles work
* Catalogue works
* Search works
* Filters work
* Sorting works
* Pagination works
* Details work
* Favourites work
* Recently Viewed works
* Saved Searches work
* Compare supports exactly up to 4 cars
* Find My Car works
* Recommendations explain their matches
* Shortlisting works
* EV data is correct
* Admin dashboard works
* Admin CRUD works
* SQL is parameterized
* Passwords use bcrypt
* User data is isolated
* Existing data is preserved
* UI is polished
* Code remains Class 12 level
* No major feature is fake or merely visual
* Documentation matches the actual implementation

---

# FINAL INSTRUCTION

Build **Car Saga as one integrated application**, not as disconnected screens.

Before writing new code, inspect the existing implementation if one is provided.

Keep the project **simple enough for a Class 12 CBSE student to explain**, but make the final application look polished, modern and professional.

Prioritize:

**Correctness → Database integrity → Security → Functionality → UI quality → Simplicity of code**

Do not over-engineer.
Do not invent unnecessary features.
Do not break existing functionality.
Do not use complicated code where simple code will work.
