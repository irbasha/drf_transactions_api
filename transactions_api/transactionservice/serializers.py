from rest_framework import serializers
from .models import TransactionModel

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TransactionModel
		fields = ['amount', 'type', 'parent_id', 'transaction_id']

