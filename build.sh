#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from axes.models import AccessAttempt
# 1. تصفير محاولات الحظر السابقة لفتح الباب أمامك
AccessAttempt.objects.all().delete()
print('Axes attempts cleared.')

# 2. إنشاء أو تحديث كلمة مرور الـ Admin
User = get_user_model()
username = 'waeel'
password = 'waeel@#780209547' # تأكد من حفظ هذه الكلمة جيداً

user, created = User.objects.get_or_create(username=username, defaults={'email': 'admin@example.com'})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.save()
print(f'User {username} updated/created successfully.')
EOF
