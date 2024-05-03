from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name='starting-page'),
    path("questions/", views.AllQuestionsView.as_view(), name='questions-page'),
    path("questions/<slug:slug>", views.ReviewDetailView.as_view(), name='question-detail-page'),
    path('read-later', views.ReadLaterView.as_view(), name='read-later-page'),
]
