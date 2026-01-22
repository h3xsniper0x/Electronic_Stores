from django.urls import path
from . import views

app_name = 'vulnerable_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('order/<int:order_id>/', views.insecure_order_view, name='insecure_order'),
    path('sqli/', views.sql_injection_view, name='sql_injection'),
    path('login/', views.weak_login, name='weak_login'),
    path('ssrf/', views.fetch_external_content, name='ssrf'),
    path('deserialize/', views.unsafe_deserialization, name='unsafe_deserialization'),
    path('crypto/', views.sensitive_data_view, name='sensitive_data'),
    path('design/', views.bypass_business_logic, name='bypass_design'),
    path('misconfig/', views.misconfiguration_view, name='misconfiguration'),
    path('outdated/', views.outdated_components_view, name='outdated'),
    path('logging/', views.silent_action_view, name='logging_failure'),
]
