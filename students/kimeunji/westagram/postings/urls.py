from django.urls import path

from postings.views import CommentView, PostingView

urlpatterns = [
    path('/posting', PostingView.as_view()),
    path('/comment', CommentView.as_view())
]