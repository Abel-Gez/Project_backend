from rest_framework import serializers
from .models import AccountApplication, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name"]

class AccountApplicationSerializer(serializers.ModelSerializer):
    # return branch as nested object in responses
    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), source='branch', write_only=True
    )

    national_id_file = serializers.FileField(required=True)

    class Meta:
        model = AccountApplication
        fields = [
            "id",
            "full_name",
            "mother_name",
            "phone",
            "gender",
            "nationality",
            "fayda_number",
            "national_id_file",
            "monthly_income",
            "account_type",
            "branch",
            "branch_id",
            "status",
            "assigned_to",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "assigned_to", "created_at", "updated_at"]

    def validate_monthly_income(self, value):
        if value <= 0:
            raise serializers.ValidationError("monthly_income must be positive.")
        return value

    def validate_account_type(self, value):
        valid = [choice[0] for choice in AccountApplication.ACCOUNT_TYPES]
        if value not in valid:
            raise serializers.ValidationError("Invalid account type.")
        return value

    def create(self, validated_data):
        # branch provided via branch_id (source='branch')
        return super().create(validated_data)
