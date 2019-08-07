from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """Generator of token for email account validation."""

    def _make_hash_value(self, user, clean_timestamp):
        """
        Make the token.
        Arguments
            user {str} -- user primary key
            clean_timestamp {str} -- timestamp without period.
        Return:
            token {str} -- the token
        """
        return str(user) + str(clean_timestamp)


account_activation_token = TokenGenerator()