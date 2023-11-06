import os
import time

LOOP = True
while LOOP == True:

        # Open and read target file /dev/shm/flag.txt.xxxxxx
	try:
		path = "/dev/shm"
		for filename in os.listdir(path):
			print("File found: ", filename)
			#print(type(filename))
			filepath = os.path.join(path, filename)
			with  open(filepath, "r") as file:
				print("File content: ", file.read())
				LOOP = False
	except IOError:
		print("Error: File not found")
