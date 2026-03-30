import requests, os, jwt

SECRET_KEY=os.getenv('SECRET_KEY','your-secret-key-change-in-production')
token=jwt.encode({'user_id':1,'role':'admin'}, SECRET_KEY, algorithm='HS256')

csv = 'name,email,event,category\nJohn,john@example.com,Test,Student\n'
files={'file':('test.csv',csv)}
res=requests.post('http://127.0.0.1:5000/api/bulk/preview', files=files, headers={'Authorization':f'Bearer {token}'})
print(res.status_code)
print(res.text)
