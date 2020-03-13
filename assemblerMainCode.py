# ASSMEMBLER PROJECT

#Initializations
opcodeSymbol = {}
locationCount=0
symbolTable={}
labelTable={}
literalTable={}
pseudoOpcodes=[]
byteCode=''

with open('opcodeSymbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		opcodeSymbol[tmp[0]]=tmp[1]

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		pass

with open ('symbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		symbolTable[tmp[0]]=[[tmp[1],tmp[2]]]

with open ('literalTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		literalTable[tmp[0]]=[[tmp[1],tmp[2]]]

with open('labelTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		labelTable[tmp[0]]=tmp[1]

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		for line in fr:
			#check for comment line
			if (line[0]=='@'):
				pass
			else:
				tmp = line.split()
				#check for label line
				if(':' in tmp[0]):
					tmp[0]=tmp[1]
					tmp[1]=tmp[2]
				#check for directive statement
				if(check(tmp[0])):
					pass
				else:
					if(len(tmp)==1):
						byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00','000000')
					else:
						if(isOperandLiteral(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',literalTable[tmp[1]])
						elif(isOperandLabel(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'01',labelTable[tmp[1]])
						elif(isOperandImmediate(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'00',registerAddress('R'+bin(tmp[1][1:])))
						elif(isOperandRegister(tmp[1])):
							byteCode=byteCodeFunc(opcodeSymbol[tmp[0]],'10',registerAddress(tmp[1]))
						else:
							pass
					fw.write(bytecode+'\n')

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

def byteCodeFunc(four,two,six):
	return four+' '+two+' '+six

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

def isOperandLabel(operand):
	try:
		tmp=labelTable[operand]
		return True
	except:
		return False

def isOperandRegister(operand):
	if('R' in operand):
		return True
	else:
		return False
