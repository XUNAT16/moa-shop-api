# Flask API

A simple RESTful API built with Flask.

## Features

- ✅ RESTful endpoints (GET, POST, PUT, DELETE)
- ✅ CORS enabled
- ✅ Error handling
- ✅ JSON responses
- ✅ Sample CRUD operations

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /
Welcome message with API information

### GET /api/items
Get all items

### GET /api/items/<id>
Get a specific item by ID

### POST /api/items
Create a new item
```json
{
  "name": "Item name",
  "description": "Item description"
}
```

### PUT /api/items/<id>
Update an existing item
```json
{
  "name": "Updated name",
  "description": "Updated description"
}
```

### DELETE /api/items/<id>
Delete an item

## Testing with cURL

```bash
# Get all items
curl http://localhost:5000/api/items

# Get specific item
curl http://localhost:5000/api/items/1

# Create new item
curl -X POST http://localhost:5000/api/items -H "Content-Type: application/json" -d "{\"name\":\"New Item\",\"description\":\"A new item\"}"

# Update item
curl -X PUT http://localhost:5000/api/items/1 -H "Content-Type: application/json" -d "{\"name\":\"Updated Item\"}"

# Delete item
curl -X DELETE http://localhost:5000/api/items/1
```

## Next Steps

- Add database integration (SQLAlchemy, MongoDB, etc.)
- Implement authentication (JWT, OAuth)
- Add input validation (Flask-WTF, Marshmallow)
- Add API documentation (Flask-Swagger, Flask-RESTX)
- Implement rate limiting
- Add unit tests
