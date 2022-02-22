from django.urls import path

from postings.views import PostingView

urlpatterns = [
    path("/upload", PostingView.as_view()),
]
