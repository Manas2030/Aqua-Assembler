# ASSMEMBLER PROJECT

#Initializations
opcodeSymbol = {}
locationCount=0

with open('opcodeSymbolTable.txt','r') as f:
	for line in f:
		tmp=line.split()
		opcodeSymbol[tmp[0]]=tmp[1]

with open('sourceCode.txt','r') as fr:
	with open('machineCode.txt','w') as fw:
		pass

print(opcodeSymbol)