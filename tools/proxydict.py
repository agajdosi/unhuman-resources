import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

out = open("out.txt", "w")
out.write('proxies = [\n    {"proxy": "", "score": 200.0},\n')

file = open("proxies.txt", "r") 
for proxy in file:
    line = '    {"proxy": "http://'+ proxy.rstrip() + '", "score": 100.0},\n'
    out.write(line)

out.write("]\n")

