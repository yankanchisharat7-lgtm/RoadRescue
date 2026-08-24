from django.urls import path
from . import views


urlpatterns = [

    # Reviews page
    path(
        "",
        views.review_list,
        name="review_list"
    ),

    # Add review
    path(
        "add/<int:mechanic_id>/",
        views.add_review,
        name="add_review"
    ),

]
