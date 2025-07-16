from rest_framework import serializers
from .models import Payment, User, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели платежа"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели пользователя с вложенным сериализатором платежей,
    видим, какие платежи были у пользователя"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "town",
            "avatar",
            "payments",
        )


class UserBaseSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели пользователя с уменьшенным количеством полей"""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "town",
            "avatar",
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор пользователя с выводом информации об истории подписке."""

    payment_info = serializers.SerializerMethodField(read_only=True)
    subscriptions = serializers.SerializerMethodField(read_only=True)

    def get_payment_info(self, obj):
        """Метод для вывода информации об истории платежей пользователя."""

        list_info = [
            f'{p.created_at}-({p.amount}, способ оплаты: {p.payment_type}),'
            for p in Payment.objects.filter(owner=obj).order_by("created_at")
        ]
        pay_info = ', '.join( list_info)
        return pay_info


    def get_subscriptions(self, obj):
        """Метод для вывода информации об обновлениях подписки """

        list_update = [
            f'{s.course}-(pk={s.course.pk}{bool(s.created_at < s.course.updated_at) * "Курс обновлен!"}),'
            for s in Subscription.objects.filter(owner=obj).order_by("created_at")
        ]
        subscriptions_updated = ', '.join(list_update)
        return subscriptions_updated

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Пользователь"."""

        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Класс сериализатора подписки."""

    class Meta:
        """Класс для изменения поведения полей сериализатора модели подписки."""

        model = Subscription
        fields = "__all__"
