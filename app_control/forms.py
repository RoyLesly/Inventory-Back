from dataclasses import field
from pyexpat import model
from django import forms
from .models import InventoryItem


# class InventoryCreateForm(forms.ModelForm):
#     class Meta:
#         model = InventoryItem
#         fields = ['created_by', 'group', 'name', 'photo']


# class InventoryPurchaseForm(forms.ModelForm):
#     class Meta:
#         model = InventoryItem
#         fields = ['created_by', 'group', 'name', 'recieved_quantity', 'recieved_by']

# class InventorySaleForm(forms.ModelForm):
#     class Meta:
#         model = InventoryItem
#         fields = ['created_by', 'group', 'name', 'issue_quantity', 'issue_by']