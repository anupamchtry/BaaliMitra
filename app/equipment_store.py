from flask import Blueprint, render_template, request, jsonify, url_for
import os
import json
from pathlib import Path

equipment_bp = Blueprint('equipment', __name__, template_folder='../templates', static_folder='../static')

BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))
EQUIPMENT_DB_PATH = BASE_DIR / 'database' / 'equipment.json'
EQUIPMENT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Sample equipment data
SAMPLE_EQUIPMENT = {
    "equipment": [
        {
            "id": 1,
            "name": "Hand Hoe",
            "category": "Hand Tools",
            "type": "equipment",
            "price_buy": 150,
            "price_rent": 15,
            "rent_period": "per day",
            "description": "Essential hand tool for weeding and soil cultivation",
            "image": "images/equipment/hand-hoe.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 25,
            "rating": 4.5,
            "reviews": 45,
            "specifications": {
                "Material": "Steel blade with wooden handle",
                "Weight": "0.8 kg",
                "Length": "35 cm"
            }
        },
        {
            "id": 2,
            "name": "Watering Can",
            "category": "Irrigation",
            "type": "equipment",
            "price_buy": 300,
            "price_rent": 25,
            "rent_period": "per day",
            "description": "10-liter capacity watering can for garden irrigation",
            "image": "images/equipment/watering-can.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 15,
            "rating": 4.2,
            "reviews": 32,
            "specifications": {
                "Capacity": "10 liters",
                "Material": "Galvanized steel",
                "Weight": "1.2 kg"
            }
        },
        {
            "id": 3,
            "name": "Garden Rake",
            "category": "Hand Tools",
            "type": "equipment",
            "price_buy": 250,
            "price_rent": 20,
            "rent_period": "per day",
            "description": "Multi-purpose rake for soil preparation and cleanup",
            "image": "images/equipment/garden-rake.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 18,
            "rating": 4.3,
            "reviews": 28,
            "specifications": {
                "Teeth": "14 steel teeth",
                "Handle": "Wooden handle 120cm",
                "Weight": "1.0 kg"
            }
        },
        {
            "id": 4,
            "name": "Pruning Shears",
            "category": "Cutting Tools",
            "type": "equipment",
            "price_buy": 400,
            "price_rent": 30,
            "rent_period": "per day",
            "description": "Professional pruning shears for tree and plant maintenance",
            "image": "images/equipment/pruning-shears.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 12,
            "rating": 4.7,
            "reviews": 56,
            "specifications": {
                "Blade": "Stainless steel",
                "Cutting capacity": "25mm diameter",
                "Weight": "0.3 kg"
            }
        }
    ],
    "machinery": [
        {
            "id": 5,
            "name": "Mini Tractor",
            "category": "Tractors",
            "type": "machinery",
            "price_buy": 450000,
            "price_rent": 1500,
            "rent_period": "per day",
            "description": "Compact tractor suitable for small to medium farms",
            "image": "images/machinery/mini-tractor.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 3,
            "rating": 4.6,
            "reviews": 89,
            "specifications": {
                "Engine": "25 HP Diesel",
                "Transmission": "8F+2R",
                "PTO": "540 RPM",
                "Weight": "1200 kg"
            }
        },
        {
            "id": 6,
            "name": "Rotavator",
            "category": "Tillage",
            "type": "machinery",
            "price_buy": 85000,
            "price_rent": 800,
            "rent_period": "per day",
            "description": "Soil preparation equipment for plowing and cultivation",
            "image": "images/machinery/rotavator.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 5,
            "rating": 4.4,
            "reviews": 34,
            "specifications": {
                "Working width": "5 feet",
                "Blades": "L-shaped rotary blades",
                "Power requirement": "25-35 HP",
                "Weight": "350 kg"
            }
        },
        {
            "id": 7,
            "name": "Seed Drill",
            "category": "Sowing",
            "type": "machinery",
            "price_buy": 65000,
            "price_rent": 600,
            "rent_period": "per day",
            "description": "Precision seed drilling machine for uniform sowing",
            "image": "images/machinery/seed-drill.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 4,
            "rating": 4.5,
            "reviews": 67,
            "specifications": {
                "Rows": "9 rows",
                "Row spacing": "18-23 cm adjustable",
                "Seed box capacity": "80 kg",
                "Weight": "280 kg"
            }
        },
        {
            "id": 8,
            "name": "Water Pump",
            "category": "Irrigation",
            "type": "machinery",
            "price_buy": 12000,
            "price_rent": 200,
            "rent_period": "per day",
            "description": "Centrifugal water pump for irrigation systems",
            "image": "images/machinery/water-pump.jpg",
            "available_buy": True,
            "available_rent": True,
            "stock": 8,
            "rating": 4.3,
            "reviews": 123,
            "specifications": {
                "Power": "5 HP Motor",
                "Flow rate": "500 liters/minute",
                "Head": "25 meters",
                "Weight": "45 kg"
            }
        }
    ]
}

def _read_equipment_db():
    try:
        if not EQUIPMENT_DB_PATH.exists():
            _write_equipment_db(SAMPLE_EQUIPMENT)
        with open(EQUIPMENT_DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return SAMPLE_EQUIPMENT

def _write_equipment_db(data):
    with open(EQUIPMENT_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@equipment_bp.route('/equipment-store')
def equipment_store_page():
    return render_template('equipment-store.html')

@equipment_bp.route('/api/equipment/items', methods=['GET'])
def get_equipment_items():
    """Get all equipment and machinery items"""
    data = _read_equipment_db()
    category = request.args.get('category', 'all')
    item_type = request.args.get('type', 'all')
    
    all_items = []
    if category == 'all' or category == 'equipment':
        all_items.extend(data.get('equipment', []))
    if category == 'all' or category == 'machinery':
        all_items.extend(data.get('machinery', []))
    
    # Filter by type if specified
    if item_type != 'all':
        all_items = [item for item in all_items if item.get('type') == item_type]
    
    return jsonify({"items": all_items, "total": len(all_items)})

@equipment_bp.route('/api/equipment/item/<int:item_id>', methods=['GET'])
def get_equipment_item(item_id):
    """Get specific equipment item by ID"""
    data = _read_equipment_db()
    all_items = data.get('equipment', []) + data.get('machinery', [])
    
    item = next((item for item in all_items if item['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify({"item": item})

@equipment_bp.route('/api/equipment/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    data = _read_equipment_db()
    all_items = data.get('equipment', []) + data.get('machinery', [])
    
    categories = list(set(item.get('category', 'Other') for item in all_items))
    categories.sort()
    
    return jsonify({"categories": categories})

@equipment_bp.route('/api/equipment/search', methods=['GET'])
def search_equipment():
    """Search equipment by name or description"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"items": [], "total": 0})
    
    data = _read_equipment_db()
    all_items = data.get('equipment', []) + data.get('machinery', [])
    
    # Search in name and description
    matching_items = []
    for item in all_items:
        if (query in item.get('name', '').lower() or 
            query in item.get('description', '').lower() or
            query in item.get('category', '').lower()):
            matching_items.append(item)
    
    return jsonify({"items": matching_items, "total": len(matching_items)})

@equipment_bp.route('/api/equipment/rent', methods=['POST'])
def rent_equipment():
    """Handle equipment rental request"""
    data = request.get_json()
    
    required_fields = ['item_id', 'customer_name', 'phone', 'address', 'rental_days']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # In a real application, you would:
    # 1. Validate customer information
    # 2. Check item availability
    # 3. Calculate total cost
    # 4. Create rental record
    # 5. Update inventory
    
    equipment_data = _read_equipment_db()
    all_items = equipment_data.get('equipment', []) + equipment_data.get('machinery', [])
    item = next((item for item in all_items if item['id'] == data['item_id']), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    if not item.get('available_rent', False):
        return jsonify({"error": "Item not available for rent"}), 400
    
    total_cost = item['price_rent'] * int(data['rental_days'])
    
    rental_record = {
        "id": f"RENT_{data['item_id']}_{int(__import__('time').time())}",
        "item_id": data['item_id'],
        "item_name": item['name'],
        "customer_name": data['customer_name'],
        "phone": data['phone'],
        "address": data['address'],
        "rental_days": int(data['rental_days']),
        "daily_rate": item['price_rent'],
        "total_cost": total_cost,
        "status": "pending",
        "created_at": __import__('datetime').datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "message": "Rental request submitted successfully",
        "rental_id": rental_record['id'],
        "total_cost": total_cost,
        "rental_record": rental_record
    })

@equipment_bp.route('/api/equipment/buy', methods=['POST'])
def buy_equipment():
    """Handle equipment purchase request"""
    data = request.get_json()
    
    required_fields = ['item_id', 'customer_name', 'phone', 'address', 'quantity']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    equipment_data = _read_equipment_db()
    all_items = equipment_data.get('equipment', []) + equipment_data.get('machinery', [])
    item = next((item for item in all_items if item['id'] == data['item_id']), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    if not item.get('available_buy', False):
        return jsonify({"error": "Item not available for purchase"}), 400
    
    quantity = int(data['quantity'])
    if quantity > item.get('stock', 0):
        return jsonify({"error": "Insufficient stock"}), 400
    
    total_cost = item['price_buy'] * quantity
    
    purchase_record = {
        "id": f"BUY_{data['item_id']}_{int(__import__('time').time())}",
        "item_id": data['item_id'],
        "item_name": item['name'],
        "customer_name": data['customer_name'],
        "phone": data['phone'],
        "address": data['address'],
        "quantity": quantity,
        "unit_price": item['price_buy'],
        "total_cost": total_cost,
        "status": "pending",
        "created_at": __import__('datetime').datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "message": "Purchase request submitted successfully",
        "order_id": purchase_record['id'],
        "total_cost": total_cost,
        "purchase_record": purchase_record
    })

@equipment_bp.route('/api/equipment/stats', methods=['GET'])
def get_equipment_stats():
    """Get equipment store statistics"""
    data = _read_equipment_db()
    equipment_items = data.get('equipment', [])
    machinery_items = data.get('machinery', [])
    
    stats = {
        "total_equipment": len(equipment_items),
        "total_machinery": len(machinery_items),
        "total_items": len(equipment_items) + len(machinery_items),
        "available_for_rent": len([item for item in equipment_items + machinery_items if item.get('available_rent')]),
        "available_for_buy": len([item for item in equipment_items + machinery_items if item.get('available_buy')]),
        "categories": len(set(item.get('category') for item in equipment_items + machinery_items)),
        "total_value": sum(item.get('price_buy', 0) * item.get('stock', 0) for item in equipment_items + machinery_items)
    }
    
    return jsonify({"stats": stats})