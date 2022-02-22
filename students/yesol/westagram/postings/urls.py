from django.urls import path

from postings.views import PostingView

urlpatterns = [
    path("/post", PostingView.as_view()),
]
