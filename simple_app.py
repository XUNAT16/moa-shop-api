from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SM Mall of Asia Shop Directory
SHOPS = {
    "uniqlo": {
        "name": "Uniqlo",
        "location": "Main Mall, Ground Level – South Wing, near H&M and Crocs",
        "category": "Apparel / Fashion"
    },
    "h&m": {
        "name": "H&M",
        "location": "Main Mall, Ground Level – South Wing, near Uniqlo",
        "category": "Apparel / Fashion"
    },
    "muji": {
        "name": "MUJI",
        "location": "Main Mall, Ground Level – South Wing",
        "category": "Home & Lifestyle"
    },
    "shake shack": {
        "name": "Shake Shack",
        "location": "Main Mall, Ground Level – North Wing, near the Food Hall",
        "category": "Food & Dining"
    },
    "starbucks": {
        "name": "Starbucks",
        "location": "Main Mall, Ground Level – Central Atrium",
        "category": "Food & Dining / Coffee"
    },
    "watsons": {
        "name": "Watsons",
        "location": "Main Mall, Ground Level – South Wing",
        "category": "Health & Beauty"
    },
    "sm supermarket": {
        "name": "SM Supermarket",
        "location": "Main Mall, Lower Ground Level",
        "category": "Grocery & Supermarket"
    },
    "forever 21": {
        "name": "Forever 21",
        "location": "Main Mall, Ground Level – South Wing",
        "category": "Apparel / Fashion"
    },
    "zara": {
        "name": "Zara",
        "location": "Main Mall, Ground Level – South Wing",
        "category": "Apparel / Fashion"
    },
    "power mac center": {
        "name": "Power Mac Center",
        "location": "Main Mall, Ground Level – North Wing",
        "category": "Electronics"
    },
    "mcdonald's": {
        "name": "McDonald's",
        "location": "Main Mall, Ground Level – Food Court Area",
        "category": "Food & Dining / Fast Food"
    },
    "jollibee": {
        "name": "Jollibee",
        "location": "Main Mall, Ground Level – near Atrium",
        "category": "Food & Dining / Fast Food"
    },
    "miniso": {
        "name": "Miniso",
        "location": "Main Mall, Ground Level – South Wing",
        "category": "Home & Lifestyle"
    },
    "national bookstore": {
        "name": "National Bookstore",
        "location": "Main Mall, Ground Level – North Wing",
        "category": "Books & Stationery"
    },
    "timezone": {
        "name": "Timezone",
        "location": "Main Mall, Upper Ground Level – Entertainment Area",
        "category": "Entertainment / Gaming"
    }
}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "SM Mall of Asia Shop Directory API",
        "endpoints": {
            "search": "/search?shop=uniqlo",
            "categories": "/categories",
            "category_shops": "/category?name=Food & Dining",
            "popular": "/popular"
        }
    })

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Handle both GET and POST
    if request.method == 'POST':
        data = request.get_json() or {}
        shop_query = data.get('shop', data.get('name', '')).lower().strip()
    else:
        shop_query = request.args.get('shop', request.args.get('name', '')).lower().strip()
    
    if not shop_query:
        return jsonify({"error": "Please provide a shop name"}), 400
    
    # Search for shop
    if shop_query in SHOPS:
        shop = SHOPS[shop_query]
        message = f"🛍️ *{shop['name']}*\n\n📍 *Location:*\n{shop['location']}\n\n🏷️ *Category:* {shop['category']}"
        
        return jsonify({
            "found": True,
            "shop": shop,
            "message": message
        }), 200
    
    return jsonify({
        "found": False,
        "message": f"Sorry, I couldn't find '{shop_query}' in SM Mall of Asia. Try: uniqlo, h&m, muji, shake shack, starbucks"
    }), 404

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    categories = set(shop['category'] for shop in SHOPS.values())
    categories_list = sorted(list(categories))
    
    message = "📂 *Shop Categories at SM Mall of Asia:*\n\n"
    for i, cat in enumerate(categories_list, 1):
        message += f"{i}. {cat}\n"
    
    return jsonify({
        "categories": categories_list,
        "message": message
    }), 200

@app.route('/category', methods=['GET', 'POST'])
def get_category_shops():
    """Get shops by category"""
    if request.method == 'POST':
        data = request.get_json() or {}
        category = data.get('category', data.get('name', '')).strip()
    else:
        category = request.args.get('category', request.args.get('name', '')).strip()
    
    if not category:
        return jsonify({"error": "Please provide a category name"}), 400
    
    # Find shops in this category (case-insensitive partial match)
    matching_shops = []
    for shop_key, shop_data in SHOPS.items():
        if category.lower() in shop_data['category'].lower():
            matching_shops.append(shop_data)
    
    if matching_shops:
        message = f"🏪 *{category}* shops:\n\n"
        for shop in matching_shops:
            message += f"• *{shop['name']}*\n  📍 {shop['location']}\n\n"
        
        return jsonify({
            "found": True,
            "category": category,
            "count": len(matching_shops),
            "shops": matching_shops,
            "message": message
        }), 200
    
    return jsonify({
        "found": False,
        "message": f"No shops found in category '{category}'"
    }), 404

@app.route('/popular', methods=['GET'])
def get_popular():
    """Get popular/featured shops"""
    popular_shops = ["uniqlo", "h&m", "shake shack", "starbucks", "muji", "jollibee"]
    
    shops_list = []
    message = "⭐ *Popular Shops at SM Mall of Asia:*\n\n"
    
    for i, shop_key in enumerate(popular_shops, 1):
        if shop_key in SHOPS:
            shop = SHOPS[shop_key]
            shops_list.append(shop)
            message += f"{i}. *{shop['name']}*\n   📍 {shop['location']}\n   🏷️ {shop['category']}\n\n"
    
    return jsonify({
        "popular": shops_list,
        "count": len(shops_list),
        "message": message
    }), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
