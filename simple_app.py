from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import requests
import os

app = Flask(__name__)
CORS(app)

def self_ping():
    """
    Self-ping background task to keep Render Free app awake.
    
    Render Free tier apps spin down after 15 minutes of inactivity.
    This function runs in a background thread and sends an HTTP GET request
    to the app's own URL every 10 minutes, simulating periodic traffic
    to prevent the app from going to sleep.
    
    The URL is read from the RENDER_EXTERNAL_URL environment variable.
    If the variable is not set, the task will not run (for local development).
    """
    render_url = os.getenv('RENDER_EXTERNAL_URL')
    
    if not render_url:
        print("ℹ️  RENDER_EXTERNAL_URL not set - self-ping disabled (local mode)")
        return
    
    # Remove trailing slash if present
    render_url = render_url.rstrip('/')
    ping_url = f"{render_url}/"
    
    print(f"✅ Self-ping enabled: Will ping {ping_url} every 10 minutes")
    
    while True:
        try:
            time.sleep(600)  # Wait 10 minutes (600 seconds)
            response = requests.get(ping_url, timeout=30)
            print(f"🏓 Self-ping: {response.status_code} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"⚠️  Self-ping failed: {e}")
            # Continue anyway - don't crash the thread

# Start self-ping in background thread
ping_thread = threading.Thread(target=self_ping, daemon=True)
ping_thread.start()

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
        data = request.get_json(force=True, silent=True) or {}
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
            "received_data": request.get_json(force=True, silent=True) if request.method == 'POST' else dict(request.args),
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
        data = request.get_json(force=True, silent=True) or {}
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

@app.route('/popular', methods=['GET', 'POST'])
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
        data = request.get_json(force=True, silent=True) or {}
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
    data = request.get_json(force=True, silent=True) or {}
    
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

# Traffic & Parking Information Endpoint
@app.route('/traffic', methods=['GET', 'POST'])
def traffic_info():
    """Handle traffic and parking information queries"""
    # Force JSON parsing even if Content-Type header is missing
    data = request.get_json(force=True, silent=True) or {}
    query = data.get('query', '').lower().strip()
    category = data.get('category', '').lower().strip()
    
    # Helper function for parking rates
    def get_parking_rates():
        return {
            "found": True,
            "type": "parking_rates",
            "message": (
                "🅿️ *SM MOA Parking Rates:*\n\n"
                "🕐 *Hourly Rate:* ₱40 per hour\n"
                "📅 *Daily Max:* ₱200\n"
                "🌙 *Overnight:* ₱300\n"
                "⚠️ *Additional:* +₱50 if exiting after 6:01 AM\n\n"
                "💡 *Tips:*\n"
                "• Pay at exit lanes or parking payment booths\n"
                "• Cash and card accepted\n"
                "• Keep your parking ticket safe!\n"
                "• Use SM Car Park App to check availability"
            )
        }
    
    # Helper function for parking locations
    def get_parking_locations():
        return {
            "found": True,
            "type": "parking_locations",
            "message": (
                "🅿️ *SM MOA Parking Facilities:*\n\n"
                "1️⃣ *Main Mall* (~8,000 slots)\n"
                "   📍 North & South Parking Buildings\n"
                "   🌙 Overnight parking available\n\n"
                "2️⃣ *MOA Arena (MAAX)* (1,400 slots)\n"
                "   📍 Adjacent to the Arena\n"
                "   🎫 Event parking available\n\n"
                "3️⃣ *NU Mall of Asia (NUMA)* (720 slots)\n"
                "   📍 Near the Arena\n"
                "   🏢 Office & retail parking\n\n"
                "4️⃣ *IKEA MOA Square* (200 slots)\n"
                "   � Adjacent to IKEA store\n"
                "   🛒 Shopping parking\n\n"
                "5️⃣ *SMX Convention Center* (400 slots)\n"
                "   📍 Basement parking area\n"
                "   📊 Convention & event parking\n\n"
                "� *Use SM Car Park App* to find open slots!"
            )
        }
    
    # Helper function for public transport
    def get_public_transport():
        return {
            "found": True,
            "type": "public_transport",
            "message": (
                "🚇 *How to Get to SM MOA:*\n\n"
                "🚆 *MRT/LRT:*\n"
                "• Take MRT-3 or LRT-1 to *Taft Avenue Station*\n"
                "• Exit and take a jeepney or UV Express to MOA\n"
                "• Travel time: ~10-15 minutes\n\n"
                "🚌 *Bus Routes:*\n"
                "• EDSA Carousel (free): Monumento to MOA\n"
                "• Regular buses: Routes via EDSA-Taft\n\n"
                "🚕 *Taxi/Grab:*\n"
                "• Available 24/7\n"
                "• From Taft: ₱80-120\n\n"
                "🚶 *From Taft Station:*\n"
                "• Jeepney: ₱15-20\n"
                "• UV Express: ₱25-30"
            )
        }
    
    # Helper function for traffic tips
    def get_traffic_tips():
        return {
            "found": True,
            "type": "traffic_tips",
            "message": (
                "🚦 *SM MOA Traffic Conditions:*\n\n"
                "📊 *Traffic Severity:*\n"
                "• Manila ranks among world's most congested cities\n"
                "• Peak congestion often exceeds 60%\n\n"
                "⏰ *Worst Traffic Times:*\n"
                "• Weekends & holidays (all day)\n"
                "• During MOA Arena or SMX events\n"
                "• Rush hours: 7-9 AM, 5-8 PM\n\n"
                "🛣️ *Main Roads:*\n"
                "• *Macapagal Boulevard* (8-lane road)\n"
                "• *Jose W. Diokno Boulevard* (4.38 km)\n"
                "• Both run parallel to MOA complex\n\n"
                "✅ *Best Times to Visit:*\n"
                "• Weekdays: 10:00 AM - 4:00 PM\n"
                "• Early mornings before 10:00 AM\n\n"
                "📱 *Real-Time Traffic Apps:*\n"
                "• Waze (live updates & routing)\n"
                "• Google Maps (traffic conditions)\n"
                "• SM Car Park App (parking availability)"
            )
        }
    
    # Helper function for walking directions
    def get_walking_directions():
        return {
            "found": True,
            "type": "walking_directions",
            "message": (
                "🚶 *Walking to SM MOA:*\n\n"
                "📍 *From Nearby Areas:*\n\n"
                "🏨 *From Conrad/Sheraton Hotels:*\n"
                "• 5-10 minute walk along Seaside Boulevard\n"
                "• Air-conditioned skybridge available\n\n"
                "🏢 *From Bay Area/MOA Arena:*\n"
                "• 10-15 minute walk to Main Mall\n"
                "• Follow the baywalk path\n\n"
                "🚉 *From Nearby Bus Stops:*\n"
                "• EDSA Carousel stop: 5 min walk\n"
                "• Regular bus stops: 2-5 min walk\n\n"
                "💡 Tip: The mall is huge! Use mall directories to find shops."
            )
        }
    
    # Helper function for help/default message
    def get_help_message():
        return {
            "found": False,
            "type": "help",
            "message": (
                "🤔 I'm not sure about that.\n\n"
                "I can help you with:\n\n"
                "🅿️ *Parking*\n"
                "   • Rates & pricing\n"
                "   • Parking locations\n\n"
                "🚇 *Public Transport*\n"
                "   • MRT/LRT directions\n"
                "   • Bus routes\n\n"
                "🚦 *Traffic Info*\n"
                "   • Peak hours\n"
                "   • Best times to visit\n\n"
                "🚶 *Walking Directions*\n"
                "   • From nearby areas\n\n"
                "What would you like to know?"
            )
        }
    
    # Category-based routing (for menu selection in Todook)
    if category:
        if category == 'parking_rates':
            return jsonify(get_parking_rates()), 200
        elif category == 'parking_locations':
            return jsonify(get_parking_locations()), 200
        elif category == 'public_transport':
            return jsonify(get_public_transport()), 200
        elif category == 'traffic_tips' or category == 'peak_hours':
            return jsonify(get_traffic_tips()), 200
        elif category == 'walking_directions':
            return jsonify(get_walking_directions()), 200
        else:
            return jsonify(get_help_message()), 200
    
    # Query-based routing (for free-text questions)
    if query:
        # Parking-related queries
        if 'park' in query:
            if any(word in query for word in ['rate', 'price', 'cost', 'how much', 'fee', 'charge']):
                return jsonify(get_parking_rates()), 200
            elif any(word in query for word in ['where', 'location', 'find', 'area', 'building']):
                return jsonify(get_parking_locations()), 200
            else:
                # General parking query - show both
                rates = get_parking_rates()
                locations = get_parking_locations()
                return jsonify({
                    "found": True,
                    "type": "parking",
                    "message": rates["message"] + "\n\n" + locations["message"]
                }), 200
        
        # Public transport queries
        elif any(word in query for word in ['mrt', 'lrt', 'train', 'metro', 'subway', 'bus', 'transport', 'commute']):
            return jsonify(get_public_transport()), 200
        
        # Traffic/timing queries
        elif any(word in query for word in ['traffic', 'rush', 'peak', 'busy', 'crowded', 'when', 'time']):
            return jsonify(get_traffic_tips()), 200
        
        # Walking/directions queries
        elif any(word in query for word in ['walk', 'direction', 'how to get', 'how do i get', 'route']):
            if any(word in query for word in ['mrt', 'lrt', 'train', 'bus']):
                return jsonify(get_public_transport()), 200
            else:
                return jsonify(get_walking_directions()), 200
        
        # Related words - suggest correct topic
        elif any(word in query for word in ['car', 'vehicle', 'auto', 'drive']):
            rates = get_parking_rates()
            return jsonify({
                "found": True,
                "type": "parking",
                "message": "💡 Did you mean *parking*?\n\n" + rates["message"]
            }), 200
        
        # Default fallback
        else:
            return jsonify(get_help_message()), 200
    
    # No query or category provided - show help
    else:
        return jsonify(get_help_message()), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
