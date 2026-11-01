from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("djangoapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dealer",
            name="lat",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
        migrations.AddField(
            model_name="dealer",
            name="long",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
        migrations.AddField(
            model_name="dealer",
            name="short_name",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
