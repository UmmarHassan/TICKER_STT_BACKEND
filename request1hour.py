# from urllib3 import PoolManager
# import time

# certificate_path = "certificate.crt"
# private_key_path = "private.key"

# # Disable SSL verification
# http = PoolManager(cert_reqs='CERT_NONE', ca_certs=None)

# while True:
#     try:
#         response = http.request(
#             'GET',
#             'https://192.168.2.168:8000/index/',
#             timeout=5.0,  # Adjust the timeout as needed
#             retries=False,  # Disable retries
#             preload_content=False,  # Do not preload content for stream
#             headers={'Connection': 'close'},  # Close the connection after each request
#         )

#         print(f"Initiated process. Response: {response.data.decode('utf-8')}")

#         # If the request is successful, sleep for 5 minutes (300 seconds) before sending the next request
#         time.sleep(3600)

#     except Exception as e:
#         print(f"Error sending request to initiate process: {e}")
#         # Sleep for a short duration before retrying
#         time.sleep(10)
from urllib3 import PoolManager
import time

certificate_path = "localhost.crt"
private_key_path = "localhost.key"

# Use HTTPS and enable SSL verification
http = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certificate_path)

while True:
    try:
        response = http.request(
            'GET',
            'https://192.168.2.168:8000/index/',
            timeout=5.0,
            retries=False,
            preload_content=False,
            headers={'Connection': 'close'},
        )

        print(f"Initiated process. Response: {response.data.decode('utf-8')}")

        # If the request is successful, sleep for 5 minutes (300 seconds) before sending the next request
        time.sleep(3600)

    except Exception as e:
        print(f"Error sending request to initiate process: {e}")
        # Sleep for a short duration before retrying
        time.sleep(10)
