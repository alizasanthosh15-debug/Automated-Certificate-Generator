import urllib.request
import urllib.error
import json

url = "http://127.0.0.1:5000/api/auth/login"
data = {
    "email": "alizasanthosh15@gmail.com",
    "password": "wrongpassword",
    "role": "user"
}

headers = {
    "Content-Type": "application/json"
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method="POST")

print(f"Sending POST to {url} with data: {data}")

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Status Text: {response.reason}")
        print("Headers:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")
        print("\nBody:")
        print(response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print(f"HTTPError Status Code: {e.code}")
    print(f"HTTPError Reason: {e.reason}")
    print("Headers:")
    for k, v in e.headers.items():
        print(f"  {k}: {v}")
    print("\nBody:")
    print(e.read().decode('utf-8'))
except urllib.error.URLError as e:
    print(f"URLError: {e.reason}")
except Exception as e:
    print(f"Error: {e}")
