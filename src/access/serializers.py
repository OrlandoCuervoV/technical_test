import re
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_password(self, password):
        if len(password) < 8 or len(password) > 16:
            msg = ('The password must be between 8 and 16 characters.')
            raise exceptions.ValidationError(msg)

        if re.findall('[()[\]{}|\\`~!@#^_\=;:\',<>.?]', password):
            msg = ("The password must only contain the following special characters: " +
                  "*/+-$%&")
            raise exceptions.ValidationError(msg)

    def _validate_email(self, email, password):
        user = None
        if email and password:
            self._validate_password(password)
            user = self.authenticate(email=email, password=password)
        else:
            msg = ('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = ('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = ('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        if not user.is_superuser:
            # If required, is the email verified?
            if 'rest_auth.registration' in settings.INSTALLED_APPS:
                from allauth.account import app_settings
                if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                    email_address = user.emailaddress_set.get(email=user.email)
                    if not email_address.verified:
                        raise serializers.ValidationError('E-mail is not verified.')

        attrs['user'] = user
        return attrs


