import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from westagram.settings import SECRET_KEY, ALGORITHM
            
class SignupView(View):
    def post(self, request):
        try :
            data           = json.loads(request.body)
            username       = data['username']
            email          = data['email']
            password       = data['password']
            phone_number   = data['phone_number']

            EMAIL_VALIDATION    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_VALIDATION = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(EMAIL_VALIDATION, email):
                return JsonResponse({'message':'Invalid Email'}, status=400)
            
            if not re.match(PASSWORD_VALIDATION, password):
                return JsonResponse({'message':'Invalid Password'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'Email Already Exist'}, status=400)
            
            hashed_pw         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')
            
            User.objects.create(
                username     = username,
                email        = email,
                password     = decoded_hashed_pw,
                phone_number = phone_number
            )         
                                   
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try :
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            
            user = User.objects.get(email=email)
                
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            access_token = jwt.encode({'id':user.id}, SECRET_KEY, ALGORITHM)
                    
            return JsonResponse({'access_token':access_token}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        