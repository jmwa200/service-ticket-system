from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)

    def __str__(self):
        return self.user.username

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    WORK_STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]
    APPROVAL_STATUS_CHOICES = [
        ("Pending Review", "Pending Review"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    scope_of_work = models.TextField()
    time_spent = models.DecimalField(max_digits=5, decimal_places=2)
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_charges = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default="Not Started")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default="Pending Review")
    completed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_approve", "Can approve tickets"),
            ("can_mark_completed", "Can mark work as completed"),
        ]

    def save(self, *args, **kwargs):
        # Auto-generate ticket ID (e.g., TKT-2023-001)
        if not self.ticket_id:
            year = timezone.now().strftime("%Y")
            last_ticket = Ticket.objects.filter(ticket_id__startswith=f"TKT-{year}-").order_by('ticket_id').last()
            last_num = int(last_ticket.ticket_id.split('-')[-1]) if last_ticket else 0
            self.ticket_id = f"TKT-{year}-{last_num + 1:03d}"
        
        # Auto-calculate total charges
        self.total_charges = self.time_spent * self.charge_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id
