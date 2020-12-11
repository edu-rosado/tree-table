from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.TreeTableDetail.as_view()),
    path("", views.TreeTableList.as_view()),
]
