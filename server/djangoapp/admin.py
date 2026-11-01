from django.contrib import admin
from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "type", "year")
    list_filter = ("make", "type", "year")
    search_fields = ("name", "make__name")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "city", "state", "zip")
    list_filter = ("state", "city")
    search_fields = ("full_name", "city", "state")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "dealership", "name", "sentiment", "created_at")
    list_filter = ("sentiment", "purchase", "created_at")
    search_fields = ("name", "review", "dealership__full_name")
    readonly_fields = ("created_at",)
