from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

import os
# 指定 gcs-emulator host
os.environ["STORAGE_EMULATOR_HOST"] = "http://gcs-emulator.cxcxc.pri:4443"


client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)

# # create bucket
# bucket = client.create_bucket("app1-web-bucket")
# # delete bucket
# bucket = client.get_bucket("test-bucket").delete()

# List the Buckets
for bucket in client.list_buckets():
    print(f"Bucket: {bucket.name}\n")

    # List the Blobs in each Bucket
    for blob in bucket.list_blobs():
        print(f"Blob: {blob.name}")