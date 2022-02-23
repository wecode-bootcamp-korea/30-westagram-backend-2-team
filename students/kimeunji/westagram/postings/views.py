import json, re, jwt

from django.http import JsonResponse
from django.views import View

from postings.models import Posting
from westagram.settings import SECRET_KEY, ALGORITHM

class PostingView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            # 토큰을 디코딩해서 페이로드를 가져온다.
            # 토큰이 없으면 키애러 발생
            payload = jwt.decode(data['token'], SECRET_KEY, ALGORITHM)
            
            Posting.objects.create(
                text      = data['text'],    
                image_url = data['image_url'],
                user_id   = payload['user_id']  
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
            
    def get(self, request):
        try:
            postings = Posting.objects.all()
            result = []
            for posting in postings:
                result.append(
                    {
                         'text'       : posting.text,
                         'image_url'  : posting.image_url,
                         'user'       : posting.user.name,
                         'created_at' : posting.created_at
                    }
                )
            return JsonResponse({'result':result}, status = 200) 
                  
        except KeyError:
            return JsonResponse({'result':'KEY_ERROR'}, status = 400)
