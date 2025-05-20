# import sys
# processing = __import__('1-batch_processing')

# ##### print processed users in a batch of 50
# try:
#     processing.batch_processing(50)
# except BrokenPipeError:
#     sys.stderr.close()

#from 1-batch_processing import batch_processing
processing = __import__('1-batch_processing')
import sys

##### print processed users in a batch of 50
try:
    processing.batch_processing(50)
except BrokenPipeError:
    sys.stderr.close()

# for batch in batch_processing(5):  # process 5 users at a time
#     for user in batch:
#         print(user)
