import os
import sys

# Parsing arguments
try:
    if sys.argv[1]:
        param = sys.argv[1]
        execute = "xdg-open https://www.youtube.com/results?search_query" \
                  "=" + param + ""
        print(execute)
        os.system(execute)
    else:
        print("Not enough parameters to search on youtube.")
except:
    print("Not enough parameters to search on youtube.")
