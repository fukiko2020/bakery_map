from django.urls import path
from . import views


app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "bakery_detail/<int:pk>",
        views.BakeryDetailView.as_view(),
        name="bakery_detail",
    ),
    path(
        "create/review",
        views.CreateReviewView.as_view(),
        name="create_review",
    ),
    path(
        "create/bakery",
        views.CreateBakeryView.as_view(),
        name="create_bakery",
    ),
]
