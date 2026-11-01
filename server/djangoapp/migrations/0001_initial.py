# Generated for the capstone Django app.
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CarMake",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Dealer",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("zip", models.CharField(blank=True, max_length=20)),
                ("lat", models.CharField(blank=True, default="", max_length=30)),
                ("long", models.CharField(blank=True, default="", max_length=30)),
                ("short_name", models.CharField(blank=True, default="", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("type", models.CharField(choices=[("Sedan", "Sedan"), ("SUV", "SUV"), ("Wagon", "Wagon"), ("Coupe", "Coupe"), ("Hatchback", "Hatchback")], default="Sedan", max_length=20)),
                ("year", models.IntegerField(validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2026)])),
                ("make", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="models", to="djangoapp.carmake")),
            ],
            options={"unique_together": {("make", "name", "year")}},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("review", models.TextField()),
                ("purchase", models.BooleanField(default=False)),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("car_make", models.CharField(blank=True, max_length=100)),
                ("car_model", models.CharField(blank=True, max_length=100)),
                ("car_year", models.IntegerField(blank=True, null=True)),
                ("sentiment", models.CharField(default="neutral", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("dealership", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="djangoapp.dealer")),
            ],
        ),
    ]
