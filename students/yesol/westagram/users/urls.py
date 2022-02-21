from django.urls import path

from users.views import MembersRegisterView, MembersLoginView

urlpatterns = [
    path("/register", MembersRegisterView.as_view()),
    path("/login", MembersLoginView.as_view()),
]
