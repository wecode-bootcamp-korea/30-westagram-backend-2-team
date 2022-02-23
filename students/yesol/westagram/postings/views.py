import json, jwt

from django.http  import JsonResponse
from django.views import View

from my_settings     import SECRET_KEY, ALGORITHM
from postings.models import Posting

class PostingView(View):
    def get(self, request):
        postings_list = Posting.objects.all()
        results       = []

        for post in postings_list:
            results.append({
                "user_id"   : post.member_id,
                "image_url" : post.image_url,
                "created_at": post.created_at
            })
            
        return JsonResponse({"results":results}, status=200)

    def post(self, request):
        try:
            data    = json.loads(request.body)
            payload = jwt.decode(data["token"], SECRET_KEY, ALGORITHM)

            Posting.objects.create(
                member_id = payload["user_id"],
                image_url = data["image_url"]
            )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"LACK_OF_INFORMATION"}, status=400)
        except jwt.DecodeError:
            return JsonResponse({"results":"INVALID_TOKEN"}, status=400)

