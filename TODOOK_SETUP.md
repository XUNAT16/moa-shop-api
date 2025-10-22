# Todook Setup Guide for MOA Shop API

## ✅ Your API is LIVE at:
`https://moa-shop-api-1.onrender.com`

## 🔧 Todook Configuration

### Option 1: GET Method (Recommended - Simpler)

**URL:**
```
https://moa-shop-api-1.onrender.com/search?shop={{user_input}}
```

**Method:** `GET`

**Headers:**
```
Content-Type: application/json
```

**No body needed for GET**

---

### Option 2: POST Method

**URL:**
```
https://moa-shop-api-1.onrender.com/search
```

**Method:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "shop": "{{user_input}}"
}
```

---

## 🧪 Test URLs (Click these in your browser):

1. **Search Uniqlo:** https://moa-shop-api-1.onrender.com/search?shop=uniqlo
2. **Search H&M:** https://moa-shop-api-1.onrender.com/search?shop=h&m
3. **Search Starbucks:** https://moa-shop-api-1.onrender.com/search?shop=starbucks
4. **Get Categories:** https://moa-shop-api-1.onrender.com/categories
5. **Get Popular:** https://moa-shop-api-1.onrender.com/popular

---

## 📋 Response Format

### Success Response (200):
```json
{
  "found": true,
  "shop": {
    "name": "Uniqlo",
    "location": "Main Mall, Ground Level – South Wing, near H&M and Crocs",
    "category": "Apparel / Fashion"
  },
  "message": "🛍️ *Uniqlo*\n\n📍 *Location:*\nMain Mall, Ground Level – South Wing, near H&M and Crocs\n\n🏷️ *Category:* Apparel / Fashion"
}
```

### Not Found Response (404):
```json
{
  "found": false,
  "message": "Sorry, I couldn't find 'xyz' in SM Mall of Asia. Try: uniqlo, h&m, muji, shake shack, starbucks"
}
```

---

## 🎯 Todook Response Mapping

Use these in your Todook response:

- **Display to user:** `{{response.message}}`
- **Check if found:** `{{response.found}}`
- **Shop name:** `{{response.shop.name}}`
- **Location:** `{{response.shop.location}}`
- **Category:** `{{response.shop.category}}`

---

## 🐛 Troubleshooting

### Not getting response in Todook?

1. **Check URL is correct** - Make sure there's no extra spaces
2. **Use GET method first** - It's simpler than POST
3. **Test URL in browser** - Click the test URLs above
4. **Check Todook logs** - Look for error messages
5. **Verify {{user_input}} works** - Test with hardcoded value first

### Test with hardcoded value:
```
https://moa-shop-api-1.onrender.com/search?shop=uniqlo
```
If this works in Todook, then replace `uniqlo` with `{{user_input}}`

---

## 📱 Example Todook Flow

1. **User Message:** "Where is Uniqlo?"
2. **Extract:** "uniqlo" → store in variable `shop_name`
3. **API Call:** GET `https://moa-shop-api-1.onrender.com/search?shop={{shop_name}}`
4. **Response:** Display `{{response.message}}`

---

## 🔑 Available Shops (for testing):

- uniqlo
- h&m
- muji
- shake shack
- starbucks
- watsons
- sm supermarket
- forever 21
- zara
- power mac center
- mcdonald's
- jollibee
- miniso
- national bookstore
- timezone
- the sm store
- beyond the box
- mary grace
- tim ho wan
- ramen nagi
- conti's
- imax
- moa arena
- smx

---

## 💡 Quick Start for Todook:

**Step 1:** Create new External API action
**Step 2:** Paste URL: `https://moa-shop-api-1.onrender.com/search?shop=uniqlo`
**Step 3:** Method: GET
**Step 4:** Test it - Should return shop info
**Step 5:** Replace `uniqlo` with your variable `{{user_input}}`
