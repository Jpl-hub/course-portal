from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from django.db.models import Avg, Count

from .models import Course, Review
from .openai_client import OpenAIProxyClient


def serialize_course(course: Course) -> dict:
    
    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "level": course.level,
        "duration_hours": course.duration_hours,
        "teacher": course.teacher,
        "price": float(course.price),
        "rating_avg": float(course.rating_avg),
        "rating_count": course.rating_count,
    }


def serialize_review(review) -> dict:
    return {
        "student_id": review.student_id,
        "student_name": review.student_name,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.isoformat(),
    }


@require_GET
def course_list(request):
    courses = Course.objects.all()
    data = [serialize_course(c) for c in courses]
    return JsonResponse({"data_source": "mysql", "items": data}, json_dumps_params={"ensure_ascii": False})


@require_GET
def course_detail(request, course_id: int):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist as exc:
        raise Http404("Course not found") from exc

    reviews = [serialize_review(r) for r in course.reviews.all()]
    payload = serialize_course(course)
    payload["reviews"] = reviews
    return JsonResponse(payload, json_dumps_params={"ensure_ascii": False})


@require_GET
def stats_view(request):
    stats = Course.objects.aggregate(
        course_count=Count("id"),
        avg_price=Avg("price"),
        avg_rating=Avg("rating_avg"),
    )
   
    formatted = {
        "course_count": stats["course_count"] or 0,
        "avg_price": float(stats["avg_price"] or 0),
        "avg_rating": float(stats["avg_rating"] or 0),
    }
    return JsonResponse({"stats": formatted}, json_dumps_params={"ensure_ascii": False})


@require_GET
def ai_summary(request):
    topic = request.GET.get("topic", "Python 基础")
    client = OpenAIProxyClient()
    try:
        result = client.summarize_topic(topic)
        response = {
            "data_source": "openai-proxy",
            "payload": result,
        }
        return JsonResponse(response, json_dumps_params={"ensure_ascii": False})
    except Exception as exc:
        return JsonResponse(
            {
                "data_source": "openai-proxy",
                "error": str(exc),
            },
            status=502,
            json_dumps_params={"ensure_ascii": False},
        )


@require_GET
def reviews_by_student(request, student_id: str):
    reviews = Review.objects.filter(student_id=student_id).select_related("course")
    if not reviews.exists():
        raise Http404("No reviews for this student")

    items = [
        {
            "course_id": r.course.id,
            "course_title": r.course.title,
            "student_id": r.student_id,
            "student_name": r.student_name,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ]
    response = {"data_source": "mysql", "student_id": student_id, "reviews": items}
    return JsonResponse(response, json_dumps_params={"ensure_ascii": False})
