import json
import os
import urllib

from django.http import HttpResponseRedirect
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.conf import settings
from rest_framework.views import APIView
from accounts.models import User
from .serializer import UserSerializer
import requests

KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"
KAKAO_REDIRECT_URI = getattr(settings, 'KAKAO_REDIRECT_URI', 'KAKAO_REDIRECT_URI')
KAKAO_REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY', 'KAKAO_REST_API_KEY')
class KakaoLoginCallback(generics.GenericAPIView, mixins.ListModelMixin):
    def get(self, request, *args, **kwargs):
        #Callback URL 에서 code 받아오기
        code = request.GET["code"]
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # kakao에 access token 발급 요청
        data = {
          "grant_type": "authorization_code",
          "client_id": KAKAO_REST_API_KEY,
          "redirect_uri": KAKAO_REDIRECT_URI,
          "code": code,
        }
        # 받은 코드로 카카오에 access token 요청하기
        token = requests.post(KAKAO_TOKEN_API, data=data).json()
        access_token = token['access_token']
        if not access_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # kakao에 user info 요청
        headers = {"Authorization": f"Bearer ${access_token}"}
        # 받은 access token 으로 user 정보 요청
        user_infomation = requests.get(KAKAO_USER_API, headers=headers).json()

        data = {'access_token': access_token, 'code': code}
        kakao_account = user_infomation.get('kakao_account')
        #email 은 카카오 user 정보에서 받은 email
        email = kakao_account.get('email')


        # 1. 유저가 이미 DB에 있는지 확인하기
        try:
            #User모델의 이메일과 Token의 이메일이 같은지 확인
            user = User.objects.get(email=email)
            token = Token.objects.get_or_create(user=user)
            print(token)
            #같으면 이미 있는 유저 -> 바로 리다이렉트
            res = redirect("http://127.0.0.1:3000")
            #res.set_cookie(res, token.get('access'), token.get('refresh'))
            # 쿠키설정은 res.set_cookie('쿠키이름', '쿠키값')
            return res

        except User.DoesNotExist:
            # 2. 없으면 회원가입하기
            data = {
                'email': email,
                'password': 'test',
                'is_social': True
                # 비밀번호는 없지만 validation 을 통과하기 위해서 임시로 사용
                # 비밀번호를 입력해서 로그인하는 부분은 없으므로 안전함
                # is_social 값을 True 변경
            }
            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data
            serializer.create(validated_data=user)

            # 2-1. 회원가입 하고 토큰 만들어서 쿠키에 저장하기
            try:
                user = User.objects.get(email=email)
                token = Token.objects.create(user=user)
                print(token)
                res = redirect("http://127.0.0.1:3000")
                #res.set_cookie(res, token.get('access'), token.get('refresh'))

                return res
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


GOOGLE_TOKEN_API = "https://oauth2.googleapis.com/token"
GOOGLE_USER_API = "https://www.googleapis.com/userinfo/v2/me"
GOOGLE_REDIRECT_URI = getattr(settings, 'GOOGLE_REDIRECT_URI', 'GOOGLE_REDIRECT_URI')
GOOGLE_CLIENT_ID = getattr(settings, 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_PW = getattr(settings, 'GOOGLE_CLIENT_PW', 'GOOGLE_CLIENT_PW')

class GoogleLoginCallback(generics.GenericAPIView, mixins.ListModelMixin):
    def get(self, request, *args, **kwargs):
        #Callback URL 에서 code 받아오기
        code = request.GET["code"]
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # kakao에 access token 발급 요청
        data = {
            "grant_type": "authorization_code",
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret" : GOOGLE_CLIENT_PW,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "code": code,
        }
        # 받은 코드로 구글에 access token 요청하기
        token = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_CLIENT_PW}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_REDIRECT_URI}")
        token_json = token.json()
        print(token_json)
        access_token = token_json.get('access_token')

        # if not access_token:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        # google에 user info 요청
        headers = {"Authorization": f"Bearer ${access_token}"}
        # 받은 access token 으로 user 정보 요청
        user_infomation = requests.get(GOOGLE_USER_API, headers=headers).json()

        data = {'access_token': access_token, 'code': code}
        email = user_infomation.get('email')
        print(email)


        # 1. 유저가 이미 DB에 있는지 확인하기
        try:
            #User모델의 이메일과 Token의 이메일이 같은지 확인
            user = User.objects.get(email=email)
            token = Token.objects.get_or_create(user=user)
            print(token)
            #같으면 이미 있는 유저 -> 바로 리다이렉트
            res = redirect("http://127.0.0.1:3000")
            #res.set_cookie(res, token.get('access'), token.get('refresh'))
            # 쿠키설정은 res.set_cookie('쿠키이름', '쿠키값')
            return res

        except User.DoesNotExist:
            # 2. 없으면 회원가입하기
            data = {
                'email': email,
                'password': 'google',
                'is_social': True
                # 비밀번호는 없지만 validation 을 통과하기 위해서 임시로 사용
                # 비밀번호를 입력해서 로그인하는 부분은 없으므로 안전함
                # is_social 값을 True 변경
            }
            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data
            serializer.create(validated_data=user)

            # 2-1. 회원가입 하고 토큰 만들어서 쿠키에 저장하기
            try:
                user = User.objects.get(email=email)
                token = Token.objects.create(user=user)
                print(token)
                res = redirect("http://127.0.0.1:3000")
                #res.set_cookie(res, token.get('access'), token.get('refresh'))

                return res
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

NAVER_TOKEN_API = "https://nid.naver.com/oauth2.0/token"
NAVER_USER_API = "https://openapi.naver.com/v1/nid/me"
NAVER_REDIRECT_URI = getattr(settings, 'NAVER_REDIRECT_URI', 'NAVER_REDIRECT_URI')
NAVER_CLIENT_ID = getattr(settings, 'NAVER_CLIENT_ID', 'NAVER_CLIENT_ID')
NAVER_CLIENT_PW = getattr(settings, 'NAVER_CLIENT_PW', 'NAVER_CLIENT_PW')


class NaverLoginCallback(generics.GenericAPIView, mixins.ListModelMixin):
    def get(self, request, *args, **kwargs):
        #Callback URL 에서 code 받아오기
        code = request.GET["code"]
        # if not code:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        print(code)
        # Naver에 access token 발급 요청
        data = {
            "grant_type": "authorization_code",
            "client_id": NAVER_CLIENT_ID,
            "client_secret": NAVER_CLIENT_PW,
            "redirect_uri": NAVER_REDIRECT_URI,
            "code": code,
        }
        # 받은 코드로 네이버에 access token 요청하기
        token = requests.post(NAVER_TOKEN_API, data=data).json()
        access_token = token.get('access_token')
        print(access_token)
        # if not access_token:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        # 네이버에 user info 요청
        headers = "Bearer " + access_token
        # 받은 access token 으로 user 정보 요청
        request = urllib.request.Request(NAVER_USER_API)
        request.add_header("Authorization", headers)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            user_info = response_body.decode('utf-8')
            jsonResult = json.loads(user_info)
        else:
            print("Error Code:" + rescode)

        email = jsonResult.get('response').get('email')


        # 1. 유저가 이미 DB에 있는지 확인하기
        try:
            #User모델의 이메일과 Token의 이메일이 같은지 확인
            user = User.objects.get(email=email)
            token = Token.objects.get_or_create(user=user)
            #같으면 이미 있는 유저 -> 바로 리다이렉트
            res = redirect("http://127.0.0.1:3000")
            #res.set_cookie(res, token.get('access'), token.get('refresh'))
            # 쿠키설정은 res.set_cookie('쿠키이름', '쿠키값')
            return res

        except User.DoesNotExist:
            # 2. 없으면 회원가입하기
            data = {
                'email': email,
                'password': 'test',
                'is_social': True
                # 비밀번호는 없지만 validation 을 통과하기 위해서 임시로 사용
                # 비밀번호를 입력해서 로그인하는 부분은 없으므로 안전함
                # is_social 값을 True 변경
            }

            serializer = UserSerializer(data=data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data
            serializer.create(validated_data=user)

            # 2-1. 회원가입 하고 토큰 만들어서 쿠키에 저장하기
            try:
                user = User.objects.get(email=email)
                token = Token.objects.create(user=user)
                print(token)
                res = redirect("http://127.0.0.1:3000")
                #res.set_cookie(res, token.get('access'), token.get('refresh'))

                return res
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)



class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object() # getobject 로 가져온거.
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario 리액트 라우터가 실패할 경우.
        return HttpResponseRedirect('/') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs