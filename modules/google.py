import os
import sys

# Parsing arguments
try:
    if sys.argv[1]:
        param = sys.argv[1]
        execute = "xdg-open https://www.google.com/search?q=" + param + "&gws_rd=ssl"
        os.system(execute)
    else:
        print("Not enough parameters to search on google.")
except:
    print("Not enough parameters to search on google.")
