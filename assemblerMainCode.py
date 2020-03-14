# ASSEMBLER PROJECT
# MANAS GUPTA
# PRACHI GOYAL

#Initializations
opcodeSymbol = {}
locationCount=0
symbolTable={}
labelTable={}
literalTable={}
pseudoOpcodes=['START','LTORG']
byteCode=''
endFlag=False
errorFlag=False

sg = 0;

with open('opcodeSymbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		opcodeSymbol[tmp[0]]=tmp[1]

with open('sourceCode.txt','r') as fr:
	for line in fr:
		tmp = line.split()

		#set val of LC
		if(tmp[0]=="START"):
			locationCount = int(tmp[1])

		#check if comment
		elif(tmp[0]=="@"):
			pass
		elif(tmp[0]=="STP"):
			pass

		#check for labelTable
		elif(tmp[0][-1]==":"):
			labelTable[tmp[0]]= bin(locationCount)
		

		#check for symbolTable
		##decimal
		elif(tmp[min(1,len(tmp)-1)]=="DC"):

			symbolTable[tmp[0]] = [bin(int(tmp[2][1:-1])),bin(locationCount)]
		
		##hexadecimal
		elif(tmp[min(1,len(tmp)-1)]=="DS"):
			symbolTable[tmp[0]] = [bin(int(tmp[2][1:-1],16)),bin(locationCount)]
		

		#check for literalTable
		if(sg==1):
			if(tmp[min(1,len(tmp)-1)][1]=="h"):
				literalTable[tmp[1]] = [bin(int(tmp[1][3:-1],16)),bin(locationCount)]
			
			elif(tmp[min(1,len(tmp)-1)][1]=="'" or tmp[min(1,len(tmp)-1)][1]=="d"):
				if(tmp[1][1]=="d"):
					literalTable[tmp[1]] = [bin(int(tmp[1][3:-1])),bin(locationCount)]
				
				else:
					literalTable[tmp[1]] = [bin(int(tmp[1][2:-1])),bin(locationCount)]
				
			
			else:
			 sg = 0
			
		
		elif(tmp[0]=="LTORG"):
			sg=1
		
		locationCount = locationCount + 1

# REMOVE THIS LATER		
print(literalTable)
print(labelTable)
print(symbolTable)

def regAddress(reg):
	reg = reg[2:]
	reg = '0'*(6-len(reg))+reg
	return reg	

with open('labelTable.txt','w') as f:
	for i in labelTable:
		f.write(i[:-1]+' '+ regAddress(labelTable[i]))
with open('literalTable.txt','w') as f:
	for i in literalTable:
		f.write(i+' '+ regAddress(literalTable[i][0])+' '+regAddress(literalTable[i][1]))
with open('symbolTable.txt','w') as f:
	for i in symbolTable:
		f.write(i+' '+ regAddress(symbolTable[i][0])+' '+regAddress(symbolTable[i][1]))




# PASS TWO

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		pass

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
	if (name in pseudoOpcodes):
		return True
	try:
		tmp = symbolTable[name]
		return True
	except:
		return False

def registerAddress(reg):
	reg = reg[1:]
	reg = bin(int(reg))[2:]
	reg = '0'*(6-len(reg))+reg
	return reg

def byteCodeFunc(opcode,addressMode,operand):
	return opcode+' '+addressMode+' '+operand

def isOperandImmediate(operand):
	if('#' in operand):
		return True
	else:
		return False

def isOperandLiteral(operand):
	try:
		tmp=literalTable[operand]
		return True
	except:
		return False

def isOperandSymbol(operand):
	try:
		tmp=symbolTable[operand]
		return True
	except:
		return False

def isOperandLabel(operand):
	try:
		tmp=labelTable[operand]
		return True
	except:
		return False

def isOperandRegister(operand):
	if(operand[0]=='R' or operand[0]=='r'):
		return True
	else:
		return False

def checkIllegalOpcode(opcode):
	if(opcode not in opcodeSymbol):
		print(opcode + ' is an ILLEGAL Opcode')
		return True
	return False

def checkforCLAandSTP(opcode):
	if(opcode == 'STP'):
		global endFlag
		endFlag=True
		return True
	if(opcode == 'CLA'):
		return True
	return False

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		for line in fr:
			if(line == ''):
				continue
			#check for comment line
			elif (line[0]=='@'):
				continue
			elif (line[0]=='*'):
				continue
			else:
				tmp = line.split()
				#check for label line
				if(':' in tmp[0]):
					tmp[0]=tmp[1]
					tmp[1]=tmp[2]
					# del tmp[2] because comparing length of tmp later
					del tmp[2]
				#check for directive statement
				if(check(tmp[0])):
					continue
				else:
					if(checkIllegalOpcode(tmp[0])):
						errorFlag=True
					if(len(tmp)==1):
						# length = 1 for CLA and STP only
						if(checkforCLAandSTP(tmp[0])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00','000000')
						else:
							print(tmp[0] + ' requires 1 Operand')
							errorFlag=True
					else:
						if(len(tmp)!=2):
							print("Too many operand(s) for "+tmp[0])
							errorFlag=True

						if(checkforCLAandSTP(tmp[0])):
							print(tmp[0] + ' requires 0 Operands')
							errorFlag=True

						if(isOperandLiteral(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',literalTable[tmp[1]])
						elif(isOperandLabel(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',labelTable[tmp[1]])
						elif(isOperandImmediate(tmp[1])):
							immediateValue=int(tmp[1][1:])
							if(tmp[0]=='DIV' and immediateValue==0):
								print('Zero Division Error')
								errorFlag=True
							else:
								byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00',registerAddress('R'+str(immediateValue)))
						elif(isOperandRegister(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'10',registerAddress(tmp[1]))
						elif(isOperandSymbol(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',symbolTable[tmp[1]][1])
						else:
							continue

					if(errorFlag):
						global bytecode

						byteCode = ' '
						errorFlag=False

					fw.write(byteCode+'\n')
					
if(endFlag == False):
	print('END statement missing. Use STP as well')
