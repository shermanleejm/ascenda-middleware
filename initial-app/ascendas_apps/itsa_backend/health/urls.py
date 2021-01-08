from django.urls import path
from . import views

urlpatterns = []

"""
USER URLS
"""
urlpatterns += [
    path('', views.health, name='health'),
    path('health/', views.health, name='health2'),
    # uncomment this for CI_CD demo
    path('ci_cd/', views.ci_cd_test, name='ci_cd'),
    path('sticky_sessions/', views.sticky_sessions, name='sticky_session'),
]