from django.db import models

class TransactionModel(models.Model):
	amount = models.FloatField()
	type = models.CharField(max_length=20)
	parent_id = models.FloatField(null=True)
	transaction_id = models.FloatField(null=True)