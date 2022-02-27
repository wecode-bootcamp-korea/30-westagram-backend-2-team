import jwt, json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist          

from my_settings import SECRET_KEY, ALGORITHM                      
from users.models import Member    

def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs):
        try : 
            token        = request.headers.get("Authorization", None)
            payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
            request.user = Member.objects.get(id=payload['user_id'])

            return func(self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:                                     
            return JsonResponse({"message" : "INVALID_TOKEN" }, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
    return wrapper
