import pandas as pd
print("Testing")
import os
#os.sys("pip freeze > freeze.txt")

myCmd = os.popen('ls -la').read()
print(myCmd)

