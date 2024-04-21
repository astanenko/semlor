from django.urls import path
from .views import SemlorListView, SemlorDetailView

urlpatterns = [
    path("", SemlorListView.as_view(), name="semlor_list"),
    path(
        "semlor/<int:semlor_id>/",
        SemlorDetailView.as_view(),
        name="semlor_detail",
    ),
]
