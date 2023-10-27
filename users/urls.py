from django.urls import path
from .views import userSignup

urlpatterns = [
    # example/hello 요청이 오면 helloAPI 함수가 처리
    path("signup", userSignup)
]