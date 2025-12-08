from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.course_list, name="course-list"),
    path("courses/<int:course_id>/", views.course_detail, name="course-detail"),
    path("stats/", views.stats_view, name="stats"),
    path("ai-summary", views.ai_summary, name="ai-summary"),
    path("students/<str:student_id>/reviews/", views.reviews_by_student, name="student-reviews"),
]
