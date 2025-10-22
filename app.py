from flask import Flask, jsonify, request
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SM Mall of Asia Shops Database
shops = {
    "uniqlo": {
        "name": "Uniqlo - SM Mall of Asia",
        "category": "Apparel / Fashion",
        "location": "Main Mall, Ground Level – South Wing, near H&M and Crocs"
    },
    "h&m": {
        "name": "H&M - SM Mall of Asia",
        "category": "Apparel / Fashion",
        "location": "Main Mall, Level 1 – North Wing, beside Uniqlo"
    },
    "the sm store": {
        "name": "The SM Store - SM Mall of Asia",
        "category": "Department Store",
        "location": "Main Mall, Ground Level – Center Atrium"
    },
    "miniso": {
        "name": "Miniso - SM Mall of Asia",
        "category": "Lifestyle / Variety Store",
        "location": "Main Mall, Level 1 – North Wing"
    },
    "watsons": {
        "name": "Watsons - SM Mall of Asia",
        "category": "Health & Beauty",
        "location": "Main Mall, Level 1 – near The SM Store entrance"
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
    "muji": {
        "name": "MUJI - SM Mall of Asia",
        "category": "Lifestyle / Home & Apparel",
        "location": "South Wing, Level 3 – near Muji Café"
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
    "shake shack": {
        "name": "Shake Shack - SM Mall of Asia",
        "category": "Casual Dining / Burgers",
        "location": "Ground Floor, North Wing – near Main Mall Atrium"
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

@app.route('/', methods=['GET'])
def home():
    """Welcome endpoint"""
    return jsonify({
        "message": "Welcome to SM Mall of Asia Shop Finder API!",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This welcome message",
            "GET /api/shops": "Get all shops",
            "POST /api/search": "Search for a shop (Recommended for chatbots - POST with JSON: {\"name\": \"shop_name\"})",
            "GET /api/shops/search?name=<shop_name>": "Search for a shop by name (GET)",
            "POST /api/shops/search": "Search for a shop by name (POST with JSON body: {\"name\": \"shop_name\"})",
            "GET /api/shops/category/<category>": "Get shops by category"
        },
        "total_shops": len(shops)
    }), 200

@app.route('/api/shops', methods=['GET'])
def get_all_shops():
    """Get all shops"""
    return jsonify({
        "total": len(shops),
        "shops": shops
    }), 200

def search_shop_by_name(shop_name):
    """Core search logic - used by multiple endpoints"""
    if not shop_name:
        return jsonify({
            "error": "Please provide a shop name",
            "formatted_response": "❌ Please provide a shop name to search."
        }), 400
    
    shop_name = shop_name.lower().strip()
    
    # Direct match
    if shop_name in shops:
        shop = shops[shop_name]
        formatted_response = f"🛍️ {shop['name']}\n📍 Location: {shop['location']}\n🏷️ Category: {shop['category']}"
        return jsonify({
            "found": True,
            "shop": shop,
            "formatted_response": formatted_response
        }), 200
    
    # Partial match - search in shop names
    matches = []
    for key, shop_data in shops.items():
        if shop_name in key or shop_name in shop_data["name"].lower():
            matches.append({
                "key": key,
                **shop_data
            })
    
    if matches:
        if len(matches) == 1:
            shop = matches[0]
            formatted_response = f"🛍️ {shop['name']}\n📍 Location: {shop['location']}\n🏷️ Category: {shop['category']}"
            return jsonify({
                "found": True,
                "shop": shop,
                "formatted_response": formatted_response
            }), 200
        else:
            shops_list = "\n".join([f"• {s['name']}" for s in matches])
            formatted_response = f"🔍 Found {len(matches)} matching shops:\n{shops_list}\n\nPlease be more specific!"
            return jsonify({
                "found": True,
                "multiple_matches": True,
                "count": len(matches),
                "shops": matches,
                "formatted_response": formatted_response
            }), 200
    
    formatted_response = f"❌ No shop found matching '{shop_name}'\n\n💡 Try: uniqlo, h&m, muji, shake shack, etc."
    return jsonify({
        "found": False,
        "message": f"No shop found matching '{shop_name}'",
        "suggestion": "Try searching for: uniqlo, h&m, muji, shake shack, etc.",
        "formatted_response": formatted_response
    }), 404

@app.route('/api/search', methods=['GET', 'POST'])
def proxy_search():
    """Unified search endpoint for chatbot/Tookooks - accepts both GET and POST"""
    shop_name = ''
    
    if request.method == 'POST':
        data = request.get_json() or {}
        # Try multiple possible field names that chatbot platforms use
        shop_name = (data.get('name') or 
                    data.get('shop_name') or 
                    data.get('query') or 
                    data.get('text') or 
                    data.get('message') or 
                    data.get('user_input') or '')
    else:
        # GET method - check query parameters
        shop_name = (request.args.get('name') or 
                    request.args.get('shop_name') or 
                    request.args.get('query') or 
                    request.args.get('text') or '')
    
    return search_shop_by_name(shop_name)

@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint that accepts ANY payload and extracts shop name"""
    data = request.get_json() or {}
    
    # Extract shop name from various possible structures
    shop_name = ''
    
    # Try common chatbot payload structures
    if isinstance(data, dict):
        # Try direct fields
        shop_name = (data.get('name') or 
                    data.get('shop_name') or 
                    data.get('query') or 
                    data.get('text') or 
                    data.get('message') or 
                    data.get('user_input') or 
                    data.get('user_message') or '')
        
        # Try nested structures (message.text, etc)
        if not shop_name and 'message' in data and isinstance(data['message'], dict):
            shop_name = data['message'].get('text', '')
    
    # If still no shop name, try to find it in the entire JSON
    if not shop_name:
        # Search through all values in the dict
        for value in data.values():
            if isinstance(value, str) and value:
                shop_name = value
                break
    
    return search_shop_by_name(shop_name)

@app.route('/api/shops/search', methods=['GET', 'POST'])
def search_shop():
    """Search for a shop by name - supports both GET and POST"""
    # Handle both POST (JSON body) and GET (query params)
    if request.method == 'POST':
        data = request.get_json() or {}
        shop_name = data.get('name', '')
    else:
        shop_name = request.args.get('name', '')
    
    return search_shop_by_name(shop_name)

@app.route('/api/shops/category/<category>', methods=['GET'])
def get_shops_by_category(category):
    """Get shops by category"""
    category = category.lower()
    matching_shops = []
    
    for key, shop_data in shops.items():
        if category in shop_data["category"].lower():
            matching_shops.append({
                "key": key,
                **shop_data
            })
    
    if matching_shops:
        return jsonify({
            "category": category,
            "count": len(matching_shops),
            "shops": matching_shops
        }), 200
    
    return jsonify({
        "error": f"No shops found in category '{category}'"
    }), 404

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = 5000
    
    # Open ngrok tunnel
    public_url = ngrok.connect(port)
    
    print("\n" + "="*60)
    print(f"🌐 PUBLIC URL: {public_url}")
    print(f"🏠 Local URL: http://localhost:{port}")
    print("\n📋 Available Endpoints:")
    print(f"   GET  {public_url}/")
    print(f"   GET  {public_url}/api/shops")
    print(f"   POST {public_url}/api/search")
    print(f"   GET  {public_url}/api/shops/search?name=uniqlo")
    print(f"   GET  {public_url}/api/shops/category/restaurant")
    print("="*60 + "\n")
    
    # Run Flask app (use_reloader=False to avoid ngrok reconnection)
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)


