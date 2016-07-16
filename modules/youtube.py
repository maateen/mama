import os, sys

# Parsing arguments
try:
    if sys.argv[1]:
        param = sys.argv[1]
        print(param)
        os.system(
            "xdg-open http://www.youtube.com/results?search_query=\"+param+\"")
    else:
        print("Not enough parameters to search on youtube.")
except:
    print("Not enough parameters to search on youtube.")
