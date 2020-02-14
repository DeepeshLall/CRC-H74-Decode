#!/usr/bin/python

ESC = '0xa5'
FLAG = '0xa9'
XORED_ESC = '0xc5'
XORED_FLAG = '0xc9'
KEY = '0x83'

xoredByteDictionary = {XORED_FLAG : FLAG, XORED_ESC : ESC}
ByteLength=8

################################### TAKING INPUT AND CONVERTING TO BYTE LIST i.e grouping the input binaryStream #################################
# by 8 bit => 1 Byte and typecasting to Hexadecimal.
string=str(input())
ByteStream = [format(int((string[i:i+ByteLength]),2),'#04x') for i in range(0, len(string), ByteLength)]
# print("--------------------------BYTE STREAM----------------------")
# print(ByteStream)

####################################CONVERTING Byte List into List of Frames with removed FLAGS.#####################################################
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
# print(int(FrameList[0][0],16))
# print("--------------------------FRAME LIST---------------------")
# print(FrameList)

####################################### CHECK CRC_CHECKBITS ##############################################
# print("--------------------------CHECK CRC LIST---------------------")

# Returns XOR of 'a' and 'b'
# (both of same length)
def xor(a, b):
    # initialize result
    result = []
    # Traverse all bits, if bits are
    # same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

# Performs Modulo-2 division
def mod2div(divident, divisor):
    # Number of bits to be XORed at a time.
    pick = len(divisor)
    # Slicing the divident to appropriate
    # length for particular step
    tmp = divident[0 : pick]
    while pick < len(divident):
        if tmp[0] == '1':
            # replace the divident by the result
            # of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            # If leftmost bit is '0'
            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor.
            tmp = xor('0'*pick, tmp) + divident[pick]
        # increment pick to move further
        pick += 1
    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    checkword = tmp
    return checkword

# Function used at the sender side to encode
# data by appending remainder of modular divison
# at the end of data.
def isFrame(data, key):
    l_key = len(key)
    # Appends n-1 zeroes at end of data
    appended_data = data + '0'*(l_key-1)
    # print ("DATA APPENDED: "+appended_data)
    # print ("KEY: "+key)
    remainder = mod2div(appended_data, key)
    # print ("REMAINDER: "+remainder)
    # Append remainder in the original data
    if(int(remainder)==0):
    	return 1 # Correct Frame
    else:
    	return 0 #Incorrect Frame

#convert Data and KEY in Hexadecimal => Int => Bin => String
#convert back the binary string output => int => hex
DataList=[]
for i in range(len(FrameList)):
	data=""
	for j in range(len(FrameList[i])):
		# print("Data Added : "+str(FrameList[i][j])+"    Binary value ===> "+str(format(int(str(FrameList[i][j]),16),'010b'))[2:])
		data=data+str(format(int(str(FrameList[i][j]),16),'010b'))[2:]
	# print(data)
	DataList.append(data)
# print DataList

ValidFrameSet=[]
inValidFrameSetid=[]
FrameNumber=1
for i in range(len(DataList)):
	if isFrame(DataList[i],str(bin(int(str(KEY),16)))[2:]):
		ValidFrameSet.append(DataList[i])
		FrameNumber+=1
	else:
		inValidFrameSetid.append(FrameNumber)
		FrameNumber+=1

inValidFramesNumber=","
inValidFramesNumber = inValidFramesNumber.join(inValidFrameSetid)

# print FrameCount #FrameNumber=FrameCount
# print(inValidFrameSetid)
# print(ValidFrameSet)

##########################################REMOVING THE BYTE STUFFING AND READING ITS ASCII############################################
# print("--------------------------REMOVING THE BYTE STUFFING AND READING ITS ASCII---------------------")

def unstuff(dataList):
	unstuffedData=[]
	for itr in range(len(dataList)):
		if dataList[itr] == ESC:
			itr+=1
			if dataList[itr] in xoredByteDictionary:
				unstuffedData.append(xoredByteDictionary[itr])
			else:
				unstuffedData.append(ESC)
				unstuffedData.append(dataList[itr])
		else:
			unstuffedData.append(dataList[itr])
	return unstuffedData
#making a list of valid data(i.e. without checksum) in Hexadecimal
asciiData=[]
for i in range(len(ValidFrameSet)):
	DataStream = str(ValidFrameSet[i])
	ValidHexData = [str(format(int((DataStream[i:i+ByteLength]),2),'#04x')) for i in range(0, len(DataStream)-ByteLength, ByteLength)]
	unstuffedDataList=unstuff(ValidHexData)
	for j in  range(len(unstuffedDataList)):
		asciiData.append(str(chr(int(str(unstuffedDataList[j]),16))))
# print ValidHexDataList
asciiText=""
asciiText = asciiText.join(asciiData)

#############################################PRINTING OUTPUT#############################################

print FrameCount
print inValidFramesNumber
print asciiText



