from django.test import TestCase
from django.contrib.auth import get_user_model


class AuthenticationTest(TestCase):

    def test_user_creation(self):
        User = get_user_model()

        user = User.objects.create_user(
            username="test_order_user",
            password="TestPass123!"
        )

        self.assertTrue(
            user.check_password("TestPass123!")
        )
