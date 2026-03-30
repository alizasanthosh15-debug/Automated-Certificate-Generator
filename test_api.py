import requests, os, jwt
SECRET_KEY=os.getenv('SECRET_KEY','your-secret-key-change-in-production')
token=jwt.encode({'user_id':1,'role':'admin'},SECRET_KEY,algorithm='HS256')

for endpoint in ['http://127.0.0.1:5000/api/certificates/']:
    try:
        res=requests.get(endpoint, headers={'Authorization':f'Bearer {token}'})
        print(endpoint, res.status_code, res.json())
    except Exception as e:
        print('error', endpoint, e)
