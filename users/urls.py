from django.urls import path
from .views import userSignup, simple_view

urlpatterns = [
    # users/signup 요청이 오면 userSignup 함수가 처리
    path("signup", userSignup),
    path('', simple_view)
]