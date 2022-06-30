from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerators(PasswordResetTokenGenerator):
    # create hash token
    def _make_hash_value(self, user, timestamp):
        # create token based on the user
        return (
                text_type(user.pk) + text_type(timestamp) +
                text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerators()
