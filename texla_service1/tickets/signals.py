from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Ticket
from notifications.models import Notification

@receiver(pre_save, sender=Ticket)
def track_assignment(sender, instance: Ticket, **kwargs):
    if not instance.pk:
        instance._was_assigned_to = None
    else:
        try:
            old = Ticket.objects.get(pk=instance.pk)
            instance._was_assigned_to = old.assigned_to_id
        except Ticket.DoesNotExist:
            instance._was_assigned_to = None

@receiver(post_save, sender=Ticket)
def notify_on_assignment(sender, instance: Ticket, created, **kwargs):
    # New or changed assignment
    if instance.assigned_to_id and instance.assigned_to_id != getattr(instance, "_was_assigned_to", None):
        Notification.objects.create(
            recipient=instance.assigned_to,
            type="TICKET_ASSIGNED",
            payload={
                "ticket_id": str(instance.id),
                "customer_name": instance.customer_name,
                "contact": instance.contact,
                "pincode": instance.pincode,
                "issue": instance.issue,
                "status": instance.status,
            },
        )
