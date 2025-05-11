# colab-config-s3-rclone

Run in a colab runtime environment to configure AWS S3 + rclone to simplify syncing runtime environment data to S3.

To configure syncing, run this in a Google Colab notebook:

```python
!apt install rclone
!curl -o /root/config_s3_rclone.py https://raw.githubusercontent.com/darkhaniop/colab-config-s3-rclone/refs/heads/main/main.py

def _setup_syncing() -> None:
    from google.colab import userdata
    key_id = userdata.get('AWS_ACCESS_KEY_ID')
    secret_key = userdata.get('AWS_SECRET_ACCESS_KEY')
    bucket = userdata.get('BUCKET_NAME')
    %run /root/config_s3_rclone.py --aws-key-id $key_id --aws-secret-key $secret_key --bucket $bucket

_setup_syncing()
del _setup_syncing
```
