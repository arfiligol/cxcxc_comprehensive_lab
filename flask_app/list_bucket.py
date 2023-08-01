from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

import os
# 指定 gcs-emulator host
os.environ["STORAGE_EMULATOR_HOST"] = os.getenv("STORAGE_EMULATOR_HOST")


client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)

# List the Buckets
for bucket in client.list_buckets():
    print(f"Bucket: {bucket.name}\n")

    # List the Blobs in each Bucket
    for blob in bucket.list_blobs():
        print(f"Blob: {blob.name}")