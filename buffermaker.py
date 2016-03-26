# buffer calculator

from Tkinter import *
from tkFileDialog import askopenfile
import csv
root = Tk()

global lst; resolution = 0.0
settings = {}
lst = [] 
valsave = []
lstsave = []
templist = []


# function to clear the list
def clear():
    for elem in range(len(lst)):
        lst.pop()
    templist = []
    listcatenate()
    textmsg()

def removeselect():
    if len(lst) == 0:
        pass
    else:
        index = int(entry9.get())-1
        del lst[index]
        listcatenate()
        textmsg()

def balanceres():
    global resolution
    resolution = float(entry8.get())
    
# function to save inputs from the user 
def fetchfromuser():
    entries = [entry1, entry2, entry3, entry4, entry5, entry6, entry7]
    temp = [];
    for i in range(len(entries)):
            if i == 0:
                temp.append(entries[i].get())
            elif i>0 and entries[i].get() is "":
                temp.append(None)
            else:
                temp.append(float(entries[i].get()))
    lst.append(temp)
    for ind in range(len(entries)):
        if ind is not 3:
            entries[ind].delete(0,END)
            
    listcatenate()
    textmsg()
    
# function to remove the last entry 
def eraselastentry():
    if len(lst) == 0:
        pass
    else:
        lst.pop()
        listcatenate()
        textmsg()

def disablebox(ent,var):
    for i in ent:
        if var.get() == 1:
            i.delete(0,END)
            i.configure(state='disabled')
        else:
            i.configure(state='normal')

def listcatenate():
    global templist;
    templist = []
    string = ['chemical name', 'molar mass', 'target concentration',
              'target volume','known dilution', 'stock concentration', 'stock volume']
    for i in range(len(lst)):
        tempsave = []
        for j in range(len(lst[i])):
            if (lst[i][j] is not None):
                tempsave.append((string[j],lst[i][j]))
        templist.append(tempsave)
        
# function to display message
def textmsg():
    text_widget = Text(root)

    scrollbar = Scrollbar(root)
    scrollbar.grid(row=12, column = 2)

    stri = ""       
    for i in range(len(templist)):
        if i > 0:
            stri += '\n'
        for j in range(len(templist[i])):
            stri += str(templist[i][j][0]) + ' : ' + str(templist[i][j][1]) + "\n"        
    text_widget.insert('1.0',stri)
    text_widget.grid(row = 12, column = 1)

    scrollbar.config(command = text_widget.yview)
        
# function to compute
def compute():
    if len(lst) == 0:
        pass
    else:
        global lstsave; lstsave = []
        global valsave; valsave = []
        vari = [0.0]*7; vari[4] = 0.1
        ic = True;
        lc = False;
        for index in range(len(lst))[::-1]:
            for j in range(len(lst[index])):
                vari[j] = lst[index][j]
        
            if vari[4] is not None: #  for case when dilution is known
                lstsave.append(str(vari[3]/vari[4]) + " mL of " + vari[0])
                valsave.append(vari[3]/vari[4])

            elif vari[5] is not None and vari[6] is None: # for case when stock concentration of liquid is known
                lstsave.append(str((vari[3]/vari[5])*vari[2]) + " mL from a stock solution of " + str(vari[5]) + " M " + vari[0])
                valsave.append((vari[3]/vari[5])*vari[2])

            elif vari[1] is not None and vari[6] is None: # case when powder is added
                lc = True;
                solidmass = vari[1]*vari[2]/1000.0*vari[3];

                if solidmass*1000 < resolution:
                    del lst[index]
                    lstsave.append("###### difficult to measure, make a stock solution for " + vari[0] + " ######")
                    ic = False
                else:  
                    lstsave.append(str(solidmass) + " g or " + str(solidmass *1000)
                               + " mg of " + str(vari[0]))

            elif vari[1] is not None and vari[6] is not None: # case when stock solution is involved
                solidmass = vari[5]*vari[1]/1000.0*vari[6];
            
                if solidmass*1000 < resolution:
                    del lst[index]
                    lstsave.append("###### difficult to measure, make a stock solution for " + vari[0] + " ######")
                    ic = False
                
                else:  
                    lstsave.append(str(vari[3]/vari[5]*vari[2]) + " mL from a stock solution of "
                               + str(vari[5]) + " M " + str(vari[0]))
                    valsave.append(vari[3]/vari[5]*vari[2])
        if ic and not(lc):
            lstsave.append(str(vari[3] - sum(valsave)) + " mL of DI water")
        elif ic and lc:
            lstsave.append("make final volume to " + str(vari[3])  + " mL with DI water")
            
        updatetextmsg()

def viewlist():
    listcatenate()
    textmsg()

def updatetextmsg():
    text_widget = Text(root)
    stri = "below is what you need to add:\n\n"
    for i in range(len(lstsave)):
        stri += str(lstsave[i])+'\n'        
    text_widget.insert('1.0',stri)
    text_widget.grid(row = 12, column = 1)
    text_widget.configure(bg = "black",fg="green")

def load_settings():
    file_path = askopenfile(filetypes=[("Text files","*.txt")])
    f = file_path.read()
    file_path.close()

    f = f.split()
    global settings
    settings = {}
    for element in range(len(f)/2):
        settings[f[element*2]] = (f[element*2],float(f[element*2+1]))

    create_dropdown(root,settings)

va = StringVar(root)
       
def create_dropdown(root, settings):
    keys = settings.keys()
    va.set(settings[keys[0]])
    option = OptionMenu(root, va, *[settings[keys] for keys in keys])
    option.grid(row = 1, column = 1)
    va.trace("w",update_options)  

def update_options(*args):
    entry = va.get().translate(None,"(,)''").partition(" ")
    entry1.delete(0,END)
    entry1.insert(0,entry[0])
    entry2.delete(0,END)
    entry2.insert(0,entry[-1])

### all labels and entries go here

label_0 = Label(root, text = "The Kornberg Lab buffer maker v.1.0", fg = "blue", font = ("Helvetica",12))
label_0.grid(row = 0, column = 1)


class Labels(object):
    def __init__(self, root, txt, r, c):
        self.root = root
        self.text = txt
        self.r = r
        self.c = c

    def label(self):
        item = Label(self.root, text = self.text)
        item.grid(row=self.r,sticky=E)

    def entry(self):
        item2= Entry(self.root)
        item2.grid(row = self.r, column = self.c)
        return item2

# LABELS
        
label_1=Labels(root,"chemical name",3,1)
label_1.label()
entry1 = label_1.entry()

label_2 = Labels(root,"molar mass (g/mol)", 4, 1)
label_2.label()
entry2 = label_2.entry()

label_3 = Labels(root, "specie concentration (M)",5,1)
label_3.label()
entry3 = label_3.entry()

label_4 = Labels(root, "buffer volume (mL)",6,1)
label_4.label()
entry4 = label_4.entry()

label_5 = Labels(root, "known dilution (X)",7,1)
label_5.label()
entry5 = label_5.entry()

label_6 = Labels(root, "stock concentration (M)",8,1)
label_6.label()
entry6 = label_6.entry()

label_7 = Labels(root, "stock volume (mL)",9,1)
label_7.label()
entry7 = label_7.entry()

            
# CHECKBOXES

#solid checkbox
ent = [entry5,entry6,entry7]
var = IntVar()
solidcheck = Checkbutton(root, text = "solid",command= lambda e = ent, v = var : disablebox(e,v), variable=var)
solidcheck.grid(row=10)

# liquid unknown dilution checkbox
ent = [entry2, entry5, entry7]
var = IntVar()
liquidcheck = Checkbutton(root, text = "liquid", command = lambda e = ent, v = var : disablebox(e,v), variable=var)
liquidcheck.grid(row=10, column = 1)

# liquid known dilution checkbox
ent = [entry2, entry3, entry6, entry7]
var = IntVar()
liquidcheck = Checkbutton(root, text = "liquid (known dilution)", command = lambda e = ent, v = var : disablebox(e,v), variable=var)
liquidcheck.grid(row=10, column = 2)

# make stock checkbox
ent = [entry5]
var = IntVar()
makestockcheck = Checkbutton(root, text = "make stock",command= lambda e = ent, v = var : disablebox(e,v), variable=var)
makestockcheck.grid(row=10, column = 3)

# BUTTONS

class buttons(object):
    def __init__(self, root, text, func, fgcol,bgcol, row, col,entc):
        self.root = root
        self.text = text
        self.func = func
        self.fgcolour = fgcol
        self.bgcolour = bgcol
        self.r = row
        self.c = col
        self.entc = entc
    def createent(self):
        ent =Entry(self.root)
        ent.grid(row = self.r,column = self.entc)
        return ent
    def createbutton(self):
        button = Button(self.root, text = self.text, command = self.func, fg = self.fgcolour, bg=self.bgcolour)
        button.grid(row = self.r, column = self.c)
        return button
        

# save user inputs into the list
save = buttons(root, "save entries", fetchfromuser, "darkgreen","white",8,2,None)
save.createbutton()

# balance resolution
resbutton = buttons(root, "balance resolution (mg)", balanceres, "yellow", "black",1,3,4)
entry8 = resbutton.createent()
resbutton.createbutton()

# remove select entry
removesel = buttons(root, "remove selection", removeselect,  'red','white',5,2,3)
entry9 = removesel.createent()
removesel.createbutton()

# clear all the data in the list
clear = buttons(root, "clear all", clear, 'red','white',4,3,None)
clear.createbutton()

# remove last entry in the list
erase = buttons(root, "remove last entry", eraselastentry,'red', 'white',4,2,None)
erase.createbutton()

# compute result
compute = buttons(root, "calculate", compute, 'blue', 'white',8,3,None)
compute.createbutton()

# load file
load = buttons(root, "load file", load_settings,  'cyan','black', 1,0,None)
load.createbutton()

# view list
view = buttons(root, "view list", viewlist, 'brown', 'white',1,2,None)
view.createbutton()

root.mainloop()
