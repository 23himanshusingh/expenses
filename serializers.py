from rest_framework import serializers
from .models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()

class ExpenseSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    split_details = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'description', 'split_method', 'participants', 'created_at', 'split_details']
        read_only_fields = ['user', 'created_at']

    def get_split_details(self, obj):
        split_method = obj.split_method
        details = []

        if split_method == 'equal':
            split_amount = obj.amount / obj.participants.count()
            details = [{"user_id": participant.id, "amount": split_amount} for participant in obj.participants.all()]

        elif split_method == 'exact':
            for participant in obj.participants.all():
                participant_amount = float(self.initial_data.get(f'participant_exact_amount_{participant.id}', 0))
                details.append({"user_id": participant.id, "amount": participant_amount})

        elif split_method == 'percentage':
            for participant in obj.participants.all():
                participant_percentage = int(self.initial_data.get(f'participant_percentage_{participant.id}', 0))
                participant_amount = (participant_percentage / 100) * obj.amount
                details.append({"user_id": participant.id, "amount": participant_amount})

        return details

    def validate(self, data):
        split_method = data['split_method']
        participants = data['participants']
        total_amount = data['amount']
        
        # Validate for percentage split
        if split_method == 'percentage':
            total_percentage = sum([int(self.initial_data.get(f'participant_percentage_{p.id}', 0)) for p in participants])
            if total_percentage != 100:
                raise serializers.ValidationError('Total percentage must add up to 100%.')

        # Validate for exact split
        if split_method == 'exact':
            total_exact_amount = sum([float(self.initial_data.get(f'participant_exact_amount_{p.id}', 0)) for p in participants])
            if total_exact_amount != total_amount:
                raise serializers.ValidationError('Total of exact amounts must equal the total expense amount.')

        return data
