#from cgitb import text
from tkinter import *
import re

result = [] #list containg the found tokens
#lineIndex = 0


class MyFirstGui:
    def __init__(self, root):
        
        self.lineIndex = 0
        self.master = root
        #####Title of Widget#####
        self.master.title("Lexical Analyzer for TinyPie")
        self.master.geometry('1290x450')
        #####Displayed text above entry box#####
        self.txtBoxLabel_1 = Label(self.master, text='Source Code Input:')
        self.txtBoxLabel_1.grid(row=0, column=0)
        #####Text box_1#####
        self.txtBox_1 = Text(self.master, width=60, height=25)
        self.txtBox_1.grid(row=1, column=0, sticky=W)
        #####Current Proc. Line text#####
        self.txtProcLine = Label(self.master, text='Current Processing Line: ' + str(self.lineIndex))
        self.txtProcLine.grid(row=2, column=0)
        #####Next Line Button#####
        self.nextLineButton = Button(self.master, text='Next Line', command=self.nextLine)
        self.nextLineButton.grid(row=3, column=0)
        #####Displayed text above tokens box#####
        self.txtBoxLabel_2 = Label(self.master, text='Tokens:')
        self.txtBoxLabel_2.grid(row=0, column=2)
        #####Text box_2#####
        self.txtBox_2 = Text(self.master, width=60, height=25)
        self.txtBox_2.grid(row=1, column=2, sticky=E)
        #####Displayed text above Parse Tree box#####
        self.txtBoxLabel_3 = Label(self.master, text='Parse Tree:')
        self.txtBoxLabel_3.grid(row=0, column=3)
        #####Text box_3#####
        self.txtBox_3 = Text(self.master, width=60, height=25)
        self.txtBox_3.grid(row=1, column=3, sticky=E)
        #####Quit Button#####
        self.quitButton = Button(self.master, text='Quit', command=self.quit)
        self.quitButton.grid(row=3, column=2)


    #####nextLine Function#####
    def nextLine(self):
        global lineIndex
        self.lineIndex = self.lineIndex + 1
        lineInput = self.txtBox_1.get(str(float(self.lineIndex)), str(float(self.lineIndex)) + 'lineend')
        result = self.cutOneLineTokens(lineInput)
        for i in result:
            self.txtBox_2.insert(END, i)
            self.txtBox_2.insert(END, "\n")
            self.txtProcLine.config(text= 'Current Processing Line: ' + str(self.lineIndex))
        self.txtBox_2.insert(END, "\n")
        print(result)
        self.parser()
        print(result)
        


    #####Lexer Function#####
    def cutOneLineTokens(self, input):
        result = [] #list containg the found tokens
        #token dictionary
        tokens = {r'\b(if|else|int|float|^print)(?=\s|\t)': 'keyword',
                    r'([a-zA-Z]+[0-9]+)|[a-zA-Z]+': 'id',
                    r'[=+>*]': 'op',
                    r'^\d+(?![\d+\.])': 'lit',
                    r'\d+\.\d+': 'lit',
                    r'[():\";]': 'sep',
                    r'[\t]+|[ ]+': 'space'}

        tempStr = input
        while len(tempStr) != 0:
            for x in tokens:
                token = re.match(x, tempStr)
                if token:
                    if tokens[x] == 'space': #Remove spacing/tabs
                        pos = token.end()
                        tempStr = tempStr[pos:]
                    elif tokens[x] == 'sep' and tempStr[0] == '\"':
                        result.append('<' + tokens[x] + ',' + token.group() + '>')
                        pos = token.end()
                        tempStr = tempStr[pos:]
                        strRgx = re.match(r'^(.)+?(?=\")', tempStr)
                        if strRgx:
                            result.append('<' + 'lit' + ',' + strRgx.group() + '>')
                            pos = strRgx.end()
                        result.append('<' + tokens[x] + ',' + token.group() + '>')
                        pos += 1
                        tempStr = tempStr[pos:]
                    else:
                        result.append('<' + tokens[x] + ',' + token.group() + '>')
                        pos = token.end()
                        tempStr = tempStr[pos:]
        return result

        
    def math(self):
        self.txtBox_3.insert('end',"\n----parent node math, finding children nodes:"+ '\n')
    
        self.multi()
        if (result[1] == "+"):
            self.txtBox_3.insert('end',"child node (internal): +"+ '\n')
            self.accept_token()

            self.multi()

    def multi(self):
        self.txtBox_3.insert('end',"\n----parent node multi, finding children nodes:" + '\n')
    
        if (result[0] == "float_lit"):
            self.txtBox_3.insert('end',"child node (internal): float"+ '\n')
            self.txtBox_3.insert('end',"   float has child node (token): " + result[1]+ '\n')
            self.accept_token()
        elif (result[0] == "int_lit"):
            self.txtBox_3.insert('end',"child node (internal): int"+ '\n')
            self.txtBox_3.insert('end',"   int has child node (token): " + result[1]+ '\n')
            self.accept_token()
            
            if (result[1] == "*"):
                self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
                self.accept_token()
                self.multi()


    def parser(self):
        #global lineIndex
        print(self.lineIndex+1)
        self.txtBox_3.insert('end',"\n\n####Parse tree for line " + str(self.lineIndex) + "#### \n")
        self.if_exp()
        if (result[1] == ":"):
            self.txtBox_3.insert('end',"child node (token):" + result[1]+ '\n')
            self.accept_token()
            self.txtBox_3.insert('end',"\nparse tree building success!"+ '\n')
        elif(result[1] == ";"):
                self.txtBox_3.insert('end',"child node (token):" + result[1]+ '\n')
                self.accept_token()

                self.txtBox_3.insert('end',"\nparse tree building success!"+ '\n')
        else:
            self.exp()
            if(result[1] == ";"):
                self.txtBox_3.insert('end',"child node (token):" + result[1]+ '\n')
                self.accept_token()
                self.txtBox_3.insert('end',"\nparse tree building success!" + "\n")
        return

    def if_exp(self):
        self.txtBox_3.insert('end',"\n----parent node if exp, finding children nodes:"+ '\n')
    
        if (result[1] == "if"):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()
        if (result[1] == "("):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()
            self.txtBox_3.insert('end',"Child node (internal): comparisons_exp"+ '\n')
            self.comparison_exp()
        if (result[1] == ")"):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()
            
        if (result[0] == "string_lit"):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()

    
            if (result[1] == "("):
                    self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
                    self.accept_token()
            if (result[0] == "sep"):
                    self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
                    self.accept_token()
            self.if_exp()

    def comparison_exp(self):
        
        self.txtBox_3.insert('end',"\n----parent node if comparisons exp, finding children nodes:"+ '\n')
        if (result[0] == "id"):
            self.txtBox_3.insert('end',"child node (internal): identifer"+ '\n')
            self.txtBox_3.insert('end',"   identifer has child node (token): " + result[1]+ '\n')
            self.accept_token()

        if (result[1] == ">"):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()

        if (result[0] == "id"):
            self.txtBox_3.insert('end',"child node (internal): identifer"+ '\n')
            self.txtBox_3.insert('end',"   identifer has child node (token): " + result[1]+ '\n')
            self.accept_token()

    def exp(self):
        self.txtBox_3.insert('end',"\n----parent node exp, finding children nodes:"+ '\n')
        
        
        if (result[0] == "keyword"):
            self.txtBox_3.insert('end',"child node (internal): keyword"+ '\n')
            self.txtBox_3.insert('end',"   keyword has child node (token): " + result[1]+ '\n')
            self.accept_token()
        else:
            self.txtBox_3.insert('end',"expect keyword as the first element of the expression!\n"+ '\n')
            return
        
        if (result[0] == "id"):
            self.txtBox_3.insert('end',"child node (internal): identifer"+ '\n')
            self.txtBox_3.insert('end',"   identifer has child node (token): " + result[1]+ '\n')
            self.accept_token()
        else:
            self.txtBox_3.insert('end',"expect id as the second element of the expression!"+ '\n')
            return
        
        if (result[1] == "="):
            self.txtBox_3.insert('end',"child node (token): " + result[1]+ '\n')
            self.accept_token()
        else:
            self.txtBox_3.insert('end',"expect = as the third element of the expression!"+ '\n')
            return
        
        self.txtBox_3.insert('end',"Child node (internal): math"+ '\n')
        self.math()

    def accept_token(self):
        self.txtBox_3.insert('end',"     accept token from the list: " + result[1] + '\n')
        result.pop(0)
        result.pop(0)


    #####Quit Function#####
    def quit(self):
        root.destroy()



if __name__ == '__main__':
    root = Tk()
    my_gui = MyFirstGui(root)
    root.mainloop()




    #HEJOEJPFOJSFJ