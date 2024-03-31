from allauth.account.forms import SignupForm
from string import hexdigits
import random

from django.conf import settings
from django.core.mail import send_mail

from ads.models import Author


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        Author.objects.create(user=user)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, k=5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код потверждения',
            message=f'{user.username}, Ваш код активации: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user

