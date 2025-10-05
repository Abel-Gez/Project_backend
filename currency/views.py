from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from accounts.permissions import RolePermission

class ExchangeRateViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD for single rates (list, retrieve, create, update, destroy).
    Also provides a custom bulk-create endpoint at:
      POST /api/v1/exchange-rates/bulk-create/
    The bulk endpoint will replace existing rates for the same base_currency + effective_date
    (upsert strategy: delete existing rows for that date+base, then insert the provided list).
    """
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [RolePermission(required_roles=["MARKETING"])]  # default for restricted actions

    def get_permissions(self):
        """
        Allow anyone to view (list/retrieve), but keep other actions restricted to MARKETING.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()  # keeps your existing RolePermission for other actions

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        # ... all existing bulk_create code remains unchanged ...
        payload = request.data
        base_currency = payload.get('base_currency', 'ETB')
        effective_date = payload.get('effective_date')
        rates = payload.get('rates')

        if not effective_date:
            return Response({"detail": "effective_date is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(rates, list) or len(rates) == 0:
            return Response({"detail": "rates must be a non-empty list."}, status=status.HTTP_400_BAD_REQUEST)

        validated_items = []
        errors = {}
        for idx, item in enumerate(rates):
            data = {
                "base_currency": base_currency,
                "currency": item.get("currency"),
                "effective_date": effective_date,
                "buying": item.get("buying"),
                "selling": item.get("selling"),
            }
            ser = self.get_serializer(data=data)
            if not ser.is_valid():
                errors[idx] = ser.errors
            else:
                validated_items.append(ser.validated_data)

        if errors:
            return Response({"detail": "validation_error", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            ExchangeRate.objects.filter(base_currency__iexact=base_currency, effective_date=effective_date).delete()

            objs = []
            for item in validated_items:
                objs.append(ExchangeRate(
                    base_currency = item.get('base_currency').upper(),
                    currency = item.get('currency').upper(),
                    effective_date = item.get('effective_date'),
                    buying = Decimal(str(item.get('buying'))),
                    selling = Decimal(str(item.get('selling'))),
                ))
            ExchangeRate.objects.bulk_create(objs)

        created_qs = ExchangeRate.objects.filter(base_currency__iexact=base_currency, effective_date=effective_date)
        out = self.get_serializer(created_qs, many=True).data
        return Response(out, status=status.HTTP_201_CREATED)
