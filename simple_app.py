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
    },
    "the sm store": {
        "name": "The SM Store - SM Mall of Asia",
        "category": "Department Store",
        "location": "Main Mall, Ground Level – Center Atrium"
    },
    "power mac": {
        "name": "Power Mac Center - SM Mall of Asia",
        "category": "Electronics",
        "location": "Cyberzone, Level 2 – North Wing"
    },
    "beyond the box": {
        "name": "Beyond the Box - SM Mall of Asia",
        "category": "Electronics / Apple Reseller",
        "location": "Cyberzone, Level 2 – North Wing"
    },
    "muji cafe": {
        "name": "Muji Coffee - SM Mall of Asia",
        "category": "Café",
        "location": "South Wing, Level 3 – inside MUJI store"
    },
    "mary grace": {
        "name": "Café Mary Grace - SM Mall of Asia",
        "category": "Café / Bakery",
        "location": "Ground Floor, Main Mall – near The SM Store entrance"
    },
    "tim ho wan": {
        "name": "Tim Ho Wan - SM Mall of Asia",
        "category": "Chinese / Dim Sum Restaurant",
        "location": "Ground Floor, Main Mall – South Wing, near Uniqlo"
    },
    "ramen nagi": {
        "name": "Ramen Nagi - SM Mall of Asia",
        "category": "Japanese Restaurant",
        "location": "Ground Floor, Main Mall – South Wing, near H&M"
    },
    "conti's": {
        "name": "Conti's Bakeshop and Restaurant - SM Mall of Asia",
        "category": "Bakery / Restaurant",
        "location": "Ground Floor, South Wing – near IMAX"
    },
    "imax": {
        "name": "IMAX Theatre - SM Mall of Asia",
        "category": "Entertainment / Cinema",
        "location": "South Wing – SM Cinema Complex, near Parking Building"
    },
    "moa arena": {
        "name": "Mall of Asia Arena",
        "category": "Events / Concert Venue",
        "location": "Across MOA Main Mall, Seaside Blvd."
    },
    "smx": {
        "name": "SMX Convention Center Manila",
        "category": "Convention Center",
        "location": "MOA Complex, beside Conrad Manila"
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
        # Try multiple possible field names that chatbots might use
        shop_query = (data.get('shop') or 
                     data.get('name') or 
                     data.get('query') or 
                     data.get('text') or 
                     data.get('message') or 
                     data.get('user_input') or '').lower().strip()
    else:
        shop_query = (request.args.get('shop') or 
                     request.args.get('name') or 
                     request.args.get('query') or '').lower().strip()
    
    if not shop_query:
        return jsonify({
            "error": "Please provide a shop name",
            "received_data": request.get_json() if request.method == 'POST' else dict(request.args),
            "hint": "Send JSON with 'shop', 'name', 'query', 'text', 'message', or 'user_input' field"
        }), 400
    
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

@app.route('/query', methods=['GET', 'POST'])
def unified_query():
    """Unified endpoint that handles shop search, category browse, and popular picks"""
    
    # Extract parameters
    if request.method == 'POST':
        data = request.get_json() or {}
        query_type = data.get('type', '').lower()
        query_value = data.get('value', '').lower().strip()
    else:
        query_type = request.args.get('type', '').lower()
        query_value = request.args.get('value', '').lower().strip()
    
    # Handle Popular Picks (no value needed)
    if query_type == 'popular':
        popular_shops = ["uniqlo", "h&m", "shake shack", "starbucks", "muji", "jollibee"]
        shops_list = []
        message = "⭐ *Popular Shops at SM Mall of Asia:*\n\n"
        
        for i, shop_key in enumerate(popular_shops, 1):
            if shop_key in SHOPS:
                shop = SHOPS[shop_key]
                shops_list.append(shop)
                message += f"{i}. *{shop['name']}*\n   📍 {shop['location']}\n   🏷️ {shop['category']}\n\n"
        
        return jsonify({
            "found": True,
            "type": "popular",
            "count": len(shops_list),
            "shops": shops_list,
            "message": message
        }), 200
    
    # Handle Category Browse
    elif query_type == 'category':
        if not query_value:
            # Return list of categories
            categories = set(shop['category'] for shop in SHOPS.values())
            categories_list = sorted(list(categories))
            message = "📂 *Shop Categories at SM Mall of Asia:*\n\n"
            for i, cat in enumerate(categories_list, 1):
                message += f"{i}. {cat}\n"
            
            return jsonify({
                "found": True,
                "type": "categories",
                "categories": categories_list,
                "message": message
            }), 200
        else:
            # Search by category
            matching_shops = []
            for shop_key, shop_data in SHOPS.items():
                if query_value in shop_data['category'].lower():
                    matching_shops.append(shop_data)
            
            if matching_shops:
                message = f"🏪 *{query_value.title()}* shops:\n\n"
                for shop in matching_shops:
                    message += f"• *{shop['name']}*\n  📍 {shop['location']}\n\n"
                
                return jsonify({
                    "found": True,
                    "type": "category",
                    "category": query_value,
                    "count": len(matching_shops),
                    "shops": matching_shops,
                    "message": message
                }), 200
            else:
                return jsonify({
                    "found": False,
                    "type": "category",
                    "message": f"No shops found in category '{query_value}'"
                }), 404
    
    # Handle Shop Search (default)
    elif query_type == 'shop' or query_type == '':
        if not query_value:
            return jsonify({
                "error": "Please provide a shop name in 'value' field",
                "hint": "Use type=shop&value=uniqlo or type=category&value=food or type=popular"
            }), 400
        
        # Search for shop
        if query_value in SHOPS:
            shop = SHOPS[query_value]
            message = f"🛍️ *{shop['name']}*\n\n📍 *Location:*\n{shop['location']}\n\n🏷️ *Category:* {shop['category']}"
            
            return jsonify({
                "found": True,
                "type": "shop",
                "shop": shop,
                "message": message
            }), 200
        else:
            return jsonify({
                "found": False,
                "type": "shop",
                "message": f"Sorry, I couldn't find '{query_value}' in SM Mall of Asia. Try: uniqlo, h&m, muji, shake shack, starbucks"
            }), 404
    
    else:
        return jsonify({
            "error": "Invalid query type",
            "hint": "Use type=shop, type=category, or type=popular"
        }), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    """Flexible webhook that accepts any JSON structure and tries to find the shop name"""
    data = request.get_json() or {}
    
    # Try to extract shop name from various possible structures
    shop_query = ''
    
    # Try common field names
    for field in ['shop', 'name', 'query', 'text', 'message', 'user_input', 'user_message', 'content']:
        if field in data and data[field]:
            shop_query = str(data[field]).lower().strip()
            break
    
    # If still no shop_query, try to find it in nested structures
    if not shop_query and 'message' in data and isinstance(data['message'], dict):
        shop_query = str(data['message'].get('text', '')).lower().strip()
    
    # Log what we received for debugging
    if not shop_query:
        return jsonify({
            "error": "Could not find shop name in request",
            "received_data": data,
            "hint": "Please send JSON with one of these fields: shop, name, query, text, message, user_input"
        }), 400
    
    # Search for shop
    if shop_query in SHOPS:
        shop = SHOPS[shop_query]
        message = f"🛍️ *{shop['name']}*\n\n📍 *Location:*\n{shop['location']}\n\n🏷️ *Category:* {shop['category']}"
        
        return jsonify({
            "found": True,
            "shop": shop,
            "message": message,
            "text": message  # Some chatbots look for 'text' field
        }), 200
    
    return jsonify({
        "found": False,
        "message": f"Sorry, I couldn't find '{shop_query}' in SM Mall of Asia. Try: uniqlo, h&m, muji, shake shack, starbucks",
        "text": f"Sorry, I couldn't find '{shop_query}' in SM Mall of Asia. Try: uniqlo, h&m, muji, shake shack, starbucks"
    }), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
