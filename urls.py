"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index2'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_auditor_reg_request_view', views.admin_auditor_reg_request_view, name='admin_auditor_reg_request_view'),
    path('admin_approve_reject_auditor', views.admin_approve_reject_auditor, name='admin_approve_reject_auditor'),



    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_auditor_details_view', views.admin_auditor_details_view, name='admin_auditor_details_view'),

    path('admin_file_store_add', views.admin_file_store_add, name='admin_file_store_add'),
    path('admin_file_store_view', views.admin_file_store_view, name='admin_file_store_view'),
    path('admin_file_store_delete', views.admin_file_store_delete, name='admin_file_store_delete'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_file_store_add', views.user_file_store_add, name='user_file_store_add'),
    path('user_file_store_view', views.user_file_store_view, name='user_file_store_view'),
    path('user_file_store_delete', views.user_file_store_delete, name='user_file_store_delete'),
    path('user_file_store_download', views.user_file_store_download, name='user_file_store_download'),

    path('user_auditor_details_view', views.user_auditor_details_view, name='user_auditor_details_view'),

    path('user_file_share_update', views.user_file_share_update, name='user_file_share_update'),
    path('user_file_share_view', views.user_file_share_view, name='user_file_share_view'),

    path('auditor_login', views.auditor_login_check, name='auditor_login'),
    path('auditor_home', views.auditor_home, name='auditor_home'),
    path('auditor_details_add', views.auditor_details_add, name='auditor_details_add'),
    path('auditor_logout', views.auditor_logout, name='auditor_logout'),
    path('auditor_changepassword', views.auditor_changepassword, name='auditor_changepassword'),

    path('auditor_user_details_view', views.auditor_user_details_view, name='auditor_user_details_view'),
    path('auditor_user_file_store_view', views.auditor_user_file_store_view, name='auditor_user_file_store_view'),

    path('auditor_file_share_add', views.auditor_file_share_add, name='auditor_file_share_add'),
    path('auditor_file_share_view', views.auditor_file_share_view, name='auditor_file_share_view'),
    path('auditor_file_share_update', views.auditor_file_share_update, name='auditor_file_share_update'),

    path('auditor_file_store_update', views.auditor_file_store_update, name='auditor_file_store_update'),
    path('auditor_file_store_compare', views.auditor_file_store_compare, name='auditor_file_store_compare'),
    path('auditor_file_store_download', views.auditor_file_store_download, name='auditor_file_store_download'),

    path('user_audit_request_add', views.user_audit_request_add, name='user_audit_request_add'),
    path('auditor_audit_request_view', views.auditor_audit_request_view, name='auditor_audit_request_view'),

    path('user_send_file', views.user_send_file, name='user_send_file'),
    path('user_org_file_view', views.user_org_file_view, name='user_org_file_view'),
    path('user_org_file_delete', views.user_org_file_delete, name='user_org_file_delete'),

    path('auditor_user_org_file_view', views.auditor_user_org_file_view, name='auditor_user_org_file_view'),



]
