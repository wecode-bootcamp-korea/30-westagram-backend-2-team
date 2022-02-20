import json, re, bcrypt

from django.views import View
from django.http  import JsonResponse

from users.models import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            first_name   = data['first_name']
            last_name    = data['last_name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTED_EMAIL'}, status=400)
            
            email_regexp    = '^\w+([\.-]?\w+)*@\w+(\.\w{2,3})+$'
            password_regexp = '\S{8,20}'
            
            if not re.match(email_regexp, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)
            
            if not re.match(password_regexp, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=400)
            
            bytes_password  = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())
            save_password   = hashed_password.decode('utf-8')
            
            User.objects.create(
                first_name   = first_name,
                last_name    = last_name,
                email        = email,
                password     = save_password,
                phone_number = phone_number
                )
            
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : "INVALID_USER"}, status=401)
            
            if not User.objects.filter(password=password).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)