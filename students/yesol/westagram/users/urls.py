from django.urls import path

from users.views import MemberRegisterView, MemberLoginView

urlpatterns = [
    path("/register", MemberRegisterView.as_view()),
    path("/login", MemberLoginView.as_view()),
]
