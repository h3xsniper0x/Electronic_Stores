

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import requests
import pickle
import base64
from orders.models import Order
from products.models import Product

def index(request):
    links = [
        ('/vulnerable/order/1/', 'A01: Broken Access Control (IDOR) - Try changing ID'),
        ('/vulnerable/crypto/', 'A02: Cryptographic Failures - Plain text sensitive data'),
        ('/vulnerable/sqli/?product_name=Phone', 'A03: Injection - SQL Injection (Try \')'),
        ('/vulnerable/design/', 'A04: Insecure Design - Logic Bypass'),
        ('/vulnerable/misconfig/', 'A05: Security Misconfiguration - Stack Trace'),
        ('/vulnerable/outdated/', 'A06: Vulnerable Components - Outdated Lib Demo'),
        ('/vulnerable/login/', 'A07: Identification Failures - Weak Login'),
        ('/vulnerable/deserialize/', 'A08: Integrity Failures - Insecure Deserialization'),
        ('/vulnerable/logging/', 'A09: Logging Failures - Silent Action'),
        ('/vulnerable/ssrf/', 'A10: SSRF - Fetch External URL'),
    ]
    
    html = "<h1>OWASP Top 10 Vulnerability Demos</h1><ul>"
    for url, desc in links:
        html += f"<li><a href='{url}'>{desc}</a></li>"
    html += "</ul>"
    return HttpResponse(html)

# A01:2021-Broken Access Control
# Vulnerability: IDOR - Allows accessing any order by ID without checking user ownership
def insecure_order_view(request, order_id):
    try:
        # VULNERABLE: No check if request.user == order.user
        order = Order.objects.get(id=order_id)
        return HttpResponse(f"<h3>Order Details (VULNERABLE)</h3><p>Order ID: {order.id}</p><p>User: {order.user.username}</p><p>Total: {order.total_price}</p>")
    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)

# A03:2021-Injection
# Vulnerability: SQL Injection via 'product_name' parameter
def sql_injection_view(request):
    product_name = request.GET.get('product_name', '')
    products = []
    if product_name:
        # VULNERABLE: Direct string interpolation into SQL query
        # Warning: This relies on the table name being 'products_product'
        query = f"SELECT * FROM products_product WHERE name = '{product_name}'"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                # Fetching rows manually
                columns = [col[0] for col in cursor.description]
                products = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except Exception as e:
            return HttpResponse(f"Database Error: {e}")
    
    return HttpResponse(f"<h3>SQL Injection Demo</h3><p>Querying for: {product_name}</p><p>Results: {products}</p>")

# A07:2021-Identification and Authentication Failures
# Vulnerability: Weak login without rate limiting
@csrf_exempt
def weak_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # VULNERABLE: No rate limiting implemented here
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Login successful")
        else:
            return HttpResponse("Login failed")
            
    form_html = """
    <h3>Weak Login Demo</h3>
    <form method="post">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    """
    return HttpResponse(form_html)

# A10:2021-Server-Side Request Forgery (SSRF)
# Vulnerability: Fetches arbitrary URLs provided by user
def fetch_external_content(request):
    url = request.GET.get('url')
    if url:
        # VULNERABLE: No validation of URL scheme (file://, http://localhost) or destination
        try:
            response = requests.get(url, timeout=5)
            return HttpResponse(f"<h3>SSRF Demo</h3><pre>{response.text[:500]}</pre>")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    
    return HttpResponse("<h3>SSRF Demo</h3><p>Provide a 'url' GET parameter to fetch content.</p>")

# A08:2021-Software and Data Integrity Failures
# Vulnerability: Insecure Deserialization (Pickle)
@csrf_exempt
def unsafe_deserialization(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:
            # VULNERABLE: Deserializing untrusted data
            try:
                # Expecting base64 encoded pickle data
                decoded_data = base64.b64decode(data)
                obj = pickle.loads(decoded_data)
                return HttpResponse(f"Deserialized object: {obj}")
            except Exception as e:
                return HttpResponse(f"Error: {e}")
                
    return HttpResponse("<h3>Insecure Deserialization Demo</h3><p>POST base64 encoded pickle data to 'data' parameter</p>")

# A02:2021-Cryptographic Failures
# Vulnerability: Exposure of sensitive data
def sensitive_data_view(request):
    # VULNERABLE: Initializing fake sensitive data
    fake_credit_card = "1234-5678-9012-3456"
    cvv = "123"
    
    # In a real scenario, this might be logging to a file that is readable by others
    # or returning it in the response when it shouldn't be.
    print(f"CRITICAL: Processing payment for card {fake_credit_card}, CVV: {cvv}")
    
    return HttpResponse(f"<h3>Cryptographic Failures Demo</h3><p>Payment processed for card: {fake_credit_card} (CVV: {cvv})</p><p>Note: This data is displayed in plain text and logged!</p>")

# A04:2021-Insecure Design
# Vulnerability: Business Logic Bypass
def bypass_business_logic(request):
    if request.method == 'POST':
        return HttpResponse("<h3>Order Placed!</h3><p>We processed your order without verifying payment status.</p>")
    return HttpResponse("<h3>Insecure Design Demo</h3><form method='post'><button>Finalize Order (Skip Payment)</button></form>")

# A05:2021-Security Misconfiguration
# Vulnerability: Information Exposure via Error Page
def misconfiguration_view(request):
    # Intentionally raise exception to show stack trace (if DEBUG=True)
    raise Exception("This is a demo exception to show stack trace and environment variables (Security Misconfiguration).")

# A06:2021-Vulnerable and Outdated Components
# Vulnerability: Usage of vulnerable components
def outdated_components_view(request):
    vulnerable_lib = "old-lib-v1.0.0 (CVE-2023-XXXX)"
    return HttpResponse(f"<h3>Component Analysis</h3><p>Detected Library: {vulnerable_lib}</p><p>Status: <b>CRITICAL VULNERABILITY</b></p>")

# A09:2021-Security Logging and Monitoring Failures
# Vulnerability: Critical action without logging
def silent_action_view(request):
    if request.method == 'POST':
        # Action executed but NOT logged
        return HttpResponse("Action 'Delete Logs' executed. No audit log created.")
    return HttpResponse("<h3>Logging Failure Demo</h3><form method='post'><button>Delete System Logs (Silent)</button></form>")

