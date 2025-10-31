from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ticket

User = get_user_model()

class TicketSerializer(serializers.ModelSerializer):
    assigned_to_info = serializers.SerializerMethodField()
    created_by_info = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id", "customer_name", "contact", "pincode", "issue", "status",
            "assigned_to", "assigned_to_info", "created_by", "created_by_info",
            "created_at", "updated_at"
        ]
        read_only_fields = ["created_by", "created_at", "updated_at", "created_by_info", "assigned_to_info"]

    def get_assigned_to_info(self, obj):
        if obj.assigned_to:
            return {"id": obj.assigned_to.id, "username": obj.assigned_to.username, "full_name": obj.assigned_to.full_name}
        return None

    def get_created_by_info(self, obj):
        if obj.created_by:
            return {"id": obj.created_by.id, "username": obj.created_by.username, "full_name": obj.created_by.full_name}
        return None

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
