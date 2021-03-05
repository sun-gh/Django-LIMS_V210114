from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils.html import strip_tags
from notifications.signals import notify
from .models import ApplyInvoice
from users.models import Person

# 实现站内消息发送功能


# @receiver(post_save, sender=ApplyInvoice)
def send_notification(sender, instance, created, **kwargs):

    # send_person = instance.person_apply
    recipient = Person.objects.filter(username='dell')

    notify.send(instance, verb="新的开票申请！", recipient=recipient)
    print("消息发送成功！")


post_save.connect(send_notification, sender=ApplyInvoice)
