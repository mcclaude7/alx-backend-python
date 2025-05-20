

from itertools import islice
#from stream_users import stream_users  # ✅ Correct way to import the function
stream_users = __import__('0-stream_users')
for user in islice(stream_users(), 6):
    print(user)
