import os
import sys

# Parsing arguments
try:
    if sys.argv[1]:
        param = sys.argv[1]
        execute = "xdg-open https://en.wikipedia.org/wiki/" + param + ""
        print(execute)
        os.system(execute)
    else:
        print("Not enough parameters to search on wikipedia.")
except:
    print("Not enough parameters to search on wikipedia.")
