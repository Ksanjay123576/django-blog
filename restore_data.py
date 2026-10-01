import os
import django
from cryptography.fernet import Fernet
from django.core.serializers import deserialize
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

User = get_user_model()

# Don't restore again if users already exist
if User.objects.exists():
    print("Database already contains users. Skipping restore.")
else:
    print("Starting database restore...")

    key = os.environ["DATABASE_ENCRYPTION_KEY"]

    with open("data.json.enc", "rb") as f:
        encrypted_data = f.read()

    data = Fernet(key).decrypt(encrypted_data).decode("utf-16")

    count = 0

    for obj in deserialize("json", data):
        obj.save()
        count += 1

    print(f"Database data restored successfully! Total records: {count}")