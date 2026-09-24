"""
Helper functions for formatting, currency, and offline vehicle visuals.
Class 12 CBSE Computer Science standard - simple, readable, and clean.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk


def get_app_logo_image(size=(40, 40)):
    """
    Loads and returns the Car Saga brand logo from assets/logo.png.
    """
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        try:
            pil_img = Image.open(logo_path)
            return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=size)
        except Exception:
            return None
    return None


def format_currency(val):
    """Format numeric price into Indian currency format (e.g. ₹12,40,000)."""
    try:
        amount = int(float(val))
    except (ValueError, TypeError):
        return "₹0"

    s = str(amount)
    if len(s) <= 3:
        return f"₹{s}"

    # Indian number grouping: last 3 digits, then groups of 2
    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
    return f"₹{','.join(parts)},{last_three}"


def format_efficiency(fuel, mileage, ev_range):
    """
    Format efficiency without confusing EV range with fuel mileage.
    CBSE requirement: Do NOT show EV range as km/l.
    """
    if str(fuel).strip().lower() == "electric":
        return f"{int(float(ev_range or 0))} km Range"
    return f"{float(mileage or 0):.1f} km/l"


def get_vehicle_placeholder_image(brand, model, fuel="Petrol", width=240, height=130):
    """
    Generates an offline, clean automotive card graphic using PIL.
    Avoids GUI network lag or frozen screens.
    """
    # Sleek automotive card color palette based on fuel
    fuel_lower = str(fuel).lower()
    if "electric" in fuel_lower:
        bg_color = (20, 45, 65)       # Electric cyan/blue vibe
        accent_color = (0, 200, 255)
        tag_text = "⚡ ELECTRIC"
    elif "hybrid" in fuel_lower:
        bg_color = (25, 55, 40)       # Green eco vibe
        accent_color = (50, 220, 120)
        tag_text = "🌿 HYBRID"
    elif "diesel" in fuel_lower:
        bg_color = (45, 35, 25)       # Warm bronze vibe
        accent_color = (230, 160, 60)
        tag_text = "⛽ DIESEL"
    else:
        bg_color = (32, 36, 44)       # Sleek graphite
        accent_color = (100, 160, 255)
        tag_text = "⛽ PETROL"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Decorative automotive card elements
    # Top accent bar
    draw.rectangle([0, 0, width, 4], fill=accent_color)

    # Background subtle road/car silhouette line
    draw.line([20, height - 35, width - 20, height - 35], fill=(60, 65, 75), width=2)
    # Simple car silhouette outline
    car_points = [
        (40, height - 35),
        (55, height - 50),
        (85, height - 52),
        (110, height - 70),
        (160, height - 70),
        (185, height - 50),
        (205, height - 50),
        (215, height - 35),
    ]
    draw.line(car_points, fill=accent_color, width=2)

    # Wheels
    draw.ellipse([65, height - 42, 85, height - 22], outline=accent_color, width=2, fill=bg_color)
    draw.ellipse([165, height - 42, 185, height - 22], outline=accent_color, width=2, fill=bg_color)

    # Brand & Model text
    brand_text = str(brand).upper()
    model_text = str(model)
    if len(model_text) > 16:
        model_text = model_text[:14] + ".."

    draw.text((15, 14), brand_text, fill=(180, 185, 195))
    draw.text((15, 32), model_text, fill=(255, 255, 255))
    draw.text((width - 95, 14), tag_text, fill=accent_color)

    return ctk.CTkImage(light_image=img, dark_image=img, size=(width, height))
