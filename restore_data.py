import os
import django
import json
from cryptography.fernet import Fernet
from django.core.serializers import deserialize

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

key = os.environ["DATABASE_ENCRYPTION_KEY"]

with open("data.json.enc", "rb") as f:
    encrypted_data = f.read()

data = Fernet(key).decrypt(encrypted_data).decode("utf-8")

for obj in deserialize("json", data):
    obj.save()

print("Database data restored successfully!")