import jwt

from django.http import JsonResponse

from westagram.settings import ALGORITHM, SECRET_KEY
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            #request의 header에 토큰이 있는지(사실상 얘는 필요없어 왜냐면 어차피 논으로 넘어가도 디코드 애러가 날테니까!)
            #그리고 있다면 유효한지 쳌쳌!
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['user_id'])
            request.user = user
        
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status = 401)
        
        except User.DoesNotExist:
            return JsonResponse({'result':'INVALID_USER'}, status = 400)
        
    return wrapper