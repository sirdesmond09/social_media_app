from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.signals import user_activated
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import ActivationOtp
from .signals import generate_otp, site_name
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission, Group
from drf_extra_fields.fields import Base64ImageField

from config import settings

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "country",
            "language",
            "role",
            "phone",
            "password",
            "is_active",
        ]


class UserDeleteSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=False
    )
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=300)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=700)


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def verify_otp(self, request):
        otp = self.validated_data["otp"]

        if ActivationOtp.objects.filter(code=otp).exists():
            try:
                otp = ActivationOtp.objects.get(code=otp)
            except Exception:
                ActivationOtp.objects.filter(code=otp).delete()
                raise serializers.ValidationError(
                    detail="Cannot verify otp. Please try later"
                )

            if otp.is_valid():
                if otp.user.is_active == False:
                    otp.user.is_active = True
                    otp.user.save()

                    # clear all otp for this user after verification
                    all_otps = ActivationOtp.objects.filter(user=otp.user)
                    all_otps.delete()
                    user_activated.send(User, user=otp.user, request=request)
                    return {"message": "Verification Complete"}
                else:
                    raise serializers.ValidationError(
                        detail="User with this otp has been verified before."
                    )

            else:
                raise serializers.ValidationError(detail="OTP expired")

        else:
            raise serializers.ValidationError(detail="Invalid OTP")


class NewOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_new_otp(self):
        try:
            user = User.objects.get(email=self.validated_data["email"], is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                detail="Please confirm that the email is correct and has not been verified"
            )

        code = generate_otp(6)
        expiry_date = timezone.now() + timezone.timedelta(minutes=10)

        ActivationOtp.objects.create(code=code, user=user, expiry_date=expiry_date)
        subject = f"NEW OTP FOR {site_name}"

        message = f"""Hi, {str(user.first_name).title()}.

    Complete your verification on {site_name} with the OTP below:

                    {code}        

    Expires in 5 minutes!

    Thank you,
    Voltrox HQ LLC                
    """
        msg_html = render_to_string(
            "email/new_otp.html",
            {
                "first_name": str(user.first_name).title(),
                "code": code,
                "MARKET_PLACE_URL": settings.Common.MARKETPLACE_URL,
            },
        )

        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list, html_message=msg_html)

        return {"message": "Please check your email for OTP."}


class ImageUploadSerializer(serializers.Serializer):
    image = Base64ImageField()
