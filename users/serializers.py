from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = ["id", "email", "phone", "town", "payment"]
        fields = "__all__"


class UserOtherSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "phone", "town"]
