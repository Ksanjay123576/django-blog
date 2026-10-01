import os
import django
from cryptography.fernet import Fernet
from django.core.serializers import deserialize
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

User = get_user_model()

if User.objects.exists():
    print("Database already contains users. Skipping restore.")
else:
    print("Starting database restore...")

    key = os.environ["DATABASE_ENCRYPTION_KEY"]

    with open("data.json.enc", "rb") as f:
        encrypted_data = f.read()

    data = Fernet(key).decrypt(encrypted_data).decode("utf-16")

    count = 0
    skipped_profiles = 0

    for obj in deserialize("json", data):

        # Skip profile records because Django/user registration
        # may already create profiles automatically.
        if obj.object.__class__.__name__ == "Profile":
            skipped_profiles += 1
            continue

        obj.save()
        count += 1

    print(f"Database data restored successfully! Total records: {count}")
    print(f"Skipped profiles: {skipped_profiles}")