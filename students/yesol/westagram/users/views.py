import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import Member
from my_settings import SECRET_KEY, ALGORITHM

class MembersRegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data["email"]
            password = data["password"]
            
            if not re.search("[@]", email) or not re.search("[.]", email) :
                return JsonResponse({"results":"EMAIL_ERROR"}, status=400)
            
            if len(password)<8 or not re.search("[a-zA-Z0-9_]", password) or not re.search("[^a-zA-Z0-9_]", password) :
                return JsonResponse({"results":"PASSWORD_ERROR"}, status=400)
            
            if Member.objects.filter(email=email).exists() :
                return JsonResponse({"results":"ALREADY_EXISTS"}, status=400)

            Member.objects.create(
                name         = data["name"],
                email        = email,
                password     = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                phone_number = data["phone_number"]
            )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)

class MembersLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            member = Member.objects.filter(email=data["email"])

            if not member.exists():
                return JsonResponse({"results":"EMAIL_ERROR"}, status=401)

            token  = jwt.encode({"user_id":member[0].id}, SECRET_KEY, ALGORITHM)

            if bcrypt.checkpw(data["password"].encode("utf-8"), member[0].password.encode("utf-8")):
                return JsonResponse({"token":token}, status=201)
            else:
                return JsonResponse({"results":"PASSWORD_ERROR"}, status=401)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)