import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User
            
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
                return JsonResponse({'Message' : 'Invalid Email'}, status = 400)
            
            if not re.match(PASSWORD_VALIDATION, password):
                return JsonResponse({'Message' : 'Invalid Password'}, status = 400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'Message' : 'Email Already Exist'}, status = 400)
            
            User.objects.create(
                username     = username,
                email        = email,
                password     = password,
                phone_number = phone_number
            )         
                                   
            return JsonResponse({'messasge':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'massage':'KEY_ERROR'}, status=400)