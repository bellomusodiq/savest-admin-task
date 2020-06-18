from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
# Create your models here.


class SendEmail(models.Model):
    title = models.CharField(max_length=400)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=SendEmail)
def send_email(sender, instance, created, *args, **kwargs):
    if created:
        title = instance.title
        for user in User.objects.filter(is_active=True):
            body = 'Dear {}, <br>'.format(user.username) + \
                   instance.content
            email = EmailMessage(
                title,
                body,
                'admin@savest.com.ng',
                [user.email]
            )
            email.send(fail_silently=True)



