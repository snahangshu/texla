from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Ticket
from .serializers import TicketSerializer
from accounts.permissions import IsAdmin, IsEngineer

User = get_user_model()

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "assign", "list_admin"]:
            return [IsAdmin()]
        if self.action in ["list", "retrieve", "partial_update", "update"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        # Engineers: see only your tickets
        if request.user.role == "ENGINEER":
            self.queryset = self.queryset.filter(assigned_to=request.user)
        return super().list(request, *args, **kwargs)

    @decorators.action(methods=["get"], detail=False, permission_classes=[IsAdmin], url_path="admin")
    def list_admin(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page else Response(ser.data)

    @decorators.action(methods=["post"], detail=True, permission_classes=[IsAdmin])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        engineer_id = request.data.get("engineer_id")
        if not engineer_id:
            return Response({"detail": "engineer_id is required"}, status=400)

        try:
            engineer = User.objects.get(id=engineer_id, role="ENGINEER")
        except User.DoesNotExist:
            return Response({"detail": "Engineer not found"}, status=404)

        ticket.assigned_to = engineer
        ticket.status = Ticket.Status.OPEN  # stays OPEN until engineer starts
        ticket.save()
        return Response(self.get_serializer(ticket).data, status=status.HTTP_200_OK)

    @decorators.action(methods=["patch"], detail=True, permission_classes=[IsEngineer], url_path="status")
    def update_status(self, request, pk=None):
        ticket = self.get_object()
        if ticket.assigned_to_id != request.user.id:
            return Response({"detail": "Not your ticket"}, status=403)

        new_status = request.data.get("status")
        if new_status not in dict(Ticket.Status.choices):
            return Response({"detail": "Invalid status"}, status=400)

        ticket.status = new_status
        ticket.save()
        return Response(self.get_serializer(ticket).data)
