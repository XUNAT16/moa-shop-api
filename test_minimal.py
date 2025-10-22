from flask import Flask, jsonify, request
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)

shops = {
    "uniqlo": {
        "name": "Uniqlo - SM Mall of Asia",
        "category": "Apparel / Fashion",
        "location": "Main Mall, Ground Level – South Wing, near H&M and Crocs"
    }
}

@app.route('/api/search', methods=['GET', 'POST'])
def search():
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            shop_name = data.get('name', '').lower().strip()
        else:
            shop_name = request.args.get('name', '').lower().strip()
        
        if shop_name in shops:
            shop = shops[shop_name]
            formatted_response = f"🛍️ {shop['name']}\n📍 Location: {shop['location']}\n🏷️ Category: {shop['category']}"
            return jsonify({
                "found": True,
                "shop": shop,
                "formatted_response": formatted_response
            }), 200
        
        return jsonify({
            "found": False,
            "formatted_response": f"❌ No shop found matching '{shop_name}'"
        }), 404
    except Exception as e:
        print(f"ERROR in /api/search: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "formatted_response": "❌ Server error occurred"
        }), 500

if __name__ == '__main__':
    port = 5000
    public_url = ngrok.connect(port)
    
    print("\n" + "="*60)
    print(f"🌐 PUBLIC URL: {public_url}")
    print(f"📍 Test: POST {public_url}/api/search")
    print(f'📋 Body: {{"name": "uniqlo"}}')
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
