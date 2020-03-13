# ASSMEMBLER PROJECT

#Initializations
opcodeSymbol = {}
locationCount=0
label={}
symbol={}
literal={}
sg = 0;

with open('sourceCode.txt','r') as fr:
	for line in fr:
		tmp = line.split()
		print(tmp)

		#set val of LC
		if(tmp[0]=="START"):
			locationCount = int(tmp[1])

		#check if comment
		elif(tmp[0]=="@"):
			pass
		elif(tmp[0]=="STP"):
			pass

		#check for label
		elif(tmp[0][-1]==":"):
			label[tmp[0]]= bin(locationCount)
		

		#check for symbol
		##decimal
		elif(tmp[min(1,len(tmp)-1)]=="DC"):

			symbol[tmp[0]] = [bin(int(tmp[2][1:-1])),bin(locationCount)]
		
		##hexadecimal
		elif(tmp[min(1,len(tmp)-1)]=="DS"):
			symbol[tmp[0]] = [bin(int(tmp[2][1:-1],16)),bin(locationCount)]
		

		#check for literal
		elif(sg==1):
			if(tmp[min(1,len(tmp)-1)][1]=="h"):
				literal[tmp[1]] = [bin(int(tmp[1][3:-1],16)),bin(locationCount)]
			
			elif(tmp[min(1,len(tmp)-1)][1]=="'" or tmp[min(1,len(tmp)-1)][1]=="d"):
				if(tmp[1][1]=="d"):
					literal[tmp[1]] = [bin(int(tmp[1][3:-1])),bin(locationCount)]
				
				else:
					literal[tmp[1]] = [bin(int(tmp[1][2:-1])),bin(locationCount)]
				
			
			else:
			 sg = 0
			
		
		elif(tmp[0]=="LTORG"):
			sg=1
		
		locationCount = locationCount + 1
print(literal)
print(label)
print(symbol)

def registerAddress(reg):
	reg = reg[2:]
	reg = '0'*(6-len(reg))+reg
	return reg	

with open('labelTable.txt','w') as f:
		for i in label:
			f.write(i+' '+ registerAddress(label[i]))
with open('literalTable.txt','w') as f:
	for i in label:
		f.write(i+' '+ registerAddress(label[i][0])+' '+registerAddress(label[i][1]))
with open('symbolTable.txt','w') as f:
	for i in symbol:
		f.write(i+' '+ registerAddress(symbol[i][0])+' '+registerAddress(symbol[i][1]))
		





