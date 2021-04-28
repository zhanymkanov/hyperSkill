from django.contrib.auth.base_user import BaseUserManager

from .constants import ErrorMessage


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True

        return self.create_user(email, password, **extra_fields)
