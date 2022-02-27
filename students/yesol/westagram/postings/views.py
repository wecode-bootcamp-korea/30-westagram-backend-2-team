import json, jwt
from re import L

from django.http  import JsonResponse
from django.views import View

from my_settings     import SECRET_KEY, ALGORITHM
from postings.models import Posting, Comment
from users.utils     import login_decorator

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

    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            Posting.objects.create(
                member_id = request.user.id,
                image_url = data["image_url"]
            )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEYERROR"}, status=400)
        except jwt.DecodeError:
            return JsonResponse({"results":"INVALID_TOKEN"}, status=400)

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            Comment.objects.create(
                content    = data["content"],
                posting_id = data["posting_id"],
                member_id  = request.user.id
            )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEYERROR"}, status=400)
        except jwt.DecodeError:
            return JsonResponse({"results":"INVALID_TOKEN"}, status=400)

    def get(self, request):
        try:
            posting_id    = 1
            comments_list = Comment.objects.filter(posting_id=posting_id)
            results       = []

            for comment in comments_list:
                results.append({
                    "posting_id" : comment.posting_id,
                    "content"    : comment.content,
                    "member_id"  : comment.member_id
                })
            return JsonResponse({"results":results}, status=200)
        except KeyError:
            return JsonResponse({"results":"KEYERROR"}, status=400)



