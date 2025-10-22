from pyngrok import conf

# Replace 'YOUR_AUTH_TOKEN_HERE' with your actual ngrok authtoken
authtoken = input("Enter your ngrok authtoken: ")
conf.get_default().auth_token = authtoken

print("✅ Ngrok authtoken configured!")
print("Now run: python app.py")
