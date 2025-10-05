from decimal import Decimal, InvalidOperation
from rest_framework import serializers
from .models import ExchangeRate

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = [
            "id",
            "base_currency",
            "currency",
            "effective_date",
            "buying",
            "selling",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_currency(self, value):
        if not value or len(value) > 10:
            raise serializers.ValidationError("Invalid currency code.")
        return value.upper()

    def validate(self, data):
        # ensure buying and selling are positive and sensible
        buying = data.get("buying")
        selling = data.get("selling")
        if buying is None or selling is None:
            raise serializers.ValidationError("Both buying and selling must be provided.")

        try:
            # convert to Decimal to ensure serializer decimal constraints too
            b = Decimal(buying)
            s = Decimal(selling)
        except (InvalidOperation, TypeError):
            raise serializers.ValidationError("buying and selling must be numeric.")

        if b <= 0 or s <= 0:
            raise serializers.ValidationError("buying and selling must be positive numbers.")

        # optional: selling should be >= buying (common for buy/sell spreads)
        if s < b:
            raise serializers.ValidationError("selling should be greater than or equal to buying.")

        return data
