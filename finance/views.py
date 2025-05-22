from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
from .serializers import TransactionSerializer
from rest_framework import viewsets


# Веб-страница: список транзакций с балансом после каждой операции
def transaction_list(request):
    # Получаем все транзакции по порядку времени (от старых к новым)
    transactions = Transaction.objects.all().order_by("created_at")

    running_balance = 0
    transaction_data = []

    for t in transactions:
        if t.type == "income":
            running_balance += t.amount
        else:
            running_balance -= t.amount
        transaction_data.append(
            {
                "type": t.get_type_display(),
                "amount": t.amount,
                "description": t.description,
                "date": t.created_at,
                "balance_after": running_balance,
            }
        )

    total_income = (
        Transaction.objects.filter(type="income").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    total_expense = (
        Transaction.objects.filter(type="expense").aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    final_balance = total_income - total_expense

    return render(
        request,
        "finance/transaction_list.html",
        {
            "transactions": transaction_data[::-1],  # Показываем последние первыми
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": final_balance,
        },
    )


# Веб-страница: форма добавления транзакции
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(request, "finance/add_transaction.html", {"form": form})


# API: работа с транзакциями через REST API
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = TransactionSerializer
