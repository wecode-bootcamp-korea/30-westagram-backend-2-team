from django.urls import path

from users.views import MembersView

urlpatterns = [
    path("/register", MembersView.as_view()),
]
