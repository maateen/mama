import os, sys

# Parsing arguments
try:
    if sys.argv[1]:
        param = sys.argv[1]
        print(param)
        os.system("http://en.wikipedia.org/w/index.php?search=\"+param+\"")
    else:
        print("Not enough parameters to search on wikipedia.")
except:
    print("Not enough parameters to search on wikipedia.")
