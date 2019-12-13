from rest_framework import serializers
from .models import TransactionModel, TransactionSumModel

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransactionModel
		fields = ['amount', 'type', 'parent_id', 'transaction_id']

class TransactionSumSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransactionSumModel
		fields = ['transaction_id', 'sumamount']

