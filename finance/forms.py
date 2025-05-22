from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    type = forms.CharField(label="Тип:")

    class Meta:
        model = Transaction
        fields = ["type", "amount", "description"]

    def clean_type(self):
        value = self.cleaned_data["type"].lower()
        if value not in ["income", "expense"]:
            raise forms.ValidationError("Введите только 'income' или 'expense'")
        return value
