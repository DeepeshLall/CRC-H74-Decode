#!/usr/bin/python

ESC = '0xa5'
FLAG = '0xa9'
XORED_ESC = '0xc5'
XORED_FLAG = '0xc9'

xoredByteDictionary = {XORED_FLAG : FLAG, XORED_ESC : ESC}
ByteLength=8

# Taking input and converting to Byte List i.e grouping the input binaryStream
# by 8 bit => 1 Byte and typecasting to Hexadecimal.
string=str(input())
ByteStream = [(hex(int((string[i:i+ByteLength]),2))) for i in range(0, len(string), ByteLength)]
# print(ByteStream)

#Converting Byte List into List of Frames with removed FLAGS.
FrameList=[]
FrameBegin=False
FrameEnd=False
FrameCount=0
for i in range(len(ByteStream)):
	# print (ByteStream[i]+" Frame Begin: "+str(FrameBegin)+" Frame End: "+str(FrameEnd))
	if ((not (FrameBegin)) and (ByteStream[i] == FLAG)):
		# print (str(FrameCount)+" Frame Begin :::"+ByteStream[i])
	    #Frame Begin is not initialized and we found a frame start
		FrameBegin=True 
		# Initialize Frame Begin
		Frame=[] 
		#Initialize Frame[]
	else:    
	#Frame Have Started
		if (not (FrameEnd)) : 
		#Frame Haven't Ended
			if ByteStream[i] == ESC: 
			#If we found next Byte as ESC put it and next byte in Frame[]
				Frame.append(ByteStream[i])
				# print("Appending "+ByteStream[i]+" to Frame No.: "+FrameCount)
				i+=1
				Frame.append(ByteStream[i])
				# print("Appending "+ByteStream[i]+" to Frame No.: "+FrameCount)
			elif ByteStream[i] == FLAG: 
			#If we found FLAG Not followed by ESC end Frame[]
				# print (str(FrameCount)+" Frame End :::"+ByteStream[i])
				FrameEnd=True
			else: 
			# Just add the Byte in the Frame to Frame[]
				# print("Appending "+ByteStream[i]+" to Frame No.: "+str(FrameCount))
				Frame.append(ByteStream[i])
		if FrameEnd : 
		# If we found the Frame End
			# print ("Appending Frame: "+str(Frame)+" to FrameList\n")
			FrameList.append(Frame) 
			#append it to FrameList
			FrameBegin=False 
			#initialize Frame back to False.
			FrameEnd=False
			FrameCount+=1
#print(FrameList)

#Check CRC_CHECKBITS


print(FrameList)