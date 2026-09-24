-- =====================================================================
-- CAR SAGA — REALISTIC SEED DATA (MySQL / CBSE Class 12 CS)
-- =====================================================================

INSERT IGNORE INTO roles (id, name) VALUES
(1, 'ADMIN'),
(2, 'USER');

INSERT IGNORE INTO brands (id, name) VALUES
(1, 'Maruti Suzuki'),
(2, 'Hyundai'),
(3, 'Mahindra'),
(4, 'Tata'),
(5, 'Toyota'),
(6, 'Kia'),
(7, 'MG'),
(8, 'Honda'),
(9, 'Skoda');

INSERT IGNORE INTO fuel_types (id, name) VALUES
(1, 'Petrol'),
(2, 'Diesel'),
(3, 'Electric'),
(4, 'Hybrid');

INSERT IGNORE INTO transmission_types (id, name) VALUES
(1, 'Manual'),
(2, 'Automatic');

INSERT IGNORE INTO body_types (id, name) VALUES
(1, 'Hatchback'),
(2, 'Sedan'),
(3, 'SUV'),
(4, 'MPV');

INSERT IGNORE INTO features (id, name) VALUES
(1, 'Anti-lock Braking System (ABS)'),
(2, '6 Airbags'),
(3, 'Touchscreen Infotainment (10.25 inch)'),
(4, 'Reverse Parking Camera with Sensors'),
(5, 'Electric Sunroof'),
(6, 'Cruise Control'),
(7, 'Automatic Climate Control'),
(8, 'Wireless Smartphone Charging'),
(9, 'Diamond Cut Alloy Wheels'),
(10, 'Ventilated Front Seats'),
(11, 'ADAS Level 2 Safety');

-- Users: Admin (admin / admin123) and Demo (demo / demo123)
INSERT IGNORE INTO users (id, full_name, username, email, password_hash, role_id) VALUES
(1, 'System Administrator', 'admin', 'admin@carsaga.com', '$2b$12$QsQ6xv3qwCXU35r755IfveV6F/VCU3Cs9jt7fEp8a81SsOuHvPGrK', 1),
(2, 'Demo Student', 'demo', 'demo@carsaga.com', '$2b$12$nZrYPBS3Aep4FsGSAWCu8O2yfPB60RRg1qI/F/Lvhrh/ZgtLWtK7q', 2);

-- 14 Realistic Diverse Cars (Covering Hatchback, Sedan, SUV, MPV, Petrol, Diesel, EV, Hybrid)
INSERT IGNORE INTO cars (
    id, brand_id, model, variant, model_year, price, fuel_id, transmission_id, body_id,
    engine_capacity, power_kw, torque, mileage, ev_range, battery_capacity, seating_capacity,
    boot_capacity, ground_clearance, safety_info, description, image_url, availability, is_active
) VALUES
(
    1, 1, 'Nexon', 'Fearless Plus', 2024, 1180000.00, 1, 1, 3,
    '1.2L Turbo Petrol', '120 hp', '170 Nm', 17.10, 0.00, '', 5,
    '382 L', '208 mm', '5-Star Bharat NCAP, ESP, Dual Airbags',
    'A rugged and feature-packed compact SUV known for unmatched structural safety, punchy turbo power, and comfortable ride quality.',
    '', 'Available', 1
),
(
    2, 1, 'Nexon EV', 'Empowered Plus 45', 2024, 1549000.00, 3, 2, 3,
    'Permanent Magnet Synchronous Motor', '145 hp', '215 Nm', 0.00, 465.00, '40.5 kWh', 5,
    '350 L', '205 mm', '5-Star Bharat NCAP, 6 Airbags, ESP, Auto-Hold',
    'India leading electric SUV offering exhilarating instant torque, vehicle-to-load charging, 465 km certified range, and quiet city cruising.',
    '', 'Available', 1
),
(
    3, 2, 'Creta', 'SX Tech', 2024, 1598000.00, 1, 2, 3,
    '1.5L MPi Petrol', '115 hp', '144 Nm', 17.80, 0.00, '', 5,
    '433 L', '190 mm', 'Level 2 ADAS, 6 Airbags, All Wheel Disc Brakes',
    'The quintessential family SUV with commanding road presence, panoramic sunroof, premium acoustic sound, and connected car technology.',
    '', 'Available', 1
),
(
    4, 2, 'i20', 'Asta (O)', 2024, 977000.00, 1, 1, 1,
    '1.2L Kappa Petrol', '83 hp', '114 Nm', 20.35, 0.00, '', 5,
    '311 L', '170 mm', '6 Airbags standard, ESC, Hill Assist',
    'A modern premium hatchback loaded with high-tech conveniences, sporty European styling, and nimble city maneuverability.',
    '', 'Available', 1
),
(
    5, 3, 'Brezza', 'ZXi Plus', 2024, 1250000.00, 1, 2, 3,
    '1.5L K15C Smart Hybrid', '103 hp', '137 Nm', 19.89, 0.00, '', 5,
    '328 L', '198 mm', 'Head-Up Display, 360-View Camera, 6 Airbags',
    'Reliable compact SUV engineered for low running costs, seamless torque-converter automatic, and robust suspension for Indian roads.',
    '', 'Available', 1
),
(
    6, 3, 'Baleno', 'Alpha', 2024, 938000.00, 1, 1, 1,
    '1.2L DualJet Petrol', '89 hp', '113 Nm', 22.35, 0.00, '', 5,
    '318 L', '170 mm', '6 Airbags, ABS with EBD, Brake Assist',
    'India highest-mileage premium hatchback featuring head-up display, spacious rear legroom, and refined four-cylinder efficiency.',
    '', 'Available', 1
),
(
    7, 4, 'XUV700', 'AX7 L', 2024, 2499000.00, 2, 2, 3,
    '2.2L mHawk Turbo Diesel', '185 hp', '450 Nm', 15.20, 0.00, '', 7,
    '460 L', '200 mm', '5-Star Global NCAP, Level 2 ADAS, 7 Airbags',
    'A powerhouse 7-seater SUV equipped with twin digital cockpit screens, luxury Sony audio, massive diesel torque, and highway stability.',
    '', 'Available', 1
),
(
    8, 4, 'Thar', 'LX Hard Top 4x4', 2024, 1620000.00, 2, 1, 3,
    '2.2L mHawk CRDe Diesel', '130 hp', '300 Nm', 14.50, 0.00, '', 4,
    '600 L', '226 mm', 'Built-in Roll Cage, 4-Star Global NCAP, Dual Airbags',
    'An iconic 4x4 off-roader with shift-on-the-fly four-wheel-drive low range, unmatched ground clearance, and adventurous road presence.',
    '', 'Available', 1
),
(
    9, 5, 'Innova HyCross', 'ZX(O) Hybrid', 2024, 3098000.00, 4, 2, 4,
    '2.0L Strong Hybrid Electric', '186 hp', '188 Nm + Motor', 23.24, 0.00, 'Self-Charging Battery', 7,
    '640 L', '190 mm', 'Toyota Safety Sense ADAS, 6 Airbags, Ottoman Seats',
    'The pinnacle of long-distance family touring with electric ottoman captain chairs, super-silent EV drive mode, and unbelievable MPV fuel economy.',
    '', 'Available', 1
),
(
    10, 5, 'Urban Cruiser Hyryder', 'V Strong Hybrid', 2024, 1999000.00, 4, 2, 3,
    '1.5L e-CVT Strong Hybrid', '116 hp', '141 Nm', 27.97, 0.00, 'Lithium-Ion Battery', 5,
    '373 L', '210 mm', '6 Airbags, 360 Camera, TPMS',
    'Segment-leading fuel economy champion with self-charging hybrid technology allowing over 50 percent of city driving in pure electric mode.',
    '', 'Available', 1
),
(
    11, 8, 'Seltos', 'GTX Plus', 2024, 1980000.00, 2, 2, 3,
    '1.5L CRDi VGT Diesel', '116 hp', '250 Nm', 18.00, 0.00, '', 5,
    '433 L', '190 mm', 'Level 2 ADAS with 17 features, 6 Airbags',
    'Aggressive styling with dual-pane panoramic sunroof, dual 10.25-inch panoramic screens, and responsive diesel-automatic powertrain.',
    '', 'Available', 1
),
(
    12, 9, 'ZS EV', 'Exclusive Pro', 2024, 2398000.00, 3, 2, 3,
    'Permanent Magnet Motor', '176 hp', '280 Nm', 0.00, 461.00, '50.3 kWh', 5,
    '470 L', '177 mm', '5-Star Euro NCAP, Level 2 ADAS, 6 Airbags',
    'Global premium electric SUV with a massive 50.3 kWh battery pack, ultra-luxurious soft-touch cabin, panoramic glass roof, and fast DC charging.',
    '', 'Available', 1
),
(
    13, 6, 'City', 'ZX', 2024, 1635000.00, 1, 2, 2,
    '1.5L i-VTEC DOHC Petrol', '121 hp', '145 Nm', 18.40, 0.00, '', 5,
    '506 L', '165 mm', 'Honda Sensing ADAS, LaneWatch Camera, 6 Airbags',
    'The timeless benchmark executive sedan featuring legendary high-revving i-VTEC refinement, couch-like rear comfort, and cavernous 506L boot.',
    '', 'Available', 1
),
(
    14, 7, 'Slavia', 'Style 1.5 TSI DSG', 2024, 1840000.00, 1, 2, 2,
    '1.5L TSI Turbocharged Petrol', '150 hp', '250 Nm', 19.30, 0.00, '', 5,
    '521 L', '179 mm', '5-Star Global NCAP adult & child, Multi-Collision Brake',
    'European driver car with rapid 7-speed DSG dual-clutch transmission, 150 hp turbocharged surge, and class-leading high-speed dynamics.',
    '', 'Available', 1
),
(
    15, 5, 'Etios', 'Platinum VX', 2020, 785000.00, 1, 1, 2,
    '1.5L 4-Cylinder Petrol', '88 hp', '132 Nm', 16.78, 0.00, '', 5,
    '592 L', '174 mm', '4-Star Global NCAP, ABS with EBD, Dual Airbags, ISOFIX',
    'A spacious and highly dependable executive sedan renowned for exceptional rear legroom, class-leading 592-litre boot space, 4-Star NCAP safety, and legendary Toyota reliability.',
    '', 'Available', 1
);

-- Car Features Matrix
INSERT IGNORE INTO car_features (car_id, feature_id) VALUES
-- 1: Nexon Petrol
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
-- 2: Nexon EV
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 10),
-- 3: Creta
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 10), (3, 11),
-- 4: i20
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
-- 5: Brezza
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
-- 6: Baleno
(6, 1), (6, 2), (6, 3), (6, 4), (6, 6), (6, 7), (6, 8), (6, 9),
-- 7: XUV700
(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (7, 10), (7, 11),
-- 8: Thar
(8, 1), (8, 3), (8, 4), (8, 6), (8, 7), (8, 9),
-- 9: Innova HyCross
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11),
-- 10: Hyryder
(10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
-- 11: Seltos
(11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11),
-- 12: MG ZS EV
(12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11),
-- 13: Honda City
(13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 11),
-- 14: Skoda Slavia
(14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10),
-- 15: Toyota Etios
(15, 1), (15, 4), (15, 7);
