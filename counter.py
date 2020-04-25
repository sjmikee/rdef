import os
counter = 0

list = []

for i in os.listdir():
    if(i.startswith('.')):
        pass
    elif(i.endswith(".rdef")):
        pass
    elif(i.endswith('md')):
        pass
    elif(i.endswith('logs')):
        pass
    elif(i == 'counter.py'):
        pass
    elif(i == '__pycache__'):
        pass
    elif(i.endswith(".py")):
           print(i)
           counter = counter + sum(1 for line in open(os.path.join(os.getcwd(), i)))
    else:
        list.append(i)
    
listtwo = []

for k in list:
    if(k.endswith("rdef")):
        pass
    elif(k.endswith('md')):
        pass
    elif(k == "logs"):
        pass
    elif(k == "resources"):
        pass
    elif(k == "__pycache__"):
        pass
    else:
        listtwo = os.listdir(os.path.join(os.getcwd(), k))
        #print(listtwo, k)

        for z in listtwo:
            if (z == "__pycache__"):
                pass
            elif (z == "logs"):
                pass
            elif(z.endswith(".py")):
                counter = counter + sum(1 for line in open(os.path.join(os.getcwd(),k ,z )))    

print("Amount of rows:",counter)