from django.urls import path
from .views import vodTestget
from .views import vodTestPOST

urlpatterns = [
    # vod/gettest 요청이 오면 vodTestget 함수가 처리
    path("gettest", vodTestget),
    path("posttest", vodTestPOST)
]