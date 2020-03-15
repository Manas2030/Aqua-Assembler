# Aqua-Assembler
# MANAS GUPTA
# PRACHI GOYAL

#Initializations
opcodeSymbol = {}
locationCount=0
symbolTable={}
labelTable={}
literalTable={}
opcodeTable=[]
# psudo opcodes = assembler directives
pseudoOpcodes=['START','LTORG','DS','DC']
byteCode=''
endFlag=False
startFlag=False
errorFlag=False
usedChar=[]      #includes all literals, labels and symbols that have been used in the source code
usedCharLC=[]
declaredChar=[]	 #includes all literals, labels and symbols that have been declared in the source code
declaredCharLC=[]
registers=['R0','R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11','R12','R13','R14','R15']
checkLTORG = 0;
checkSTP = 0;
correctAlpha = ['a','b','c','d','e','f']
incorrectAlpha = ['g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


#PASS ONE
with open('opcodeSymbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		opcodeSymbol[tmp[0]]=tmp[1]

with open('sourceCode.txt','r') as fr:
	for line in fr:
		line=line.strip()
		if(len(line)==0):
			continue
		tmp = line.split()

		#set val of LC
		if(tmp[0]=="START"):
			if(startFlag):
				print('ERROR at line: '+ str(locationCount))
				print('START already used, cannot initialize Location counter again')
				locationCount-=1
			else:
				if(len(tmp)==1):
					locationCount = 0
				else:
					locationCount = int(tmp[1])       	 #initialize the value of LC 
					if(locationCount>31):
						locationCount=0
						print('ERROR at line: '+ str(locationCount))
						print('Exceeded memory limit. Location counter cannot start from 31.')
						locationCount-=1
				startFlag=True
		#check if comment
		elif(tmp[0]=="@"):
			locationCount = locationCount-1
		elif(tmp[0]=="STP"):                             #raises an error if STP used multiple times
			opcodeTable.append(['STP','1100','  ','1'])
			if(checkSTP==0):
				checkSTP = 1
			else:
				print("Declarative statement error. STP used multiple times. Error at locationCount: "+str(locationCount))
				locationCount-=1	

		#check for labelTable
		elif(tmp[0][-1]==":"):
			labelTable[tmp[0]]= bin(locationCount)
			declaredChar.append(tmp[0][:-1])
			declaredCharLC.append(locationCount)
		
		#check for symbolTable
		##decimal
		elif(len(tmp)>1 and tmp[1]=="DC"):
			sg = 0
			for i in tmp[2][1:-1]:
				if(i in correctAlpha or i in incorrectAlpha):
					print("Value Error. "+ i +" present in decimal value. Error at locationCount: "+str(locationCount)+". Corrected Value taken as 0.")
					sg = 1
			if(sg==0):
				symbolTable[tmp[0]] = [bin(int(tmp[2][1:-1])),bin(locationCount)]
				declaredChar.append(tmp[0])
				declaredCharLC.append(locationCount)
				if(len(str(bin(int(tmp[2][1:-1])))[2:])>6):     #raises error if binary value of symbol exceeds 6 bits
					print("Word limit exceeded for "+tmp[0]+". Given literal can't be represented in 6 bits. Error at locationCount: "+str(locationCount))
					locationCount-=1
			else:
				symbolTable[tmp[0]] = ['0b000000',bin(locationCount)]
				declaredChar.append(tmp[0])
				declaredCharLC.append(locationCount)		
		##hexadecimal
		elif(len(tmp)>1 and tmp[1]=="DS"):
			sg = 0
			for i in tmp[2][1:-1]:
				if(i in incorrectAlpha):
					print("Value Error. "+ i +" present in hexadecimal value. Error at locationCount: "+str(locationCount)+". Corrected Value taken as 0.")
					sg = 1
			if(sg==0):	
				symbolTable[tmp[0]] = [bin(int(tmp[2][1:-1],16)),bin(locationCount)]
				declaredChar.append(tmp[0])
				declaredCharLC.append(locationCount)
				if(len(str(bin(int(tmp[2][1:-1],16)))[2:])>6):	#raises error if binary value of symbol exceeds 6 bits
					print("Word limit exceeded for "+tmp[0]+". Given literal can't be represented in 6 bits. Error at locationCount: "+str(locationCount))
					locationCount-=1
			else:
				symbolTable[tmp[0]] = ['0b000000',bin(locationCount)]
				declaredChar.append(tmp[0])
				declaredCharLC.append(locationCount)
		
				
		#check for literalTable
		if(checkLTORG==1):
			if(tmp[min(1,len(tmp)-1)][1]=="h"):
				sg = 0
				for i in tmp[1][3:-1]:
					if(i in incorrectAlpha):
						print("Value Error. "+ i +" present in hexadecimal value. Error at locationCount: "+str(locationCount)+". Corrected Value taken as 0.")
						sg = 1
				if(sg==0):		
					literalTable[tmp[1]] = [bin(int(tmp[1][3:-1],16)),bin(locationCount)]
					declaredChar.append(tmp[1])
					declaredCharLC.append(locationCount)
					if(len(str(bin(int(tmp[1][3:-1],16)))[2:])>6):		#raises error if binary value of symbol exceeds 6 bits
						print("Word limit exceeded for "+tmp[1]+". Given literal can't be represented in 6 bits. Error at locationCount: "+str(locationCount))
						locationCount-=1
				else:
					literalTable[tmp[1]] = ['0b000000',bin(locationCount)]
					declaredChar.append(tmp[1])
					declaredCharLC.append(locationCount)		
			
			elif(tmp[min(1,len(tmp)-1)][1]=="'" or tmp[min(1,len(tmp)-1)][1]=="d"):
				if(tmp[1][1]=="d"):
					sg = 0
					for i in tmp[1][3:-1]:
						if(i in incorrectAlpha or i in correctAlpha):
							print("Value Error. "+ i +" present in hexadecimal value. Error at locationCount: "+str(locationCount)+". Corrected Value taken as 0.")
							sg = 1
					if(sg==0):
						literalTable[tmp[1]] = [bin(int(tmp[1][3:-1])),bin(locationCount)]
						declaredChar.append(tmp[1])
						declaredCharLC.append(locationCount)
						if(len(str(bin(int(tmp[1][3:-1])))[2:])>6):		#raises error if binary value of symbol exceeds 6 bits
							print("Word limit exceeded for "+tmp[1]+". Given literal can't be represented in 6 bits. Error at locationCount: "+str(locationCount))
							locationCount-=1
					else:
						literalTable[tmp[1]] = ['0b000000',bin(locationCount)]
						declaredChar.append(tmp[1])
						declaredCharLC.append(locationCount)
				else:
					sg = 0
					for i in tmp[1][2:-1]:
						if(i in incorrectAlpha or i in correctAlpha):
							print("Value Error. "+ i +" present in hexadecimal value. Error at locationCount: "+str(locationCount)+". Corrected Value taken as 0.")
							sg = 1
					if(sg==0):
						literalTable[tmp[1]] = [bin(int(tmp[1][2:-1])),bin(locationCount)]
						declaredChar.append(tmp[1])
						declaredCharLC.append(locationCount)
						if(len(str(bin(int(tmp[1][2:-1])))[2:])>6):		#raises error if binary value of symbol exceeds 6 bits
							print("Word limit exceeded for "+tmp[1]+". Given literal can't be represented in 6 bits. Error at locationCount: "+str(locationCount))
							locationCount-=1
					else:
						literalTable[tmp[1]] = ['0b000000',bin(locationCount)]
						declaredChar.append(tmp[1])
						declaredCharLC.append(locationCount)
			elif(tmp[0]=='LTORG'):
				print("Declarative statement error. LTORG used multiple times. Error at locationCount: "+str(locationCount))
				locationCount-=1
			else:
				checkLTORG = 0

		#updating the usedChar list
		elif(len(tmp)>1 and (((tmp[0] in opcodeSymbol.keys()) and (tmp[0]!='CLA')) or (len(tmp)>2 and (tmp[1] in opcodeSymbol.keys()) and (tmp[1]!='CLA')))):
			if(tmp[0] in opcodeSymbol.keys()): 
				opcodeTable.append([tmp[0],opcodeSymbol[tmp[0]],tmp[1],'2'])
				if(tmp[1] not in registers  and (tmp[1][0]!='#')):
					usedChar.append(tmp[1])
					usedCharLC.append(locationCount)
			else:
				opcodeTable.append([tmp[1],opcodeSymbol[tmp[1]],tmp[2],'2'])
				if(tmp[2] not in registers  and (tmp[2][0]!='#')):
					usedChar.append(tmp[2])
					usedCharLC.append(locationCount)

		elif((len(tmp)>1 and tmp[1]=='CLA') or tmp[0]=='CLA'):
			opcodeTable.append(['CLA','0000','  ','1'])
					
		locationCount = locationCount + 1	#set LC value
		if(locationCount>64):		#LC value cannot exceed 63 as 6 bits assigned for memory address
			print('Exceeded memory limit. 6 bits allocated for memory address and thus maximum number of instructions cannot exceed 64. Error at locationCount: '+str(locationCount))


#check if a symbol/literal/label hasn't been declared/initialized
j=-1
for i in usedChar:
	j = j+1
	if(i not in declaredChar):
		print("Declaration error. "+i+" not initialized. Error at locationCount: "+str(usedCharLC[j]))

#check if a symbol/literal/label has been declared/initialized multiple times	
n = len(declaredChar)
for i in range(1,n):
	if(declaredChar[i] in declaredChar[:i]):
		print("Declaration error. "+declaredChar[i]+" initialized multiple times. Error at locationCount: "+str(declaredCharLC[i]))			

				
def addZeroes(reg): 
	'''function to make a binary value 6 bit long'''
	reg = reg[2:]
	reg = '0'*(6-len(reg))+reg
	return reg	

#creating labelTable
with open('labelTable.txt','w') as f:
	for i in labelTable:
		f.write(i[:-1]+' '+ addZeroes(labelTable[i]))
#creating literalTable		
with open('literalTable.txt','w') as f:
	for i in literalTable:
		f.write(i+' '+ addZeroes(literalTable[i][0])+' '+addZeroes(literalTable[i][1]))
		
#creating symbolTable		
with open('symbolTable.txt','w') as f:
	for i in symbolTable:
		f.write(i+' '+ addZeroes(symbolTable[i][0])+' '+addZeroes(symbolTable[i][1]))

#creating opcodeTable
with open ('opcodeTable.txt','w') as f:
	for i in opcodeTable:
		f.write(i[0]+' '+i[1]+' '+i[2]+' '+i[3]+'\n')

# PASS TWO

with open ('symbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		symbolTable[tmp[0]]=[tmp[1],tmp[2]]

with open ('literalTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		literalTable[tmp[0]]=[[tmp[1],tmp[2]]]

with open('labelTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		labelTable[tmp[0]]=tmp[1]

def check(name):
	'''
	Function to check if parameter is pseudo-Opcode 
	'''
	if (name in pseudoOpcodes):
		return True
	try:
		tmp = symbolTable[name]
		return True
	except:
		return False

def registerAddress(reg):
	'''
	Function to convert register number to it's binary address
	'''
	reg = reg[1:]
	reg = bin(int(reg))[2:]
	reg = '0'*(6-len(reg))+reg
	return reg

def byteCodeFunc(opcode,addressMode,operand):
	'''
	Function to return assembly instruction's binary output (space separated)
	'''
	return opcode+' '+addressMode+' '+operand

def isOperandImmediate(operand):
	'''
	Function to check immediate operand
	'''
	if('#' in operand):
		return True
	else:
		return False

def isOperandLiteral(operand):
	'''
	Function to check literal operand
	'''
	try:
		tmp=literalTable[operand]
		return True
	except:
		return False

def isOperandSymbol(operand):
	'''
	Function to check symbol operand
	'''
	try:
		tmp=symbolTable[operand]
		return True
	except:
		return False

def isOperandLabel(operand):
	'''
	Function to check label operand
	'''
	try:
		tmp=labelTable[operand]
		return True
	except:
		return False

def isOperandRegister(operand):
	'''
	Function to check register operand
	'''
	if(operand[0]=='R'):
		return True
	else:
		return False

def checkIllegalOpcode(opcode):
	'''
	Function to check ILLEGAL OpCode
	'''
	if(opcode not in opcodeSymbol):
		return True
	return False

def checkforCLAandSTP(opcode):
	'''
	Function to check if opcode is CLA/STP (for error handling)
	'''
	if(opcode == 'STP'):
		global endFlag
		endFlag=True
		return True
	if(opcode == 'CLA'):
		return True
	return False

locationCount=0
startFlag=False

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		for line in fr:
			locationCount+=1
			line=line.strip()
			if(len(line)==0):
				locationCount-=1
				continue
	
			#check for comment line
			elif (line[0]=='@'):
				locationCount-=1
				continue
			elif (line[0]=='*'):
				locationCount-=1
				continue
			else:
				tmp = line.split()
				if(tmp[0]=="START"):
					if(startFlag):
						pass
					else:
						if(len(tmp)==1):
							locationCount = 0
						else:
							locationCount = int(tmp[1])
							if(locationCount>31):
								locationCount=0
						startFlag=True
					continue
				#check for label line
				if(':' in tmp[0]):
					tmp[0]=tmp[1]
					tmp[1]=tmp[2]
					# del tmp[2] because comparing length of tmp later
					del tmp[2]
				#check for directive statement
				if(check(tmp[0])):
					locationCount-=1
					continue
				else:
					if(checkIllegalOpcode(tmp[0])):
						print('ERROR at line: '+ str(locationCount))		
						print(tmp[0] + ' is an ILLEGAL Opcode')
						locationCount-=1
						fw.write(' '+'\n')
						continue

					if(len(tmp)==1):
						# length = 1 for CLA and STP only
						if(checkforCLAandSTP(tmp[0])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00','000000')
						else:
							print('ERROR at line: '+ str(locationCount))
							print(tmp[0] + ' requires 1 Operand')
							locationCount-=1
							errorFlag=True
					else:
						if(len(tmp)!=2):
							print('ERROR at line: '+ str(locationCount))
							print("Too many operand(s) for "+tmp[0])
							locationCount-=1
							errorFlag=True

						if(checkforCLAandSTP(tmp[0])):
							print('ERROR at line: '+ str(locationCount))
							print(tmp[0] + ' requires 0 Operands')
							locationCount-=1
							errorFlag=True

						if(isOperandLiteral(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',literalTable[tmp[1]])
						elif(isOperandLabel(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',labelTable[tmp[1]])
						elif(isOperandImmediate(tmp[1])):
							immediateValue=int(tmp[1][1:])
							if(tmp[0]=='DIV' and immediateValue==0):
								print('ERROR at line: '+ str(locationCount))
								print('Zero Division Error')
								locationCount-=1
								errorFlag=True
							else:
								byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00',registerAddress('R'+str(immediateValue)))
						elif(isOperandSymbol(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',symbolTable[tmp[1]][1])
						# check operand for register in the last because symbol(or anything) could start with 'R'...	
						elif(isOperandRegister(tmp[1])):
							try:
								registerNum=int(tmp[1][1:])
								if(registerNum<0 or registerNum>15):
									print('ERROR at line: '+ str(locationCount))
									print('Register Number should be from 0 to 15 (inclusive)')
									locationCount-=1
									errorFlag=True
							except:
								errorFlag=True 
							else:
								byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'10',registerAddress(tmp[1]))
						else:
							continue

					if(errorFlag):
						global bytecode
						byteCode = ' '
						errorFlag=False

					fw.write(byteCode+'\n')
					
if(endFlag == False):
	print('ERROR at line: '+ str(locationCount))
	print('END statement missing. Use STP as well')
