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
    }
}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "SM Mall of Asia Shop Directory API",
        "endpoints": {
            "search": "/search?shop=uniqlo"
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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
