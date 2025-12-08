from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="student_id",
            field=models.CharField(db_index=True, default="S000", max_length=50),
            preserve_default=False,
        ),
    ]
