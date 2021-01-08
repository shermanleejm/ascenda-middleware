from django.urls import path
from . import views
from . import loyalty_partner_views
from . import fake_data_views

urlpatterns = []

"""
USER URLS
"""
urlpatterns += [
    path('users', views.user_list, name='user-list'),
    path('user/<int:pk>', views.user_detail, name='user-detail'),
]

"""
BANK URLS
"""
urlpatterns += [
    path('banks', views.bank_list, name='bank-list'),
    path('bank/<str:pk>', views.bank_detail, name='bank-detail'),
]

"""
LOYALTY PROGRAM URLS
"""

urlpatterns += [
    path('loyaltyprograms', views.loyaltyprogram_list, name='loyaltyprogram-list'),
    path('loyaltyprogram/<int:pk>', views.loyaltyprogram_detail, name='loyaltyprogram-detail'),
    path('loyaltyprogram/newbatchfile', loyalty_partner_views.loyalty_program_handback_file_submission, name='loyaltyprogram-new-batch-file'),
    path('loyaltyprogram/newaccrual', loyalty_partner_views.loyaltyprogram_new_accrual, name='loyaltyprogram-new-accrual'),
    path('loyaltyprogram/validatemembership', loyalty_partner_views.validate_membership_id, name='loyaltyprogram-validate-membership'),
    path('loyaltyprogram/generatebatchfile', loyalty_partner_views.generateBatchFile, name='loyaltyprogram-generate-batch-file'),
    # TODO: Remove the fake data
    path('loyaltyprogram/addfakedata', fake_data_views.addFakeData, name='loyaltyprogram-add-fake-data'),
    # path('loyaltyprogram/flush-db', fake_data_views.resetDbAndAddFakeData, name='loyaltyprogram-flush-data'),
    path('loyaltyprogram/testsherman', loyalty_partner_views.test_sherman, name='loyaltyprogram-test-sherman')
]

"""
TRANSACTION URLS
"""
urlpatterns += [
    path('transactions', views.transaction_list, name='transaction-list'),
    path('transactions/<str:date>', views.get_transaction_by_date, name='get-transaction-by-date'),
    path('transaction/<int:pk>', views.transaction_detail, name='transaction-detail'),
    path('transaction/user/<int:userid>', views.get_transaction_by_user, name="get-transaction-by-user"),
    path('transaction/status/<int:pk>', views.get_transaction_status, name="get-transaction-status")
]

"""
MEMBERSHIP URLS
"""
urlpatterns += [
    path('memberships', views.membership_list, name='membership-list'),
    path('membership/<int:pk>', views.membership_detail, name='membership-detail'),
    path('membership/<int:userId>/<int:loyaltyId>', views.get_membership_by_user_loyaltyprogram, name='membership-by-user-loyaltyprogram')
]