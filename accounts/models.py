from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.forms import model_to_dict

from .managers import UserManager
import uuid
import random
from django.contrib.auth.models import Group as DjangoGroup


class User(AbstractBaseUser, PermissionsMixin):
    """
    Database schema for User model.

    Fields:
        - id (UUID): Unique identifier for the user.
        - first_name (str): First name of the user
        - last_name (str): Last name of the user
        - email (str): Email address of the user.
        - role (str): User type i.e admin, user.
        - image (img): profile picture of users
        - country (str): nationality of users
        - language (str): language of users
        - password (str): Password of the users
        - is_staff (bool): Field to mark an admin user as a super admin
        - is_admin (bool): Field to mark the  user as an admin
        - is_active (bool): Active status of the user
        - is_deleted (bool): Deleted status of the user
        - fcm_token (str): User's device firebase token for push notification
        - provider (str): Channel through which user signed up.
        - date_joined (datetime): Time at which the user signed up.
    """

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    id = models.UUIDField(
        primary_key=True, unique=True, editable=False, default=uuid.uuid4
    )
    first_name = models.CharField(_("first name"), max_length=250)
    last_name = models.CharField(_("last name"), max_length=250)
    role = models.CharField(_("role"), max_length=255, choices=ROLE_CHOICES)
    email = models.EmailField(_("email"), unique=True)
    image = models.ImageField(
        upload_to="profile_photos/",
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
        blank=True,
        null=True,
    )
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255, default="English")
    password = models.CharField(_("password"), max_length=300)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_admin = models.BooleanField(_("admin"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_deleted = models.BooleanField(_("deleted"), default=False)
    created_at = models.DateTimeField(_("date joined"), auto_now_add=True)
    provider = models.CharField(
        _("provider"),
        max_length=255,
        default="email",
        choices=(("email", "email"), ("google", "google")),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["id", "first_name", "last_name", "role", "country", "language"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.email} -- {self.role}"
    
    def get_full_name(self):
        """Returns the full name of the user"""
        
        return f"{self.first_name} {self.last_name}"

    @property
    def image_url(self):
        """See the image url of the user

        Returns:
            str: Image url of the  user or empty string if no image uploaded
        """

        if self.image:
            return self.image.url
        return ""

    def delete(self):
        """
        Performs soft delete on the user model
        Delete the user by flagging it as deleted and adding updating the email and phone with delete flags.
        """

        self.is_deleted = True
        self.email = f"{random.randint(0,100000)}-deleted-{self.email}"
        self.save()
        return

    def delete_permanently(self):
        """
        Performs hard delete on the user model.
        To be used with caution!
        """

        super().delete()

        return


class ActivationOtp(models.Model):
    """
    Database schema for Activation Otp model.

    Fields:
        - id (int): Unique identifier for the OTP.
        - code (str): OTP for the user
        - user (FK): User attached to the  otp
        - expiry_date (datetime): Time at which the OTP expires.
    """

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiry_date = models.DateTimeField()

    def is_valid(self):
        """Checks if the OTP has expires or not

        Returns:
            bool: Result of OTP check.
        """

        return bool(self.expiry_date > timezone.now())


