from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "contact", "pincode", "status", "assigned_to", "created_at")
    list_filter = ("status",)
    search_fields = ("customer_name", "contact", "issue")
