import sqlite3
from tkinter import *
from tkinter.font import Font
root = Tk()

conn = sqlite3.connect("Benchmarks.db")
cursor = conn.cursor()

root.wm_title("ESOL Curriculum Framework Benchmark Browser")

root.config(bg='lightgray')

root.resizable(0,0)

#-----------Start Menubar Code--------------------------------------
def onExit():
    root.destroy()

def about():
    toplevel = Toplevel(background='lightgray')
    toplevel.resizable(0,0)
    aboutMsg = '''Hello! This program was created by Taylor A. Liss with help from Steve Seeley! It uses the Massachusetts Adult Basic Education Curriculum Framework for English Speakers of Other Languages found at:
    
               http://www.doe.mass.edu/acls/frameworks/frameworks.html
    
Please Note: This program is not perfect. Due to software limitations, this program is unable to correctly show emphasis via underlining and italics as found in the original PDF document. This is most apparent in benchmarks like S2.4d and R3.4b. This should prove to be no major problem for most instructors that are familiar with the framework, but it is important to note nonetheless. \n Thank you for using my first program! I hope it proves useful for you in your lesson planning!

                        Version 1.0 ©2015 by Taylor A. Liss

                              tayloraliss@gmail.com'''
    popup = Text(toplevel, height=17, background='lightgray', wrap=WORD, relief=FLAT)
    popup.pack(padx=(20,20), pady=(20,20))
    popup.insert(END, aboutMsg)
    aboutButton = Button(toplevel, text="Ok", bg="lightgray", command=lambda: toplevel.destroy())
    aboutButton.pack(ipadx=10, pady=(0,10))
    
menubar = Menu(root)
root.config(menu=menubar)
        
fileMenu = Menu(menubar)
fileMenu.add_command(label="Exit", command=onExit)
menubar.add_cascade(label="File", menu=fileMenu)

helpMenu = Menu(menubar)
helpMenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=helpMenu)
#-----------End Menubar Code---------------------------------------

def someFunction(*args):
    listSelector.delete(0, END)
    benchmarkPreview.config(state=NORMAL)
    benchmarkPreview.delete(0.0, END)

    #checkBoxList is a list of lists. The inner lists look like this: ['lStrand1', lStrandSpin1, lStrandSpin4, 'Listening', 1]
    rowCount = 1
    
    for item in checkBoxList:
    
        if checkBoxDict[item[0]].get() == 1: #if the checkbox is checked...
            
            item[1].config(state = NORMAL) #Enable access to spinboxes
            item[2].config(state = NORMAL)
            
            #-----Get value of spinbox ---------------
            x = item[1].get()
            y = item[2].get()
            
            if x == '0-1':
                x = 1
            if y == '0-1':
                y = 1
            
            x = int(x)
            y = int(y)
            
            if x > y:
                x, y = y, x
            #------------------------------------------

            myRange = []
            
            
            
            for num in range(x,y+1):
                myRange.append(num)
            
            for value in myRange:

                #This code makes the listSelector listbox
                query = "SELECT SUBSTR (Benchmark, 1, 5) FROM benchmarks  WHERE Strand is \'%s\' AND Standard is %i AND Level is %s;" % (item[3], item[4], value)
                for row in cursor.execute(query):
                    listSelector.insert(END, str(row[0])) #str(row[0]) prints tuple without brackets
                
                #This code makes the benchmarkPreview textbox
                query2 =  "SELECT benchmark FROM benchmarks WHERE Strand is \'%s\' AND Standard is %i AND Level is %s" % (item[3], item[4], value)
                for row in cursor.execute(query2):
                    benchmarkPreview.insert(END, str(row[0]))
                    benchmarkPreview.insert(END, '\n')
                    benchmarkPreview.tag_config('colorize', background='lightblue', font=('Calibri', '10', 'bold'))
                    benchmarkPreview.tag_add('colorize', '%i.0' % rowCount, '%i.5' % rowCount) 
                    rowCount += 1
                    
        else:
            item[1].config(state = DISABLED) #Disable access to spinboxes
            item[2].config(state = DISABLED)
    benchmarkPreview.config(state=DISABLED)
            
checkBoxDict = {}
            
def createStrandBox(location, name, display):
    var = IntVar(root)
    var.trace('w', someFunction)
    checkbox = Checkbutton(location, text=display, variable=var, bg='lightgray')   
    checkBoxDict[name] = var
    return checkbox

def createSpinbox(location):
    var = IntVar(root)
    var.trace('w', someFunction)
    spinbox = Spinbox(location, width=5, command=someFunction, values=('0-1', 2, 3, 4, 5, 6), font=Font(size=16))
    return spinbox

def createToLabel(location):
    toLabel = Label(location, bg='lightgray', text='to')
    return toLabel
    
def createSeparator(location):
    separator = Frame(location, width=2, bd=1, bg='darkgray', relief=SUNKEN)
    return separator
    
def display():
    selection = listSelector.get(listSelector.curselection())
    notice = (selection)
    query =  "SELECT Benchmark from benchmarks WHERE Benchmark LIKE '%s%%';" % (notice)
    for row in cursor.execute(query):
        selectedText.insert(END, str(row[0]))
        selectedText.insert(END, '\n')

boxHolder1 = Frame(root, bg='lightgray')
boxHolder1.grid(row=0, column=0, padx=(10,0), sticky=N)
    
box1 = Frame(boxHolder1, bg='lightgray')
box1.grid(row=0, column=0, pady=(10,0))

box2 = Frame(boxHolder1, bg='lightgray')
box2.grid(row=1, column=0, pady=(10,0))

box3 = Frame(boxHolder1, bg='lightgray')
box3.grid(row=2, column=0, pady=(10,0))

box4 = Frame(boxHolder1, bg='lightgray')
box4.grid(row=3, column=0, pady=(10,0))
    
lSPLLevels = Label(box1, bg='lightgray', text='SPL Levels') #SPL Levels
lSPLLevels.grid(row=1, column=1, columnspan=3)

lStrandCheck1 = createStrandBox(box1, 'lStrand1', 'Strand 1') #Strand 1
lStrandCheck1.grid(row=2, column=0)
lStrandCheck2 = createStrandBox(box1, 'lStrand2', 'Strand 2') #Strand 2
lStrandCheck2.grid(row=3, column=0)
lStrandCheck3 = createStrandBox(box1, 'lStrand3', 'Strand 3') #Strand 3
lStrandCheck3.grid(row=4, column=0)

lStrandSpin1 = createSpinbox(box1) #Spinbox 1
lStrandSpin1.grid(row=2, column=1)
lStrandSpin2 = createSpinbox(box1) #Spinbox 2
lStrandSpin2.grid(row=3, column=1)
lStrandSpin3 = createSpinbox(box1) #Spinbox 3
lStrandSpin3.grid(row=4, column=1)

to1 = createToLabel(box1)
to1.grid(row=2, column=2, padx=(8,8)) #to 1
to2 = createToLabel(box1)       
to2.grid(row=3, column=2, padx=(8,8)) #to 2
to3 = createToLabel(box1)       
to3.grid(row=4, column=2, padx=(8,8)) #to 3

lStrandSpin4 = createSpinbox(box1) #Spinbox 4
lStrandSpin4.grid(row=2, column=3)
lStrandSpin5 = createSpinbox(box1) #Spinbox 5
lStrandSpin5.grid(row=3, column=3)
lStrandSpin6 = createSpinbox(box1) #Spinbox 6
lStrandSpin6.grid(row=4, column=3)

#--Box 2 below--

sSPLLevels = Label(box2, bg='lightgray', text='SPL Levels') #SPL Levels
sSPLLevels.grid(row=1, column=6, columnspan=3)

sStrandCheck1 = createStrandBox(box2, 'sStrand1', 'Strand 1') #Strand 4
sStrandCheck1.grid(row=2, column=5)
sStrandCheck2 = createStrandBox(box2, 'sStrand2', 'Strand 2') #Strand 5
sStrandCheck2.grid(row=3, column=5)
sStrandCheck3 = createStrandBox(box2, 'sStrand3', 'Strand 3') #Strand 6
sStrandCheck3.grid(row=4, column=5)

sStrandSpin1 = createSpinbox(box2) #Spinbox 7
sStrandSpin1.grid(row=2, column=6)
sStrandSpin2 = createSpinbox(box2) #Spinbox 8
sStrandSpin2.grid(row=3, column=6)
sStrandSpin3 = createSpinbox(box2) #Spinbox 9
sStrandSpin3.grid(row=4, column=6)

to4 = createToLabel(box2)
to4.grid(row=2, column=7, padx=(8,8)) #to 4
to5 = createToLabel(box2)       
to5.grid(row=3, column=7, padx=(8,8)) #to 5
to6 = createToLabel(box2)       
to6.grid(row=4, column=7, padx=(8,8)) #to 6

sStrandSpin4 = createSpinbox(box2) #Spinbox 10
sStrandSpin4.grid(row=2, column=8)
sStrandSpin5 = createSpinbox(box2) #Spinbox 11
sStrandSpin5.grid(row=3, column=8)
sStrandSpin6 = createSpinbox(box2) #Spinbox 12
sStrandSpin6.grid(row=4, column=8)

#--Box 3 below--

rSPLLevels = Label(box3, bg='lightgray', text='SPL Levels') #SPL Levels
rSPLLevels.grid(row=1, column=11, columnspan=3)

rStrandCheck1 = createStrandBox(box3, 'rStrand1', 'Strand 1') #Strand 7
rStrandCheck1.grid(row=2, column=10)
rStrandCheck2 = createStrandBox(box3, 'rStrand2', 'Strand 2') #Strand 8
rStrandCheck2.grid(row=3, column=10)
rStrandCheck3 = createStrandBox(box3, 'rStrand3', 'Strand 3') #Strand 9
rStrandCheck3.grid(row=4, column=10)

rStrandSpin1 = createSpinbox(box3) #Spinbox 13
rStrandSpin1.grid(row=2, column=11)
rStrandSpin2 = createSpinbox(box3) #Spinbox 14
rStrandSpin2.grid(row=3, column=11)
rStrandSpin3 = createSpinbox(box3) #Spinbox 15
rStrandSpin3.grid(row=4, column=11)

to7 = createToLabel(box3)
to7.grid(row=2, column=12, padx=(8,8)) #to 4
to8 = createToLabel(box3)        
to8.grid(row=3, column=12, padx=(8,8)) #to 5
to9 = createToLabel(box3)        
to9.grid(row=4, column=12, padx=(8,8)) #to 6

rStrandSpin4 = createSpinbox(box3) #Spinbox 16
rStrandSpin4.grid(row=2, column=13)
rStrandSpin5 = createSpinbox(box3) #Spinbox 17
rStrandSpin5.grid(row=3, column=13)
rStrandSpin6 = createSpinbox(box3) #Spinbox 18
rStrandSpin6.grid(row=4, column=13)

#--Box 4 below--

wSPLLevels = Label(box4, bg='lightgray', text='SPL Levels') #SPL Levels
wSPLLevels.grid(row=1, column=16, columnspan=3)

wStrandCheck1 = createStrandBox(box4, 'wStrand1', 'Strand 1') #Strand 10
wStrandCheck1.grid(row=2, column=15)
wStrandCheck2 = createStrandBox(box4, 'wStrand2', 'Strand 2') #Strand 11
wStrandCheck2.grid(row=3, column=15)
wStrandCheck3 = createStrandBox(box4, 'wStrand3', 'Strand 3') #Strand 12
wStrandCheck3.grid(row=4, column=15)

wStrandSpin1 = createSpinbox(box4) #Spinbox 13
wStrandSpin1.grid(row=2, column=16)
wStrandSpin2 = createSpinbox(box4) #Spinbox 14
wStrandSpin2.grid(row=3, column=16)
wStrandSpin3 = createSpinbox(box4) #Spinbox 15
wStrandSpin3.grid(row=4, column=16)

to10 = createToLabel(box4)
to10.grid(row=2, column=17, padx=(8,8)) #to 4
to11 = createToLabel(box4)        
to11.grid(row=3, column=17, padx=(8,8)) #to 5
to12 = createToLabel(box4)        
to12.grid(row=4, column=17, padx=(8,8)) #to 6

wStrandSpin4 = createSpinbox(box4) #Spinbox 16
wStrandSpin4.grid(row=2, column=18)
wStrandSpin5 = createSpinbox(box4) #Spinbox 17
wStrandSpin5.grid(row=3, column=18)
wStrandSpin6 = createSpinbox(box4) #Spinbox 18
wStrandSpin6.grid(row=4, column=18)

#-------------------------------------------------------

                #Variable              Spinboxes          Strand     Standard
checkBoxList = [['lStrand1', lStrandSpin1, lStrandSpin4, 'Listening', 1],
                ['lStrand2', lStrandSpin2, lStrandSpin5, 'Listening', 2],
                ['lStrand3', lStrandSpin3, lStrandSpin6, 'Listening', 3],
                                                         
                ['sStrand1', sStrandSpin1, sStrandSpin4, 'Speaking', 1],
                ['sStrand2', sStrandSpin2, sStrandSpin5, 'Speaking', 2],
                ['sStrand3', sStrandSpin3, sStrandSpin6, 'Speaking', 3],
                                                         
                ['rStrand1', rStrandSpin1, rStrandSpin4, 'Reading', 1],
                ['rStrand2', rStrandSpin2, rStrandSpin5, 'Reading', 2],
                ['rStrand3', rStrandSpin3, rStrandSpin6, 'Reading', 3],
                                                         
                ['wStrand1', wStrandSpin1, wStrandSpin4, 'Writing', 1],
                ['wStrand2', wStrandSpin2, wStrandSpin5, 'Writing', 2],
                ['wStrand3', wStrandSpin3, wStrandSpin6, 'Writing', 3]]
				
#------------code for select all checkboxes-----------

listeningChecks = [lStrandCheck1, lStrandCheck2, lStrandCheck3]
listeningStartSpins = [lStrandSpin1, lStrandSpin2, lStrandSpin3]
listeningEndSpins = [lStrandSpin4, lStrandSpin5, lStrandSpin6]

speakingChecks = [sStrandCheck1, sStrandCheck2, sStrandCheck3]
speakingStartSpins = [sStrandSpin1, sStrandSpin2, sStrandSpin3]
speakingEndSpins = [sStrandSpin4, sStrandSpin5, sStrandSpin6]

readingChecks = [rStrandCheck1, rStrandCheck2, rStrandCheck3]
readingStartSpins = [rStrandSpin1, rStrandSpin2, rStrandSpin3]
readingEndSpins = [rStrandSpin4, rStrandSpin5, rStrandSpin6]

writingChecks = [wStrandCheck1, wStrandCheck2, wStrandCheck3]
writingStartSpins = [wStrandSpin1, wStrandSpin2, wStrandSpin3]
writingEndSpins = [wStrandSpin4, wStrandSpin5, wStrandSpin6]

def selectAll(checks, startSpins, endSpins):
    for box in checks:
        box.select()
    for wheel in startSpins:
        wheel.delete(0,"end")
        wheel.insert(0,'0-1')
    for wheel in endSpins:
        wheel.delete(0,"end")
        wheel.insert(0,6)
    someFunction()

#Note: a lambda must be used for the following commands due to tkinter being unable to pass an argument with a function.
#See: http://effbot.org/zone/tkinter-callbacks.htm
listeningCheck = Button(box1, text='Select All Listening', bg='lightgray', command=lambda: selectAll(listeningChecks, listeningStartSpins, listeningEndSpins))
listeningCheck.grid(row=0, column=0, columnspan=1, pady=(10,0))

speakingCheck = Button(box2,bg='lightgray', text='Select All Speaking', command=lambda: selectAll(speakingChecks, speakingStartSpins, speakingEndSpins)) #Speaking
speakingCheck.grid(row=0, column=5, pady=(10,0))

readingCheck = Button(box3,bg='lightgray', text='Select All Reading', command=lambda: selectAll(readingChecks, readingStartSpins, readingEndSpins)) #Reading
readingCheck.grid(row=0, column=10, pady=(10,0))

writingCheck = Button(box4,bg='lightgray', text='Select All Writing', command=lambda: selectAll(writingChecks, writingStartSpins, writingEndSpins)) #Writing
writingCheck.grid(row=0, column=15, pady=(10,0))

#------------end of code for select all checkboxes-----------

previewBox = Frame(root, bg='lightgray')
previewBox.grid(row=0, column=1, pady=(10,0), padx=(30,10), sticky=N)
                
preview = Label(previewBox, bg='lightgray', text='Benchmark Preview') #Benchmark Preview Label
preview.grid(row=0, column=0, sticky=W)

# benchmarkPreview = Listbox(previewBox, selectmode=SINGLE, width=75, height=17) #Benchmark Preview Window
# benchmarkPreview.grid(row=1, column=0)

benchmarkPreview = Text(previewBox, width=75, height=17, wrap=WORD) #Benchmark Preview Window
benchmarkPreview.grid(row=1, column=0)

listSelectorLabel = Label(previewBox, text="Select Benchmark", bg='lightgray')
listSelectorLabel.grid(row=0, column=1, padx=(20,0), sticky=W)

listSelector = Listbox(previewBox, height=17)
listSelector.grid(row=1, column=1, padx=(20,0))

selectButton = Button(previewBox, font=Font(size=16), text='Select', command=display, bg="#FF4545", activebackground="#FF8F8F") #Select -> Button
selectButton.grid(row=2, column=1, padx=(15,0), pady=(15,0))

selected = Label(previewBox, bg='lightgray', text='Selected Benchmarks') #Selected Benchmarks Label
selected.grid(row=3, column=0, columnspan=2, sticky=W)

selectedText = Text(previewBox, height=10, width=75, wrap=WORD) #Selected Text Window
selectedText.grid(row=4, column=0, columnspan=2, sticky=E+W)

buttonBox = Frame(previewBox, bg='lightgray')
buttonBox.grid(row=5, column=0, columnspan=2, pady=15)

def copy():
    root.clipboard_clear()
    text = selectedText.get(0.0, END)
    root.clipboard_append(text)
    
copyButton = Button(buttonBox, text='Copy', font=Font(size=16), command=copy, bg="#85E085", activebackground="#DAF6DA")
copyButton.grid(row=0, column=0, padx=(0,15))

def clearText():
    selectedText.config(state=NORMAL)
    selectedText.delete(0.0, END)

clearButton = Button(buttonBox, text='Clear', font=Font(size=16), command=clearText, bg="#FFFF66", activebackground="#FFFFD1")
clearButton.grid(row=0, column=1)

someFunction()

mainloop()