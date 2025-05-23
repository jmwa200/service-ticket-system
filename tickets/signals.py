from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Ticket

@receiver(post_save, sender=Ticket)
def notify_supervisor(sender, instance, **kwargs):
    if instance.approval_status == "Pending Review":
        supervisors = User.objects.filter(groups__name="Supervisors")
        emails = [u.email for u in supervisors]
        send_mail(
            f"Ticket {instance.ticket_id} Needs Approval",
            f"Technician {instance.technician.user.username} has completed work for {instance.client.name}.\nScope: {instance.scope_of_work}",
            "noreply@servicetracker.com",
            emails,
            fail_silently=True,
        )
