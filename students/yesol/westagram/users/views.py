import json, re, bcrypt, jwt

from django.core.exceptions import ObjectDoesNotExist
from django.http            import JsonResponse
from django.views           import View
from json                   import JSONDecodeError

from users.models import Member
from my_settings import SECRET_KEY, ALGORITHM

class MemberRegisterView(View):
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
        except JSONDecodeError:
            return JsonResponse({"results":"INVALID_DATA"}, status=400)

class MemberLoginView(View):
    def post(self, request):
        try:
            data   = json.loads(request.body)
            member = Member.objects.get(email=data["email"])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), member.password.encode("utf-8")):
                return JsonResponse({"results":"INVALID_USER"}, status=401)

            token = jwt.encode({"user_id":member.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"message":"SUCCESS", "token":token}, status=200)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"results":"INVALID_USER"}, status=401)
        except JSONDecodeError:
            return JsonResponse({"results":"INVALID_DATA"}, status=400)
 
