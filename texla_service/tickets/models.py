from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        CLOSED = "CLOSED", "Closed"
        PENDING_PARTS = "PENDING_PARTS", "Pending Parts"

    customer_name = models.CharField(max_length=120)
    contact = models.CharField(max_length=20)
    pincode = models.CharField(max_length=10)
    issue = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_tickets")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
