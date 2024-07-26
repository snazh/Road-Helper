from jose import jwt

algo = "HS256"
secret = "5b4bb4e6fsddse7862a28986e67b7087f0a61385f28e32ce9284295a3ce2781afc97"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjQsImV4cCI6MTcyNDU4Mzk0Nn0.3wDcsN8fqZDlbRmyMwyAfB-GsHEE0cgPuY0dQfUL-4U"
payload = jwt.decode(token, secret, algorithms=[algo])

print(payload)
