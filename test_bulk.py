import requests, os, jwt

SECRET_KEY=os.getenv('SECRET_KEY','your-secret-key-change-in-production')
token=jwt.encode({'user_id':1,'role':'admin'}, SECRET_KEY, algorithm='HS256')

participants=[{'name':'Alice','email':'alice@example.com','event':'Test','category':'Student'},{'name':'Bob','email':'bob@example.com','event':'Test','category':'Speaker'}]
res=requests.post('http://127.0.0.1:5000/api/bulk/generate-bulk', json={'participants':participants,'template_id':None}, headers={'Authorization':f'Bearer {token}'})
print(res.status_code, res.text)
