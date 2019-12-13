"""
URL pattern configuration for the respective view functions
"""

from django.urls import path
from . import views

urlpatterns = [
    path('transaction/<int:tid>', views.transaction_request, name='transaction_request'), # pattern to view function which create and read transaction data
    path('types/<slug:ttype>', views.transaction_type, name='transaction_type'), # pattern to view function which reads the transactions of a specific type
    path('sum/<int:tsum>', views.transaction_sum, name='transaction_sum'), # pattern to a view function which calculates the sum amount of all the transitive transactions linked to requested transaction id
]
