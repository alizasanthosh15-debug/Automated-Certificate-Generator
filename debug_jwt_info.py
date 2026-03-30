import jwt
import sys
print('jwt module file:', getattr(jwt, '__file__', None))
print('has encode:', hasattr(jwt, 'encode'))
print('attrs sample:', [a for a in dir(jwt) if not a.startswith('__')][:60])
print('version attr:', getattr(jwt, '__version__', None))
