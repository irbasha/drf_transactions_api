from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TransactionModel, TransactionSumModel
from .serializers import TransactionSerializer, TransactionSumSerializer
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
				addsum(tid, body['amount'])
				return JsonResponse({"Status": "Ok"}) # return success on creating a new entry
			return JsonResponse(serializer.errors, status=400) # errors in case of failures
		return JsonResponse({"Error": "Transaction already Exists"}, safe=False) # return error if entry already exists


@csrf_exempt
def transaction_type(request, ttype):
	"""
	transaction_type()
	view function to read all the transactions of a specific type and return in response
	"""
	try:
		transaction = TransactionModel.objects.filter(type__contains=ttype).values('transaction_id') # select only transaction_ids of all the transactions of specific_type
	except TransactionModel.DoesNotExist:
		return JsonResponse({"Error": "Transaction DoesNotExist for its Type"}, safe=False)

	if request.method == 'GET': # Validating the request
		idlist = []
		for eachtransaction in transaction:
			tid = eachtransaction['transaction_id']
			idlist.append(tid) # adding transaction_id of every transaction to the list
		return JsonResponse(idlist, safe=False)

@csrf_exempt
def transaction_sum(request, tsum):
	try:
		sumtransaction = TransactionSumModel.objects.get(transaction_id=tsum).values('sumamount')
	except TransactionSumModel.DoesNotExist:
		return HttpResponse(status=404)
	sumamount = sumtransaction['sumamount']
	return JsonResponse({"sum": sumamount}, safe=False)


def addsum(tid, tsum):
	"""
	addsum()
	function is called during the insertion of a new transaction entry into database
	updates sum value of every parent node if there is a paren child relation
	"""
	transaction = TransactionModel.objects.get(transaction_id=tid)

	# if 'parent_id' in transaction and transaction['parent_id'] is not None: 
	# 	parent_id = transaction['parent_id']
	# 	parent_transaction = TransactionModel.objects.get(parent_id=parent_id)
	# 	parent_transaction['amount'] += tsum
	# 	serializer = TransactionSerializer(data=parent_transaction)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 	return addsum(parent_id, tsum)