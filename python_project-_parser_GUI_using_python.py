from tkinter import *
import re
#global Variables
lineIndex = 0
i = 0
list=[]
myTokens = []

class MyFirstGUI:
    
    def __init__(self, root):
        # Master is the default prarent object of all widgets.
        # You can think of it as the window that pops up when you run the GUI code.
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")
        self.master.geometry('1290x450')
        
        # creates a text box for source code input
        self.label = Label(self.master, text="Source Code Input: ")
        self.label.grid(row=0, column=0)
        self.sourceCodeInput = Text(self.master, width=60, height=25, bd=1, relief="groove")
        self.sourceCodeInput.grid(row=1, column=0, sticky=E, padx=5)
        
        # creates a text box for Lexical analyzed result
        self.label = Label(self.master, text="Tokens:")
        self.label.grid(row=0, column=2)
        self.lar = Text(self.master, width=60, height=25, bd=1, relief="groove")
        self.lar.grid(row=1, column=2, sticky=E, padx=5)

                 # creates a text box for parser tree
        self.label = Label(self.master, text="Parser Tree: ")
        self.label.grid(row=0, column=3)
        self.parsertree = Text(self.master, width=60, height=25, bd=1, relief="groove")
        self.parsertree.grid(row=1, column=3, sticky=E, padx=5)
        
        # creates a current processing line holder
        self.label = Label(self.master, text="Current Processing Line: ")
        self.label.grid(row=3, column=0, sticky=W, padx=50)
        self.line = Entry(self.master, width=1)  # , width=4, height=2,bd=2, insertborderwidth=2, relief="groove")
        self.line.grid(row=3, column=0)
        
        # quit button
        self.quit = Button(self.master, text="Quit", command=self.quit)
        self.quit.grid(row=3, column=2)
        
        
        # create a next line button that would jump to the next line when clicked
        self.nextLine = Button(self.master, text="Next Line", command=self.next_line)
        self.nextLine.grid(row=4, column=0)
    
         
    
    def next_line(self):
        global lineIndex
        global i
        
        string = self.sourceCodeInput.get('1.0', 'end').split('\n')
        list.append(string[i])
        print(list)
    
        for line in list:
            l = len(line)
            result = l
            
            
            while  result > 0:
            
                keyword = re.match(r'(^if|^else|^int|^float|^print)', line)  # if  else    int float
                id = re.match(r'^[A-Z]+[0-9]+|^[a-z]+[0-9]+', line)  # letters, or letters followed by digits
                operator = re.match(r'^(=|\*|>|\+)', line)  # = +   >   *
                separators = re.match(r'^(\(|\)|\:|["]|\;)', line)
                int_literal = re.match(r'^\d+', line)  # only integers
                float_literal = re.match(r'^\d+\.\d+', line)  # only floats
                string_literal = re.match(r'[A-Z\s]+[a-z\s]+|[a-z\s]+', line)  # only lines
                space = re.match(r'\s+', line)
                if(space != None):
                    line = line[space.end():]
                    result = len(line)
                elif(keyword != None):
                    self.lar.insert('end', "<keyword," + keyword.group(0) + ">" + '\n')
                    myTokens.append("keyword")
                    myTokens.append(keyword.group(0))
                    line = line[keyword.end():]
                    result = len(line)
                elif (id != None):
                    self.lar.insert('end',"<id,"+ id.group(0) + ">" + '\n')
                    myTokens.append("id")
                    myTokens.append(id.group(0))
                    line = line[id.end():]
                    result = len(line)
                elif (operator != None):
                    self.lar.insert('end',"<op," + operator.group(0) + ">" + '\n')
                    line = line[operator.end():]
                    myTokens.append("op")
                    myTokens.append(operator.group(0))
                    result = len(line)
                elif (separators != None):
                    self.lar.insert('end',"<sep," + separators.group(0) + ">" + '\n')
                    line = line[separators.end():]
                    myTokens.append("sep")
                    myTokens.append(separators.group(0))
                    result = len(line)
                elif (float_literal != None):
                    self.lar.insert('end',"<float_lit," + float_literal.group(0) + ">" + '\n')
                    line = line[float_literal.end():]
                    myTokens.append("float_lit")
                    myTokens.append(float_literal.group(0))
                    result = len(line)
                elif (int_literal != None):
                    self.lar.insert('end',"<int_lit," + int_literal.group(0) + ">" + '\n')
                    line = line[int_literal.end():]
                    myTokens.append("int_lit")
                    myTokens.append(int_literal.group(0))
                    result = len(line)
                elif (string_literal != None):
                    self.lar.insert('end',"<string_lit," + string_literal.group(0) + ">" + '\n')
                    line = line[string_literal.end():]
                    myTokens.append("string_lit")
                    myTokens.append(string_literal.group(0))
                    result = len(line)
            
            self.parser()
            #for loop only reads the first element in the list so pop each time the tokens are printed out
            list.pop(0)
            break
        
        # clearing the processing line text box
        self.line.delete(0, 'end')
        # inserting the current line value
        self.line.insert('end', lineIndex + 1)
        lineIndex += 1
        #index for which line i want to read
        i +=1
        
        
    # handling the action on cicking quit button
    # closes the app
    def quit(self):
        self.master.quit()

    def accept_token(self):
        self.parsertree.insert('end',"     accept token from the list: " + myTokens[1] + '\n')
        myTokens.pop(0)
        myTokens.pop(0)
    def multi(self):
        self.parsertree.insert('end',"\n----parent node multi, finding children nodes:" + '\n')
    
        if (myTokens[0] == "float_lit"):
            self.parsertree.insert('end',"child node (internal): float"+ '\n')
            self.parsertree.insert('end',"   float has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
        elif (myTokens[0] == "int_lit"):
            self.parsertree.insert('end',"child node (internal): int"+ '\n')
            self.parsertree.insert('end',"   int has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
            
            if (myTokens[1] == "*"):
                self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
                self.accept_token()
                self.multi()

    def math(self):
        self.parsertree.insert('end',"\n----parent node math, finding children nodes:"+ '\n')
    
        self.multi()
        if (myTokens[1] == "+"):
            self.parsertree.insert('end',"child node (internal): +"+ '\n')
            self.accept_token()

            self.multi()
   

    def if_exp(self):
        self.parsertree.insert('end',"\n----parent node if exp, finding children nodes:"+ '\n')
    
        if (myTokens[1] == "if"):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
        if (myTokens[1] == "("):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
            self.parsertree.insert('end',"Child node (internal): comparisons_exp"+ '\n')
            self.comparison_exp()
        if (myTokens[1] == ")"):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
            
        if (myTokens[0] == "string_lit"):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()

    
            if (myTokens[1] == "("):
                    self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
                    self.accept_token()
            if (myTokens[0] == "sep"):
                    self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
                    self.accept_token()
            self.if_exp()
            
    def comparison_exp(self):
        
        self.parsertree.insert('end',"\n----parent node if comparisons exp, finding children nodes:"+ '\n')
        if (myTokens[0] == "id"):
            self.parsertree.insert('end',"child node (internal): identifer"+ '\n')
            self.parsertree.insert('end',"   identifer has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()

        if (myTokens[1] == ">"):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()

        if (myTokens[0] == "id"):
            self.parsertree.insert('end',"child node (internal): identifer"+ '\n')
            self.parsertree.insert('end',"   identifer has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()

    
    def exp(self):
        self.parsertree.insert('end',"\n----parent node exp, finding children nodes:"+ '\n')
        
        
        if (myTokens[0] == "keyword"):
            self.parsertree.insert('end',"child node (internal): keyword"+ '\n')
            self.parsertree.insert('end',"   keyword has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
        else:
            self.parsertree.insert('end',"expect keyword as the first element of the expression!\n"+ '\n')
            return
        
        if (myTokens[0] == "id"):
            self.parsertree.insert('end',"child node (internal): identifer"+ '\n')
            self.parsertree.insert('end',"   identifer has child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
        else:
            self.parsertree.insert('end',"expect id as the second element of the expression!"+ '\n')
            return
        
        if (myTokens[1] == "="):
            self.parsertree.insert('end',"child node (token): " + myTokens[1]+ '\n')
            self.accept_token()
        else:
            self.parsertree.insert('end',"expect = as the third element of the expression!"+ '\n')
            return
        
        self.parsertree.insert('end',"Child node (internal): math"+ '\n')
        self.math()
    
    def parser(self):
        global lineIndex
        print(lineIndex+1)
        self.parsertree.insert('end',"\n\n####Parse tree for line " + str(lineIndex+1) + "#### \n")
        self.if_exp()
        if (myTokens[1] == ":"):
            self.parsertree.insert('end',"child node (token):" + myTokens[1]+ '\n')
            self.accept_token()
            self.parsertree.insert('end',"\nparse tree building success!"+ '\n')
        elif(myTokens[1] == ";"):
                self.parsertree.insert('end',"child node (token):" + myTokens[1]+ '\n')
                self.accept_token()

                self.parsertree.insert('end',"\nparse tree building success!"+ '\n')
        else:
            self.exp()
            if(myTokens[1] == ";"):
                self.parsertree.insert('end',"child node (token):" + myTokens[1]+ '\n')
                self.accept_token()
                self.parsertree.insert('end',"\nparse tree building success!" + "\n")
        return


            
           

    
    


    





if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()
    