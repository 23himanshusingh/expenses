from django.urls import path
from .views import ExpenseViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

expense_list = ExpenseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

expense_detail = ExpenseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('expenses/', expense_list, name='expense-list'),
    path('expenses/<int:pk>/', expense_detail, name='expense-detail'),
]
