import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            password    = data['password']
            EMAIL_RE    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_RE = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(EMAIL_RE, email):
                return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        
            if not re.match(PASSWORD_RE, password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status = 400)
            
            hashed_password         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
                
            User.objects.create(
                name         = data['name'],
                email        = email,
                phone_number = data['phone_number'],
                password     = decoded_hashed_password
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        
class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)
                    
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'message':'SUCCESS', 'token':token}, status = 200)
            
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
                
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        
        except ObjectDoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)