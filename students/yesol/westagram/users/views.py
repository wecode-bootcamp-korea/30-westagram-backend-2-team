import json, re

from django.http  import JsonResponse
from django.views import View

from users.models import Member

class MembersView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not re.search("[@]", data["email"]) or not re.search("[.]", data["email"]) :
                return JsonResponse({"results":"EMAIL_ERROR"}, status=400)
            
            if len(data["password"])<8 or not re.search("[a-zA-Z0-9_]", data["password"]) or not re.search("[^a-zA-Z0-9_]", data["password"]) :
                return JsonResponse({"results":"PASSWORD_ERROR"}, status=400)
            
            if Member.objects.filter(email=data["email"]).exists() :
                return JsonResponse({"results":"ALREADY_EXISTS"}, status=400)
            
            Member.objects.create(
                name         = data["name"],
                email        = data["email"],
                password     = data["password"],
                phone_number = data["phone_number"]
            )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)
