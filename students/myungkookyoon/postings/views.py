import json

from django.http       import JsonResponse
from django.views      import View

from postings.models   import Post, Image
from users.models      import User
from core.utils        import login_decorator


class PostingView(View) :
    @login_decorator
    def post(self, request) :
        try :
            data     = json.loads(request.body)
            user     = request.user
            content    = data['content']
            image_list = data['image'].split(',')
            post = Post.objects.create(
                content = content,
                user = user
            )

            for image in image_list :
                Image.objects.create(
                    url = image,
                    post = post
                )
        
            return JsonResponse({'MASSAGE':'SUCCESS'}, status=200)

        except KeyError :
            return JsonResponse({'MASSAGE':'KEY_ERROR'}, status=400)
    
    @login_decorator
    def get(self, request) : 
        post_list = [{
            'user'       : User.objects.get(id=post.user.id).id,
            'content'    : post.content,
            'images'     : [image.url for image in post.images.all()],
            'created_at' : post.created_at
        } for post in Post.objects.all()
        ]

        return JsonResponse({'DATA' : post_list}, status=200)