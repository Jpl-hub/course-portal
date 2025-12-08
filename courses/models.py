from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    duration_hours = models.PositiveIntegerField()
    teacher = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "course"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, related_name="reviews", on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, db_index=True)
    student_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student_name} - {self.course.title}"
