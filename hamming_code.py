#!/usr/bin/python

import numpy as np

# H Matrix Hy=ei=Hi
H=np.array([[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]])

# R Matrix Ry.T=x
R=np.array([[0,0,1,0,0,0,0],[0,0,0,0,1,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,0,1]])

# Null Matrix
NM=[0,0,0]

def Correct(e,y): # Correct the y0 to z0 by flipping the bit by identifying 1 error
	# print("--FLIP FUCNTION--")
	e_idx=e[0] # Calculate idx in y is with error
	for i in range(1,len(e)):
		e_idx=e_idx*2+e[i]
	# print ("FLIP at idx ",e_idx)
	# print ("y UNFLIPPED ",y)
	for i in range(0,len(y)): #flipping the e_idx bit of y
		if i == e_idx-1:
			if y[i] == 0:
				y[i] = 1
			else:
				y[i] = 0
	# print ("y FLIPPED ",y)
	return y

def DecodeChar(y0,y1):
	# print("--------DECODE FUCNTION---------")
	# print("y0: ",y0," y1: ",y1)
	# print y0,y1
	char_message1=np.matmul(R,y0.T)
	char_message2=np.matmul(R,y1.T)
	char_message_array=np.append(char_message1,char_message2)
	# print char_message_array
	char_message_bin=""
	for i in range(len(char_message_array)):
		if char_message_array[i]==0:
			char_message_bin+=str(0)
		else:
			char_message_bin+=str(1)
	ascii_val=int(char_message_bin,2)
	# print str(chr(ascii_val)),ascii_val
	return str(chr(ascii_val))

filename="input.txt"
with open(filename, 'r') as f:
	line = f.readline()
	while(line):
		# print("##########################New LINE###########################")
		line = line.strip()
		if (len(line)%14!=0):
			print("INVALID")
			print("")
			line = f.readline()
			continue
		if (len(line) == 0):
			line = f.readline()
			continue
		#Chunk contains each lines divided in segments of length 14 bits
		chunk = [line[i:i+14] for i in range(0, len(line), 14)]
		# print chunk
		no_of_corruptedMessage=0
		total_no_of_message=0
		DecodeMessage=[]
		for itr in range(len(chunk)):
			# print("New message Chunk--------->")
			#y_message is the recived message unit (7+7) of actual sent message say x(4 + 4) 
			y_message = np.fromstring(chunk[itr],'u1') - ord('0')
			y0 = np.array(y_message[0:7])	#first half for decoding x[0:4]
			y1 = np.array(y_message[7:14])  #2nd half for decoding x[0:4]
			# print "Chunk part1: "+str(y0)+" ,Chunk Part2: "+str(y1)
			e0=np.matmul(H,y0.T) #e0 is error in 1st half
			e1=np.matmul(H,y1.T) #e1 is error in 2nd half
			y=np.append(y0,y1)
			# print ("y0: ",y0)
			# print ("y1: ",y1)
			# print (y)
			# print("Before ei mod 2")
			# print(e0," e0")
			# print(e1," e1")
			e0=np.remainder(e0,2)
			e1=np.remainder(e1,2)
			# print("After ei mod2")
			# print(e0," e0 Mod2")
			# print(e1," e1 Mod2")
			e0=e0[::-1]
			e1=e1[::-1]
			if np.array_equal(e0,NM) and np.array_equal(e1,NM):
				#error free character decoded.
				# Decode y0 and y1 as x0 and x1 and return x
				# print("y0: ",y0," ,y1: ",y1)
				# print("1")
				DecodeMessage.append(DecodeChar(y0,y1))
				total_no_of_message+=1
			else:
				#error containing character decoded
				#z0 and z1 is corrected y0 and y1
				z0=np.zeros((7,), dtype=int)
				z1=np.zeros((7,), dtype=int)
				if (not np.array_equal(e0,NM)):
					# print("Error y0:")
					z0=Correct(e0,y0)
				if (not np.array_equal(e1,NM)):
					# print("Error y1:")
					z1=Correct(e1,y1)
				# print("2")
				# print("y0 Correct: ",z0," ,y1 Correct: ",z1)
				DecodeMessage.append(DecodeChar(z0,z1))
				# print no_of_corruptedMessage
				no_of_corruptedMessage+=1
				total_no_of_message+=1
			# print(DecodeMessage)
		asciiText=""
		asciiText = asciiText.join(DecodeMessage)
		print(asciiText)
		print(str(int((float(no_of_corruptedMessage)/total_no_of_message*100.0)))+' %')
		# print()
		line = f.readline()