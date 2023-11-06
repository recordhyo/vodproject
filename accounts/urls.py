from django.urls import path
from .views import KakaoLoginCallback, GoogleLoginCallback, NaverLoginCallback


urlpatterns = [
    path('kakao/callback', KakaoLoginCallback.as_view(), name='kakao_login_callback'),
    path('google/callback', GoogleLoginCallback.as_view(), name='google_login_callback'),
    path('naver/callback', NaverLoginCallback.as_view(), name='naver_login_callback'),
]