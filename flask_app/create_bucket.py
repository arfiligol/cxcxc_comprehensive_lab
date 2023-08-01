from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

import os
# 指定 gcs-emulator host
os.environ["STORAGE_EMULATOR_HOST"] = os.getenv("STORAGE_EMULATOR_HOST")


client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)

# create bucket
bucket = client.create_bucket(os.getenv("GCS_BUCKET_NAME"))
