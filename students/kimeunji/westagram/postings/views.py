import json, jwt
from django import views

from django.http  import JsonResponse
from django.views import View

from postings.models    import Posting, Comment
import users
from westagram.settings import SECRET_KEY, ALGORITHM
from users.utils        import login_decorator


class PostingView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            # 토큰을 디코딩해서 페이로드를 가져온다.
            # 토큰이 없으면 키애러 발생, token에 벨류가 없는 것은 안 해봄
            payload = jwt.decode(data['token'], SECRET_KEY, ALGORITHM)
            
            Posting.objects.create(
                text      = data['text'],    
                image_url = data['image_url'],
                user_id   = payload['user_id'] 
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)
        
        #토큰의 입력값이 틀렸을 때, 형식은 맞아서 디코드는 되는데 아마 페이로드가 다르게 나오는 듯??
        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        
        #토큰의 값이 없거나, 빈 문자열일 때
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        
        #요청에서 키가 없을 때
        except KeyError:
            return JsonResponse({'result':'KEY_ERROR'}, status = 400)
        
        #그 외 기타
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

class CommentView(views.View):
    @login_decorator
    #데코레이터를 쓰면 단지 토큰 검증 해주고, 리퀘스트에, 이 유저 데이터가 추가로 담겨있는 것일 뿐임.
    def post(self, request):
        try:
            data = json.loads(request.body)
            Comment.objects.create(
                user_id = request.user.id,
                posting_id = data['posting_id'],
                comment = data['comment']
            )
            return JsonResponse({'message':'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        
    @login_decorator
    def get(self, request):
        try:
            comments = Comment.objects.all()
            result = []
            for comment in comments:
                result.append(
                    {
                        'user'    : request.user.name,
                        #만약에 얘가 역참조라면 posting_id_set인건가?
                        #이건 필요없는 질문인게, 만약에 여기서 또 posting의 요소를 꺼내고 싶으면 
                        #posting의 객체를 가져오는 방법으로 해야하쟈나..?
                        #맞나....?
                        'posting' : comment.posting_id,
                        'comment' : comment.comment,
                        'created_at' : comment.created_at
                    }
                )
            return JsonResponse({'result':result}, status = 200)    
        
        except KeyError:
            return JsonResponse({'result':'KEY_ERROR'}, status = 400)