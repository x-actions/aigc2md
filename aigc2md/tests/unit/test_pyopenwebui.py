# import os

# import pyopenwebui
# from pyopenwebui import Pyopenwebui, DefaultHttpxClient

# client = Pyopenwebui(
#     # Or use the `PYOPENWEBUI_BASE_URL` env var
#     base_url='https://ai.80.xyz',
#     bearer_token=os.environ.get("PYOPENWEBUI_API_KEY"),
#     max_retries=3,
#     default_headers={},
#     http_client=DefaultHttpxClient(),
# )

# try:
#     # print(client.chats.list_all())
#     print(client.api.v1.users.get(limit=3, skip=1))
# except pyopenwebui.APIConnectionError as e:
#     print("The server could not be reached")
#     print(e.__cause__)  # an underlying Exception, likely raised within httpx.
# except pyopenwebui.RateLimitError as e:
#     print("A 429 status code was received; we should back off a bit.")
# except pyopenwebui.APIStatusError as e:
#     print("Another non-200-range status code was received")
#     print(e.status_code)
#     print(e.response)
