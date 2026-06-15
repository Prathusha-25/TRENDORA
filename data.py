import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Trend Data ──────────────────────────────────────────────────────────────
TRENDS = [
    {"id": 1, "name": "Baggy Cargo Pants", "category": "Bottoms", "heat": 94,
     "direction": "🔥 Viral", "city": "Hyderabad", "change": "+38%",
     "tags": ["streetwear", "Gen-Z", "unisex"], "urgency": "HIGH",
     "description": "Cargo silhouettes dominating local markets. Demand spike driven by college campuses.",
     "peak_weeks": 6, "image_hint": "cargo"},

    {"id": 2, "name": "Pastel Oversized Shirts", "category": "Tops", "heat": 87,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+24%",
     "tags": ["summer", "unisex", "casual"], "urgency": "HIGH",
     "description": "Pastel colour-blocked shirts trending across Instagram reels.",
     "peak_weeks": 8, "image_hint": "shirt"},

    {"id": 3, "name": "Co-ord Sets (Ethnic Fusion)", "category": "Sets", "heat": 82,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+19%",
     "tags": ["fusion", "women", "festive"], "urgency": "MEDIUM",
     "description": "Ethnic-modern fusion co-ords gaining traction pre-festive season.",
     "peak_weeks": 10, "image_hint": "coord"},

    {"id": 4, "name": "Relaxed Linen Trousers", "category": "Bottoms", "heat": 71,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+15%",
     "tags": ["summer", "workwear", "sustainable"], "urgency": "MEDIUM",
     "description": "Comfort-work hybrid trend. Linen in muted earth tones.",
     "peak_weeks": 12, "image_hint": "linen"},

    {"id": 5, "name": "Logo Crop Hoodies", "category": "Tops", "heat": 65,
     "direction": "→ Stable", "city": "Hyderabad", "change": "+4%",
     "tags": ["streetwear", "women", "casual"], "urgency": "LOW",
     "description": "Holding steady. Good consistent seller but no surge expected.",
     "peak_weeks": 16, "image_hint": "hoodie"},

    {"id": 6, "name": "Formal Straight-Cut Blazers", "category": "Outerwear", "heat": 38,
     "direction": "📉 Declining", "city": "Hyderabad", "change": "-12%",
     "tags": ["formal", "office", "classic"], "urgency": "DEAD_STOCK",
     "description": "Post-pandemic formal wear slowing down. Reduce inventory now.",
     "peak_weeks": 0, "image_hint": "blazer"},

    {"id": 7, "name": "Crochet Mini Skirts", "category": "Bottoms", "heat": 79,
     "direction": "📈 Rising", "city": "Hyderabad", "change": "+21%",
     "tags": ["boho", "summer", "women"], "urgency": "HIGH",
     "description": "Crochet textures exploding on social. Boutique favourite.",
     "peak_weeks": 7, "image_hint": "skirt"},

    {"id": 8, "name": "Printed Maxi Dresses", "category": "Dresses", "heat": 85,
     "direction": "🔥 Viral", "city": "Hyderabad", "change": "+29%",
     "tags": ["summer", "women", "festive"], "urgency": "HIGH",
     "description": "Bold prints in floral and abstract trending hard this season.",
     "peak_weeks": 5, "image_hint": "dress"},
]

# ── Inventory Data ────────────────────────────────────────────────────────────
INVENTORY = [
    {"sku": "BGC-001", "name": "Baggy Cargo Pants - Olive", "qty": 12, "reorder_point": 30,
     "cost": 480, "selling_price": 1299, "days_of_stock": 4, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Bottoms", "trend_alignment": 94},

    {"sku": "PST-002", "name": "Pastel Oversized Shirt - Blue", "qty": 8, "reorder_point": 25,
     "cost": 320, "selling_price": 899, "days_of_stock": 5, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Tops", "trend_alignment": 87},

    {"sku": "CRD-003", "name": "Ethnic Co-ord Set - Beige", "qty": 34, "reorder_point": 20,
     "cost": 650, "selling_price": 1799, "days_of_stock": 18, "velocity": "Medium",
     "status": "HEALTHY", "category": "Sets", "trend_alignment": 82},

    {"sku": "LIN-004", "name": "Linen Trouser - Sand", "qty": 45, "reorder_point": 15,
     "cost": 390, "selling_price": 999, "days_of_stock": 28, "velocity": "Medium",
     "status": "HEALTHY", "category": "Bottoms", "trend_alignment": 71},

    {"sku": "BLZ-005", "name": "Straight Blazer - Black", "qty": 78, "reorder_point": 10,
     "cost": 890, "selling_price": 1499, "days_of_stock": 90, "velocity": "Slow",
     "status": "DEAD STOCK", "category": "Outerwear", "trend_alignment": 38},

    {"sku": "CRC-006", "name": "Crochet Mini Skirt - White", "qty": 6, "reorder_point": 20,
     "cost": 280, "selling_price": 799, "days_of_stock": 3, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Bottoms", "trend_alignment": 79},

    {"sku": "MAX-007", "name": "Printed Maxi Dress - Floral", "qty": 9, "reorder_point": 25,
     "cost": 540, "selling_price": 1499, "days_of_stock": 4, "velocity": "Fast",
     "status": "REORDER NOW", "category": "Dresses", "trend_alignment": 85},

    {"sku": "HDD-008", "name": "Logo Crop Hoodie - Pink", "qty": 52, "reorder_point": 15,
     "cost": 420, "selling_price": 999, "days_of_stock": 35, "velocity": "Slow",
     "status": "OVERSTOCK", "category": "Tops", "trend_alignment": 65},
]

# ── Pricing Data ──────────────────────────────────────────────────────────────
PRICING = [
    {"product": "Baggy Cargo Pants", "your_price": 1299, "market_avg": 1350,
     "low": 999, "high": 1799, "suggested": 1399, "margin_pct": 63, "opportunity": "Price UP ↑"},

    {"product": "Pastel Oversized Shirt", "your_price": 899, "market_avg": 849,
     "low": 699, "high": 1199, "suggested": 949, "margin_pct": 64, "opportunity": "Price UP ↑"},

    {"product": "Ethnic Co-ord Set", "your_price": 1799, "market_avg": 1899,
     "low": 1499, "high": 2499, "suggested": 1899, "margin_pct": 64, "opportunity": "Price UP ↑"},

    {"product": "Crochet Mini Skirt", "your_price": 799, "market_avg": 899,
     "low": 599, "high": 1299, "suggested": 899, "margin_pct": 71, "opportunity": "Price UP ↑"},

    {"product": "Printed Maxi Dress", "your_price": 1499, "market_avg": 1599,
     "low": 1199, "high": 2199, "suggested": 1649, "margin_pct": 66, "opportunity": "Price UP ↑"},

    {"product": "Logo Crop Hoodie", "your_price": 999, "market_avg": 849,
     "low": 699, "high": 1099, "suggested": 849, "margin_pct": 50, "opportunity": "Reduce Price ↓"},

    {"product": "Straight Blazer", "your_price": 1499, "market_avg": 1099,
     "low": 799, "high": 1399, "suggested": 999, "margin_pct": 12, "opportunity": "Clearance Sale 🔥"},
]

# ── Wholesaler Data ───────────────────────────────────────────────────────────
WHOLESALERS = [
    {
        "id": 1, "name": "Rajesh Textiles & Exports", "city": "Surat",
        "rating": 4.8, "verified": True, "years": 14,
        "products": [
            {"name": "Baggy Cargo Pants (Bulk)", "moq": 50, "price_per_unit": 320,
             "fabric": "Cotton-Poly Blend", "sizes": "S-XXL", "colors": 8,
             "lead_days": 7, "category": "Bottoms"},
            {"name": "Relaxed Linen Trousers", "moq": 30, "price_per_unit": 280,
             "fabric": "Pure Linen", "sizes": "S-XL", "colors": 5,
             "lead_days": 10, "category": "Bottoms"},
        ],
        "tags": ["BESTSELLER", "FAST DISPATCH"],
        "min_order_value": 15000,
        "speciality": "Bottoms & Denims"
    },
    {
        "id": 2, "name": "Femina Fashion House", "city": "Jaipur",
        "rating": 4.6, "verified": True, "years": 9,
        "products": [
            {"name": "Pastel Oversized Shirts (Bulk)", "moq": 60, "price_per_unit": 210,
             "fabric": "Rayon Georgette", "sizes": "S-XXL", "colors": 12,
             "lead_days": 5, "category": "Tops"},
            {"name": "Printed Maxi Dresses", "moq": 40, "price_per_unit": 380,
             "fabric": "Chiffon / Georgette", "sizes": "S-XL", "colors": 10,
             "lead_days": 8, "category": "Dresses"},
            {"name": "Crochet Mini Skirts", "moq": 25, "price_per_unit": 195,
             "fabric": "Crochet Cotton", "sizes": "XS-L", "colors": 6,
             "lead_days": 12, "category": "Bottoms"},
        ],
        "tags": ["TOP RATED", "WOMEN'S SPECIALIST"],
        "min_order_value": 12000,
        "speciality": "Women's Fashion"
    },
    {
        "id": 3, "name": "StyleSync Wholesale Hub", "city": "Mumbai",
        "rating": 4.4, "verified": True, "years": 6,
        "products": [
            {"name": "Ethnic Co-ord Sets (Fusion)", "moq": 20, "price_per_unit": 450,
             "fabric": "Chanderi / Cotton Silk", "sizes": "S-XL", "colors": 8,
             "lead_days": 14, "category": "Sets"},
            {"name": "Logo Crop Hoodies", "moq": 50, "price_per_unit": 280,
             "fabric": "French Terry", "sizes": "XS-XXL", "colors": 7,
             "lead_days": 6, "category": "Tops"},
        ],
        "tags": ["LOW MOQ", "TREND-FORWARD"],
        "min_order_value": 8000,
        "speciality": "Fusion & Streetwear"
    },
    {
        "id": 4, "name": "Apex Knitwear Co.", "city": "Tirupur",
        "rating": 4.9, "verified": True, "years": 21,
        "products": [
            {"name": "Premium Crop Hoodies (Bulk)", "moq": 100, "price_per_unit": 195,
             "fabric": "Fleece / Terry", "sizes": "XS-3XL", "colors": 15,
             "lead_days": 10, "category": "Tops"},
        ],
        "tags": ["EXPORT QUALITY", "LARGE BATCHES"],
        "min_order_value": 20000,
        "speciality": "Knitwear & Hosiery"
    },
]

# ── Demand Forecast (Weekly) ──────────────────────────────────────────────────
def get_forecast_data():
    weeks = [f"W{i}" for i in range(1, 13)]
    return {
        "weeks": weeks,
        "Baggy Cargo Pants": [18, 24, 32, 41, 55, 68, 74, 70, 62, 50, 38, 28],
        "Pastel Oversized Shirts": [22, 28, 35, 44, 52, 61, 65, 60, 52, 42, 30, 22],
        "Crochet Mini Skirts": [12, 18, 28, 40, 54, 62, 68, 65, 55, 42, 28, 18],
        "Printed Maxi Dresses": [30, 38, 48, 58, 65, 70, 68, 60, 48, 35, 24, 18],
        "Formal Blazers": [20, 18, 15, 12, 10, 8, 7, 6, 6, 5, 5, 4],
    }

# ── Sales History ─────────────────────────────────────────────────────────────
def get_sales_history():
    dates = pd.date_range(end=datetime.today(), periods=30, freq='D')
    return pd.DataFrame({
        "date": dates,
        "revenue": np.random.randint(8000, 28000, 30),
        "units_sold": np.random.randint(15, 65, 30),
        "avg_order": np.random.randint(600, 1800, 30),
    })

CATEGORIES = ["All", "Tops", "Bottoms", "Dresses", "Sets", "Outerwear"]