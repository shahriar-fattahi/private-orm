from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password, is_active=True, is_admin=False):
        if not username:
            raise ValueError("Username must be entered")
        if not password:
            raise ValueError("Password must be entered")

        user = self.model(
            username=username,
            is_active=is_active,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            is_active=True,
            is_admin=True,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user
