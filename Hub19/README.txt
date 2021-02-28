If you run into CORS issues with web sockets:
In the __init__.py file, have this line:
socketio.init_app (app, async_mode='gevent', cors_allowed_origins="*")

If the number of socket clients connecting to the server automatically keeps increasing:
   An exception occurred, most probably within buttons.html. This crashes the socket connection but it automatically
   keeps trying to reestablish the connection.
   
If you encounter the error:
AttributeError: module 'jwt' has no attribute 'encode'    
https://stackoverflow.com/questions/33198428/jwt-module-object-has-no-attribute-encode
The problem arises if you have both JWT and PyJWT installed. When doing import jwt it is importing the library 
JWT as opposed to PyJWT - the latter is the one you want for encoding. 
I did 
pip uninstall JWT 
and then 
pip uninstall PyJWT 
then finally 
pip install PyJWT.
You can also specify a version:
pip install PyJWT=1.6.4

flask-jwt insists on a particular version of jwt, namely, PyJWT==1.4.2
So I needed to do: 
pip uninstall jwt
pip uninstall PyJWT 
pip uninstall flask-jwt
pip install flask-jwt
