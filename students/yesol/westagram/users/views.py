import json, re

from django.http import JsonResponse
from django.views import View

from users.models import Member

class MembersView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email_list = []
            existing_email_list = Member.objects.all()
            
            for user_email in existing_email_list:
                email_list.append(user_email.email)

            if data["email"]=="" or data["password"]=="" :
                return JsonResponse({"results":"KEY_ERROR"}, status=400)
            elif re.search("[@]", data["email"])==None or re.search("[.]", data["email"])==None :
                return JsonResponse({"results":"EMAIL_ERROR"}, status=400)
            elif len(data["password"])<8 or re.search("[a-zA-Z0-9_]", data["password"])==None or re.search("[^a-zA-Z0-9_]", data["password"])==None:
                return JsonResponse({"results":"PASSWORD_ERROR"}, status=400)
            elif data["email"] in email_list :
                return JsonResponse({"results":"ALREADY_EXISTS"}, status=400)
            else:
                Member.objects.create(
                    name         = data["name"],
                    email        = data["email"],
                    password     = data["password"],
                    phone_number = data["phone_number"],
                    created_at   = data["created_at"],
                    updated_at   = data["updated_at"],
                )
            return JsonResponse({"results":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"results":"KEY_ERROR"}, status=400)


