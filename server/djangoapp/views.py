import json
import re
import logging
from datetime import date

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError

from .models import Dealer, Review, CarMake, CarModel

logger = logging.getLogger(__name__)


def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"status": "Invalid JSON"}, status=400)
    username = payload.get("userName") or payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return JsonResponse({"status": "Username and password are required"}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"status": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out", "userName": ""})


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"status": "Invalid JSON"}, status=400)
    username = (payload.get("userName") or payload.get("username") or "").strip()
    first_name = (payload.get("firstName") or payload.get("first_name") or "").strip()
    last_name = (payload.get("lastName") or payload.get("last_name") or "").strip()
    email = (payload.get("email") or "").strip()
    password = payload.get("password") or ""
    if not all([username, first_name, last_name, email, password]):
        return JsonResponse({"status": "All fields are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": "Username already exists"}, status=409)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"status": "Email already registered"}, status=409)
    try:
        validate_password(password)
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
    except ValidationError as exc:
        return JsonResponse({"status": "Invalid password", "errors": list(exc.messages)}, status=400)
    except IntegrityError:
        return JsonResponse({"status": "Could not create user"}, status=400)
    return JsonResponse({"status": "Registered", "userName": user.username}, status=201)


def _dealer_dict(dealer):
    return {
        "id": dealer.id,
        "full_name": dealer.full_name,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.lat,
        "long": dealer.long,
        "short_name": dealer.short_name,
    }


@require_http_methods(["GET"])
def get_dealers(request, state=None):
    state = state or request.GET.get("state")
    dealers = Dealer.objects.all().order_by("id")
    if state:
        dealers = dealers.filter(state__iexact=state.strip())
    return JsonResponse({"status": 200, "dealers": [_dealer_dict(d) for d in dealers]})


@require_http_methods(["GET"])
def get_dealer_by_id(request, dealer_id):
    try:
        dealer = Dealer.objects.get(pk=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)
    return JsonResponse({"status": 200, "dealer": [_dealer_dict(dealer)]})


@require_http_methods(["GET"])
def get_dealer_reviews(request, dealer_id):
    if not Dealer.objects.filter(pk=dealer_id).exists():
        return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)
    reviews = Review.objects.filter(dealership_id=dealer_id).order_by("-created_at")
    return JsonResponse({"status": 200, "reviews": [{
        "id": r.id,
        "name": r.name,
        "dealership": r.dealership_id,
        "review": r.review,
        "purchase": r.purchase,
        "purchase_date": r.purchase_date.isoformat() if r.purchase_date else "",
        "car_make": r.car_make,
        "car_model": r.car_model,
        "car_year": r.car_year,
        "sentiment": r.sentiment,
    } for r in reviews]})


def _sentiment(text):
    positive = {"good", "great", "excellent", "fantastic", "amazing", "wonderful",
                "friendly", "helpful", "best", "perfect", "satisfied", "awesome",
                "love", "professional", "fast", "clean"}
    negative = {"bad", "poor", "terrible", "awful", "worst", "rude", "slow",
                "horrible", "disappointed", "unhappy", "waste", "hate"}
    words = set(re.findall(r"[a-z]+", (text or "").lower()))
    p, n = len(words & positive), len(words & negative)
    return "positive" if p > n else "negative" if n > p else "neutral"


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 401, "message": "Authentication required"}, status=401)
    payload = _json_body(request)
    if payload is None:
        return JsonResponse({"status": 400, "message": "Invalid JSON"}, status=400)
    try:
        dealer = Dealer.objects.get(pk=payload.get("dealership"))
    except (Dealer.DoesNotExist, TypeError, ValueError):
        return JsonResponse({"status": 400, "message": "Invalid dealership"}, status=400)
    text = (payload.get("review") or "").strip()
    if not text:
        return JsonResponse({"status": 400, "message": "Review is required"}, status=400)
    purchase_date = payload.get("purchase_date") or None
    try:
        if purchase_date:
            date.fromisoformat(purchase_date)
        car_year = int(payload["car_year"]) if payload.get("car_year") else None
    except (ValueError, TypeError):
        return JsonResponse({"status": 400, "message": "Invalid purchase date or car year"}, status=400)
    review = Review.objects.create(
        dealership=dealer,
        name=(payload.get("name") or request.user.get_full_name() or request.user.username).strip(),
        review=text,
        purchase=bool(payload.get("purchase", False)),
        purchase_date=purchase_date,
        car_make=payload.get("car_make", ""),
        car_model=payload.get("car_model", ""),
        car_year=car_year,
        sentiment=_sentiment(text),
    )
    return JsonResponse({"status": 200, "message": "Review added successfully", "review_id": review.id})


@require_http_methods(["GET"])
def get_cars(request):
    models = CarModel.objects.select_related("make").order_by("make__name", "name", "year")
    return JsonResponse({"CarModels": [{
        "CarMake": car.make.name,
        "CarModel": car.name,
        "Year": car.year,
        "Type": car.type,
    } for car in models]})


@require_http_methods(["GET"])
def get_car_makes(request):
    makes = CarMake.objects.prefetch_related("models").order_by("name")
    return JsonResponse({"CarMakes": [{
        "CarMake": make.name,
        "CarModels": [{
            "CarModel": model.name,
            "Year": model.year,
            "Type": model.type,
        } for model in make.models.all().order_by("name", "year")]
    } for make in makes]})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def analyze_review(request, review_text=None):
    if review_text is not None:
        text = review_text
    elif request.method == "GET":
        text = request.GET.get("text", "")
    else:
        payload = _json_body(request) or {}
        text = payload.get("text", payload.get("review", ""))
    if not text:
        return JsonResponse({"status": 400, "message": "Review text is required"}, status=400)
    return JsonResponse({"status": 200, "text": text, "sentiment": _sentiment(text)})
