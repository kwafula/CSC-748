from pwn import *

# connect to local binary process
# p = processs("./lab1-1.bin")

# connect to remote server process at port 7011
p = remote("csc748.hostbin.org", 7011)

# read data upto secret string
p.recvuntil(b"\n\n")

# get and print secret string 
s = p.recv(15)
print(f"The secret string was: {s}")

# send back secret string
p.sendline(s)

# establish interactive session 
p.interactive()

# add code to print flag.txt

# function address to call is 0x40130f or 4199183 in decimal
# Flag to fetched is: flag{082f90215133f4755f27ec6850b1eecc}


