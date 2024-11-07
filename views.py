from rest_framework import viewsets
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve_user_expenses(self, request, user_id=None):
        User = get_user_model()
        user = get_object_or_404(User, pk=user_id)
        expenses = Expense.objects.filter(participants=user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def retrieve_overall_expenses(self, request):
        total_expense = Expense.objects.all().aggregate(total=models.Sum('amount'))['total']
        return Response({'total_expense': total_expense})
