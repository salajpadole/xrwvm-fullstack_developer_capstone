from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
import json
import logging

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
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"status": "Logged out", "userName": username})

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
