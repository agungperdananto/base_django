from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from utils.models import GeneralManager


class UserGeneralManager(UserManager, GeneralManager):
    pass


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    phone = models.CharField(
        max_length=50,
        db_index=True,
        null=True)
    email = models.EmailField(
        null=True,
        default=None)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserGeneralManager()

    def __str__(self):
        return self.get_username() or f'User #{self.pk}'
