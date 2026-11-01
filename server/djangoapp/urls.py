from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.registration, name="register"),

    path("get_dealers", views.get_dealers, name="get_dealers"),
    path("get_dealers/<str:state>", views.get_dealers, name="get_dealers_by_state"),
    path("dealer/<int:dealer_id>", views.get_dealer_by_id, name="dealer"),
    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="dealer_reviews"),
    path("add_review", views.add_review, name="add_review"),

    path("get_cars", views.get_cars, name="get_cars"),
    path("get_car_makes", views.get_car_makes, name="get_car_makes"),
    path("analyze_review", views.analyze_review, name="analyze_review"),
    path("analyze_review/<str:review_text>", views.analyze_review, name="analyze_review_text"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
