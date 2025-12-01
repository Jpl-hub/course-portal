from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("category", models.CharField(max_length=100)),
                ("level", models.CharField(max_length=50)),
                ("duration_hours", models.PositiveIntegerField()),
                ("teacher", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("rating_avg", models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ("rating_count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "db_table": "course",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_name", models.CharField(max_length=100)),
                ("rating", models.PositiveSmallIntegerField()),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="courses.course"),
                ),
            ],
            options={
                "db_table": "review",
                "ordering": ["-created_at"],
            },
        ),
    ]
