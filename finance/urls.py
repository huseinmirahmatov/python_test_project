from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),
    path("add/", views.add_transaction, name="add_transaction"),
    path("delete_all/", views.delete_all_transactions, name="delete_all_transactions"),
]
