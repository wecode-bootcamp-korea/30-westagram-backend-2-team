import json, re, bcrypt as b

from django.http  import JsonResponse
from django.views import View

from users.models import Member

class MembersRegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data["email"]
            input_password = data["password"]
            
            if not re.search("[@]", email) or not re.search("[.]", email) :
                return JsonResponse({"results":"EMAIL_ERROR"}, status=400)
            
            if len(input_password)<8 or not re.search("[a-zA-Z0-9_]", input_password) or not re.search("[^a-zA-Z0-9_]", input_password) :
                return JsonResponse({"results":"PASSWORD_ERROR"}, status=400)
            
            if Member.objects.filter(email=email).exists() :
                return JsonResponse({"results":"ALREADY_EXISTS"}, status=400)

            hashed_password = b.hashpw(input_password.encode("utf-8"), b.gensalt()) 
            if b.checkpw(input_password.encode("utf-8"), hashed_password):
                Member.objects.create(
                    name         = data["name"],
                    email        = email,
                    password     = hashed_password,
                    phone_number = data["phone_number"]
                )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)

class MembersLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not Member.objects.filter(email=data["email"]).exists() or Member.objects.get(email=data["email"]).password != data["password"] :
                return JsonResponse({"results":"INVALID_USER"}, status=401)
                
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)