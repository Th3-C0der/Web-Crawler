# colors 
r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
d = "\033[2;37m"
R = "\033[1;41m"
Y = "\033[1;43m"
B = "\033[1;44m"
w = "\033[1;37m"

#----------------modules
from os import system,name
from time import sleep


# -----clear 
system('cls' if name=='nt' else 'clear')

#-------update
system('cd ..')
system('rm -rf Web-Crawler')
sleep(0.1)
system('git clone https://github.com/Th3-C0der/Web-Crawler')
system('cd Web-Crawler')
print(r+"└─ "+r+"\033[1;37m>> Script Updated <<")
print(r+"└─ "+g+"\033[1;37m>> Now Run Tool Using <<")
print(r+"└─ "+b+"\033[1;37m>> python main.py <<")
sleep(0.5)
