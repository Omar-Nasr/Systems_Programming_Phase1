#InstructionSetDefinition
Format3 = {
        "ADD":int("18",16),
        "AND":int("40",16),
        "COMP":int("28",16),
        "DIV":int("24",16),
        "J":int("3C",16),
        "JEQ":int("30",16),
        "JGT":int("34",16),
        "JLT":int("38",16),
        "JSUB":int("48",16),
        "LDA":int("00",16),
        "LDCH":int("50",16),
        "LDL":int("08",16),
        "LDX":int("04",16),
        "MUL":int("20",16),
        "OR":int("44",16),
        "RD":int("D8",16),
        "RSUB":int("4C",16),
        "STA":int("0C",16),
        "STCH":int("54",16),
        "STL":int("14",16),
        "STSW":int("E8",16),
        "STX":int("10",16),
        "SUB":int("1C",16),
        "TD":int("E0",16),
        "TIX":int("2C",16),
        "WD":int("DC",16)
        }
Format1 = {
        "FIX":int("C4",16),
        "FLOAT":int("C0",16),
        "HIO":int("F4",16),
        "NORM":int("C8",16),
        "SIO":int("F0",16),
        "TIO":int("F8",16),
        }



#intermediatefilecreation
with open("testfile.txt") as f:
    labels = []
    input_instructions = []
    input_arguments = []
    for line in f:
        x = line.split("    ")
        labels.append(x[1].upper())
        input_instructions.append(x[2].upper())
        input_arguments.append(x[3].upper())
with open("intermediatefile.txt","w") as f:
    for i in range(len(input_instructions)):
        f.write(labels[i] + "    " + input_instructions[i] + "    " + input_arguments[i]+"\n")


## Pass 1
Current_Location = int(input_arguments[0],16)

Location_Counter = ['']*len(input_instructions)
Program_Name = labels[0] 
print(Program_Name)
for i in range(1,len(input_instructions)):
    if(input_instructions[i] in Format3):
        Location_Counter[i] = hex(Current_Location)
        Current_Location+=3
    elif input_instructions[i] in Format1:
        Location_Counter[i] = hex(Current_Location)
        Current_Location+=1
    else:
        Location_Counter[i] = ""
Symbol_Table = {}
for i in range(1,len(input_instructions)):
    if(labels[i]!=''):
        Symbol_Table[labels[i]]=Location_Counter[i][2:]

with open("out_pass1.txt","w") as f:
    for i in range(len(input_instructions)):
        f.write(Location_Counter[i][2:] + "    " + labels[i] + "    " + input_instructions[i] + "    " + input_arguments[i]+"\n")
with open("symbTable.txt","w") as f:
    for symbol in Symbol_Table:
        f.write(symbol + "    "+ Symbol_Table[symbol] + "\n")
## Pass 2 
obcode = ['']*len(input_instructions)
for i in range(1,len(input_instructions)):
    if(input_instructions[i] in Format3):
        address = ""
        currentargument = input_arguments[i].split(",")
        op_code = Format3[input_instructions[i]]
        print(op_code)
        if(input_arguments[i][0]=="#"):
            op_code+=1
            address+=hex(int(input_arguments[i][1:]))[2:] 
        else:
            address+=Symbol_Table[currentargument[0]]
        op_code = hex(op_code)[2:]
        while(len(op_code)<2):
            op_code = "0"+op_code
        while(len(address)<4):
            address="0"+address
        ob_code = op_code+address
        print(ob_code)
    if(input_instructions[i] in Format1):
        op_code = Format1[input_instructions[i]]
        op_code = hex(op_code)[2:]
        while(len(op_code)<2):
            op_code = "0"+op_code
        ob_code = op_code
        print(ob_code)





    
