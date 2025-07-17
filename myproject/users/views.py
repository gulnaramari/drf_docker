from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment, User, Subscription
from .permissions import IsUser, IsOwner, IsUserOwner
from .serializers import PaymentSerializer, UserBaseSerializer, UserSerializer, SubscriptionSerializer, \
    CustomUserSerializer
from .services import create_product, create_price, create_session
from edu_materials.models import Course


class UserCreateAPIView(generics.CreateAPIView):
    """Контроллер, позволяет любому пользователю зарегистрироваться."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Контроллер, позволяет редактировать пользователя"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated & IsUserOwner]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер, позволяет получать детализацию о пользователе"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Метод, позволяет получать детализацию полную для пользователя,
        и частичную не для этого пользователя"""
        if self.kwargs.get("pk") == self.request.user.pk:
            return UserSerializer
        return UserBaseSerializer


class UserListAPIView(generics.ListAPIView):
    """Контроллер, позволяет получать список пользователей"""

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """Контроллер, позволяет удалять пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsUser,)


class PaymentsListAPIView(generics.ListAPIView):
    """Контроллер для списка оплат."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type')
    ordering_fields = ("payment_date",)
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра информации об оплате."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания оплаты через платежный сервис Stripe"""

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Метод вносит изменение в сериализатор создания платежа"""

        payment = serializer.save(user=self.request.user)
        product_id = create_product(payment)
        price = create_price(payment, product_id)
        session_id, session_url = create_session(price)
        payment.session_id = session_id
        payment.payment_link = session_url
        payment.save()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения оплаты """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления оплаты """

    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated & IsOwner]


class SubscriptionView(APIView):
    """Контроллер для создания или удаления подписки пользователя на курс."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated | IsAuthenticated & IsOwner]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course"],
            properties={"course": openapi.Schema(type=openapi.TYPE_INTEGER)},
        )
    )
    def post(self, *args, **kwargs):
        """Метод для отправки запроса на создание или
        удаление подписки пользователя на курс."""

        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subscription_item = Subscription.objects.all().filter(user=user, course=course_item)

        if subscription_item.exists():
            subscription_item.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.create(owner=user, course=course_item)
            message = "Подписка добавлена."
        return Response({"message": message})
