import os
import django
from cryptography.fernet import Fernet
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

key = os.environ["DATABASE_ENCRYPTION_KEY"]

with open("data.json.enc", "rb") as f:
    encrypted_data = f.read()

data = Fernet(key).decrypt(encrypted_data)

with open("data_restore.json", "wb") as f:
    f.write(data)

call_command("loaddata", "data_restore.json")

os.remove("data_restore.json")

print("Database data restored successfully!")