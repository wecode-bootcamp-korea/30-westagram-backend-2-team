import json, re, jwt

from django.http  import JsonResponse
from django.views import View

from postings.models    import Posting
from westagram.settings import SECRET_KEY, ALGORITHM

class PostingView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            # 토큰을 디코딩해서 페이로드를 가져온다.
            payload = jwt.decode(data['token'], SECRET_KEY, ALGORITHM)
            
            Posting.objects.create(
                text      = data['text'],    
                image_url = data['image_url'],
                user_id   = payload['user_id']  
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        #토큰 값이 이상할 경우
        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        #토큰 키는 있지만 벨류값이 빈 스트링이거나 값이 아예 없는 경우
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        #토큰 키가 없을 경우
        except KeyError:
            return JsonResponse({'result':'KEY_ERROR'}, status = 400)
        #아직 모르겠는 오류
        except Exception:
            return JsonResponse({'result':'500_ERROR'}, status = 400)
        
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
