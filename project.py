#InstructionSetDefinition
import math
import sys
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
OtherInstructions = {
        "WORD",
        "RESW",
        "BYTE",
        "RESB",
        "END",
        "START",

        }



#intermediatefilecreation
def main():
    with open(sys.argv[1]) as f:
        line_numbers = []
        labels = []
        input_instructions = []
        input_arguments = []
        for line in f:
            if(line.replace(" ","")==""):
                continue
            x = line.replace("\n","")
            x = x.split()
            x = " ".join(x)
            x = x.upper()
            x = x.split()
            if(x[1]== "."):
                continue
            line_numbers.append(x[0])
            if(x[1] in Format3 or x[1] in Format1 or x[1] in OtherInstructions):
                labels.append("")
                input_instructions.append(x[1])
                if(x[1] == "RSUB" or x[1] == "END"):
                    input_arguments.append("")
                else:
                    input_arguments.append(x[2])
            elif(x[2] in Format3 or x[2] in Format1 or x[2] in OtherInstructions):
                labels.append(x[1])
                input_instructions.append(x[2])
                if(x[2] == "RSUB"):
                    input_arguments.append("")
                else:
                    input_arguments.append(x[3])
            else:
                print("Syntax Error At Line " + line_numbers[-1])
                return

    with open("intermediatefile.txt","w") as f:
        for i in range(len(input_instructions)):
            f.write(labels[i].ljust(6) + "    " + input_instructions[i].ljust(6) + "    " + input_arguments[i].ljust(6)+"\n")


## Pass 1
    Current_Location = int(input_arguments[0],16)

    Location_Counter = ['']*len(input_instructions)
    Program_Name = labels[0] 
    if(len(Program_Name)>6):
        print(" Syntax Error Program Name is too long")
    for i in range(1,len(input_instructions)):
        if(input_instructions[i]=="END"):
            Location_Counter[i] = hex(Current_Location)
            continue
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
            f.write(Location_Counter[i][2:].ljust(6) + "    " + labels[i].ljust(6) + "    " + input_instructions[i].ljust(6) + "    " + input_arguments[i].ljust(6)+"\n")
    with open("symbTable.txt","w") as f:
        for symbol in Symbol_Table:
            f.write(symbol.ljust(6) + "    "+ Symbol_Table[symbol].ljust(6) + "\n")




    ## Pass 2 
    obcode = ['']*len(input_instructions)
    for i in range(1,len(input_instructions)):
        ob_code = ''
        if(input_instructions[i] in Format3):
            address = ""
            address_hex = 0
            currentargumentwithcomma = input_arguments[i].split(",")
            currentargument = currentargumentwithcomma[0]
            op_code = Format3[input_instructions[i]]
            if(currentargument[0]=="#"):
                op_code+=1
                if(currentargument[1:] in Symbol_Table):
                    address_hex=int(Symbol_Table[currentargument[1:]],16)
                else:
                    address_hex = int(currentargument[1:],10)
            else:
                address_hex=int(Symbol_Table[currentargument],16)
            if(len(currentargumentwithcomma)>1):
                if(currentargumentwithcomma[1]=="X"):
                    address_hex = address_hex + 32768
                else:
                    print("error")
            op_code = hex(op_code)[2:]
            address = hex(address_hex)[2:]
            while(len(op_code)<2):
                op_code = "0"+op_code
            while(len(address)<4):
                address="0"+address
            ob_code = op_code+address

        if(input_instructions[i] in Format1):
            op_code = Format1[input_instructions[i]]
            op_code = hex(op_code)[2:]
            while(len(op_code)<2):
                op_code = "0"+op_code
            ob_code = op_code
        obcode[i] = ob_code
    with open("out_pass2.txt","w") as f:
        for i in range(len(input_instructions)):
            f.write(Location_Counter[i][2:].ljust(6) + "    " + labels[i].ljust(6) + "    " + input_instructions[i].ljust(6) + "    " + input_arguments[i].ljust(6)+"    "+obcode[i].ljust(6)+ "\n")


    #HTE
    with open("HTE.txt","w") as f:
        records = []
        while(len(Program_Name)<6):
            Program_Name = Program_Name+"X"
        Starting_Address = Location_Counter[1][2:]
        while(len(Starting_Address)<6):
            Starting_Address = "0" + Starting_Address
        Ending_Address = Location_Counter[len(Location_Counter)-1][2:]
        Program_Size = int(Ending_Address,16) - int(Starting_Address,16)
        Program_Size = hex(Program_Size)[2:]
        while(len(Program_Size)<6):
            Program_Size = "0" + Program_Size
        records.append("H"+Program_Name+Starting_Address+Program_Size)
        i = 1
        while(i<len(input_instructions)):
            T_Starting_Address = int(Location_Counter[i][2:],16)
            T_Record = ""
            T_Record_Size = 0
            while(T_Record_Size<30):
                if(i==len(input_instructions)):
                    break
                if(obcode[i]==''):
                    i+=1
                    break
                if(T_Record_Size + math.floor(len(obcode[i])/2) <=30):
                    T_Record_Size+=math.floor(len(obcode[i])/2)
                    T_Record+=obcode[i]
                    i+=1
                else:
                    break
            T_Record_Size = hex(T_Record_Size)[2:]
            while(len(T_Record_Size)<2):
                T_Record_Size = "0"+T_Record_Size
            T_Starting_Address = hex(T_Starting_Address)[2:]
            while(len(T_Starting_Address)<6):
                T_Starting_Address = "0"+T_Starting_Address
            records.append("T"+T_Starting_Address+T_Record_Size+T_Record)
        records.append("E"+Starting_Address)
        for i in range(len(records)):
            f.write(records[i]+"\n")
if __name__ == "__main__":
    main()










