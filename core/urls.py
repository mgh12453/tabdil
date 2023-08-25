from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
import core.views as views

urlpatterns = [
    path('add-balance/', staff_member_required(views.AddBalanceView.as_view())),
    path('charge-phone-number/', views.ChargePhoneNumberView.as_view()),
]