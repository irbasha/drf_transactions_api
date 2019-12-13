from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TransactionModel
from .serializers import TransactionSerializer
import json

@csrf_exempt
def transaction_request(request, tid):
	"""
	transaction_detail(...)
	- Accepts a positive integer parameter which is a transaction_id
	- Based on the type of request 'GET' or 'PUT' it performs below operations
		'GET'
			- reads the transaction data from database for a particular transactionid and returns it in json format.
			- if the transaction data is not found proper error message is deisplayed
		'PUT'
			- reads the body from the request and creates a new transaction entry in the database.
			- if the transaction with same id exists returns error
			- if the transaction id is same as the parent_id returns error
	"""
	if request.method == 'GET':
		trans = TransactionModel.objects.all()
		for eachtr in trans:
			print(eachtr.transaction_id)
		try:
			transaction = TransactionModel.objects.get(transaction_id=tid)
		except TransactionModel.DoesNotExist:
			return JsonResponse({"Status": 404, "Error": "Transaction DoesNotExist"})

		serializer = TransactionSerializer(transaction) # serializes the required data into json ype
		return JsonResponse(serializer.data)
	elif request.method == 'PUT':
		try:
			transaction = TransactionModel.objects.get(transaction_id=tid)
		except TransactionModel.DoesNotExist: # creates entry when try fails i.e, when there is no entry with the transaction_id
			body = json.loads(request.body)
			body['transaction_id'] = tid
			data = body
			if 'parent_id' in data and data['parent_id'] == tid: # checks for the match parent_it == transaction_id
				return JsonResponse({"Error": "parent_id is same as transaction id"}, safe=False)

			serializer = TransactionSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
				return JsonResponse({"Status": "Ok"}) # return success on creating a new entry
			return JsonResponse(serializer.errors, status=400) # errors in case of failures
		return JsonResponse({"Error": "Transaction already Exists"}, safe=False) # return error if entry already exists


@csrf_exempt
def transaction_type(request, ttype):
	return HttpResponse("transaction_type")

@csrf_exempt
def transaction_sum(request, tsum):
	return HttpResponse("transaction_sum")

