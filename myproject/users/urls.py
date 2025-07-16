from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import (
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView, PaymentsListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView, PaymentUpdateAPIView,
    PaymentDestroyAPIView, SubscriptionView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="user_login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="user_token_refresh",
    ),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update", UserUpdateAPIView.as_view(), name="update_user"),
    path("users/<int:pk>/delete", UserDestroyAPIView.as_view(), name="delete_user"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment"),
    path("payment/pay/", PaymentCreateAPIView.as_view(), name="adding_payment"),
    path("payment/<int:pk>/adjust/", PaymentUpdateAPIView.as_view(), name="update_payment"),
    path("payment/<int:pk>/cancel/", PaymentDestroyAPIView.as_view(), name="delete_payment"),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
]
