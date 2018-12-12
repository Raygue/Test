from tkinter import *
from tkinter.messagebox import *
import time
import random
   
class gui(Frame):
    
    def __init__ (self, master=None):
        
        super().__init__(master)
        self.masta = master
        self.grid()
        self.create_widget(master)
        
        self.masta.bind('<Escape>', lambda e: self._ask_quit())
        
    def create_widget(self, masta, *args):
        '''makes the widgets'''
        self.masta.title('Stopwatch and Clock')
        self.createbuttons(masta)
        self.createlabel(masta)
        
        self.masta.protocol('WM_DELETE_WINDOW',self._ask_quit)

    def createlabel(self, masta, *args):
        '''makes the label'''
        global alabel

        alabel = Label(masta, text = 'Hello World', width = 30 ,
                       font = 'Helvatica 20 bold')
        alabel.grid(row = 1, column = 1, columnspan = 1)
        self.alabel = alabel

    def createbuttons(self, masta, *args):
        '''makes buttons'''
        stopwatch = Button(masta, text = 'StopWatch',
                                 width = 25, command = self.StopWatch)
        stopwatch.grid(row= 1, column = 2, columnspan = 1, rowspan = 1)
        self.stopwatch = stopwatch

        fun = Button(masta, text = 'Fun',
                                width = 25, command = self.Fun)
        fun.grid(row = 0, column = 0, columnspan = 1, rowspan = 1)
        self.fun = fun

        gethelp = Button(masta, text = 'Help',
                                 width = 25,command = self.Helps)
        gethelp.grid(row = 1, column = 0, columnspan = 1, rowspan = 1)
        self.gethelp = gethelp

        clock = Button(masta, text = 'Clock',
                                 width = 25, command = self.Clock)
        clock.grid(row = 0, column = 2, columnspan = 1, rowspan = 1)
        self.clock = clock

        exitbutton = Button(masta, text = 'Exit',
                                 width = 15, command = self.Exit)
        exitbutton.grid(row = 2, column = 2, columnspan = 1, rowspan = 1)
        self.exitbutton = exitbutton

    #   Stop Watch
    def StopWatch(self):
        
        if not prep.stopwatchrun and not prep.exitrun:

            other = self
            
            prep.stopwatchrun = True         
            other.run = False
            
            other.masta = Tk()
            other.masta.title('StopWatch')
            other.timer = [0,0,0,0]     # [hours, minutes ,seconds, centiseconds]
            
            other._makewidget()
            other._update_time()
            
            other.masta.bind('<Escape>', lambda e : self._swquit())
            other.masta.protocol('WM_DELETE_WINDOW',self._swquit)
            
        else:
            if prep.stopwatchrun :
                showinfo(title = 'Alert',
                      message ='Please Close the StopWatch')
            else :
                showinfo(title = 'Alert',
                      message ='Please Close the Exit Window')
            
        
    def _makewidget(self):
        
        timeFrame = LabelFrame(self.masta, text='Time Frame',
                               width=700)
        timeFrame.grid(row=0,column=0, sticky=W)
        self.timeFrame = timeFrame

        self._swbuttons()
        self._swlabel()
        
    def _swbuttons(self, *args):

        if len(prep.list_of_buttons) == 0:
            for count in range(3):
                prep.list_of_buttons.append(Button(self.masta))

            reset = prep.list_of_buttons[2]
            reset['text'] = 'Reset'
            reset['command'] = self._resetTime
            reset['width'] = 15
            self.reset = reset
           
            pause = prep.list_of_buttons[1]
            pause['text'] = 'Pause'
            pause['command'] = self._pause
            pause['width'] = 15
            self.pause = pause
            
            start = prep.list_of_buttons[0]
            start['text'] = 'start'
            start['command'] = self._start
            start['width'] = 15
            self.start = start

            self.timed_buttons()
        else :
            prep.list_of_buttons.clear()
            self._swbuttons()

    def timed_buttons(self, *args):
        if prep.buttoncounter != len(prep.list_of_buttons):
            prep.list_of_buttons[prep.buttoncounter].grid(row =
                            prep.buttoncounter, column =1)
            prep.buttoncounter +=1
            self.masta.after(1500, self.timed_buttons)
        else:
            prep.buttoncounter = 0

    def _swlabel(self):
        
        show = Label(self.masta, text='00:00:00:00',font=('Helvatica', 30))
        show.grid(row=0, column=0)
        self.show = show

    def _update_time(self):

        if self.run :                   #stopwatch is running
            self.timer[3] += 1
            if (self.timer[3] >= 100):  #100 centiseconds to 1 second
                self.timer[3] = 0
                self.timer[2] += 1      #add 1 second

            if (self.timer[2] >= 60):   #60 seconds to 1 minute
                self.timer[1] += 1
                self.timer[2] = 0       #add 1 minute

            if (self.timer[1] >= 60):   #60 minutes to 1 hour
                self.timer[0] += 1
                self.timer[1] = 0       #add 1 hour

            string = ''.join(e for e in
                             (
                            str(self.timer[0]),':',
                            str(self.timer[1]),':',
                            str(self.timer[2]),':',
                            str(self.timer[3]))
                             )
            self.timeString = str(string)
            self.show.config(text=self.timeString)
            
        self.masta.after(10, self._update_time)

    def _start(self):                   #Start the stopwatch
        
        self.run = True

    def _pause(self):                   #Pause the stopwatch
        
        self.run = False
        if prep.funs:
            self.abc = self.timeString
            prep.swcounter = self.abc[4]
            alabel['text'] = (prep.swcounter)

    def _resetTime(self):               #Reset the stopwatch
        
        self.run = False
        self.timer = [0,0,0,0]
        self.show.config(text='00:00:00:00')
        
    def _swquit(self, event = None):
        
        self._ask_quit(allwindow = False, sw = True)
            
    #   Clock
    def Clock(self, event = None, *args):

        prep.clockrun = False
        self._update_clock()
        self.clock['command'] = self._stop_clock   

    def _stop_clock(self):

        now = time.strftime("%H:%M:%S")
        if prep.funs :
            prep.clockcounter = now[7]
            self.alabel.configure(text=prep.clockcounter)
        else:
            self.alabel.configure(text=now)
        self.clock['command'] = self.Clock
        prep.clockrun = True
        
    def _update_clock(self):

        if not prep.clockrun:
            now = time.strftime("%H:%M:%S")
            self.alabel.configure(text=now)
            self.after(1000, self._update_clock)
    
    #   Exit
    def Exit(self, event=None, *args):
        
        if prep.stopwatchrun:
            showinfo(title = 'Alert',
                     message ='Please Close the Stopwatch First')
        else:
            if not prep.exitrun:                
                prep.exitrun = True
                other = self
                
                other.masta = Tk()
                other.masta.title('No')
                other.masta.geometry('250x100')

                yes = Button(
                                 other.masta, text="Yes", fg = 'black',
                                 bg = 'white', command = other._trick,
                                 width = 20, state = 'normal'                   
                                 )
                yes.pack()
                other.yes = yes
                
                no = Button(
                                 other.masta, text="No", fg = 'black',
                                 bg = 'white', command = other._falseintention,
                                 width = 20
                                 )
                no.pack()
                other.no = no

                other.masta.bind('<Escape>', lambda e: self._exitquit())
                other.masta.protocol('WM_DELETE_WINDOW',self._exdestroy)
                                
            else :
                showinfo(title = 'Alert',
                         message ='Please Close the Window First')
            
    def _exitquit(self, event = None):
        
        self.yes['state'] = 'disabled'
        self.no['state'] = 'disabled'
        self._ask_quit(ex = True)
        
    def _exdestroy(self, event = None):
        
        prep.exitrun = False
        self.masta.destroy()
    
    def _trick(self, event=None, *args):
        
        self.yes['text'],self.no['text'] = ':(',':)'
        self.yes['command'] = self._exitquit
    
    def _falseintention(self, event=None, *args):

        self.masta.destroy()
        showinfo('<3', message = 'Thank you :)')
        prep.exitrun = False

    def _ask_quit(self, allwindow = True, sw = False,
                  ex = False, event = None):
        
        if not prep.funs or prep.swcounter == '1':
            if askokcancel("Quit", "You want to quit now? *sniff*"):
                if sw:
                    prep.stopwatchrun = False
                try:
                    self.masta.destroy()
                    if allwindow:
                        root.destroy()
                        
                except TclError:
                    if allwindow:
                        try:
                            root.destroy()
                        except TclError :
                            pass
                        
        elif prep.funs:
            if ((prep.clockcounter == '3' or prep.clockcounter =='4')
                and prep.swcounter == '1'):
                if askokcancel("Quit", "You want to quit now? *sniff*"):
                    if sw:
                        prep.stopwatchrun = False
                    try:
                        self.masta.destroy()
                        if allwindow:
                            root.destroy()
                            
                    except TclError:
                        if allwindow:
                            try:
                                root.destroy()
                            except TclError :
                                pass

            else:
                alabel['text'] = 'Try Again \n Get Help'
        
        elif ex :
            self.masta.destroy()
            prep.exitrun = False

    #   Puzzle       
    def Fun(self, event=None, *args):

        prep.funs = True

        self.exitbutton['command'] = self._alternateExit
        root.protocol('WM_DELETE_WINDOW',self._no_x)

        self.alabel['text'] = 'Have Fun'
        
        for a in prep.morehelp:
                prep.helping.append(a)

    def _no_x(self, event =None):
        pass

    def _alternateExit(self, event=None, *args):
        
        if prep.stopwatchrun:
            showinfo(title = 'Alert',
                     message ='Please Close the Stopwatch First')
        else:
            
            if not prep.exitrun:                
                prep.exitrun = True
                other = self
                
                other.masta = Tk()
                other.masta.title('No')
                other.masta.geometry('250x100')

                menubar = Menu(other.masta)
                filemenu = Menu(menubar, tearoff = 0)

                filemenu.add_command(label = 'Exit?',
                                     command = other._ask_quit)
                filemenu.add_separator()
                menubar.add_cascade(label = 'file', menu = filemenu)
                other.masta.config(menu = menubar)
                                
                yes = Button(
                                 other.masta, text="Yes", fg = 'black',
                                 bg = 'white', command = other._falseintention,
                                 width = 20, state = 'disabled'                   
                                 )
                yes.pack()
                other.yes = yes
                
                no = Button(
                                 other.masta, text="No", fg = 'black',
                                 bg = 'white', command = other._falseintention,
                                 width = 20
                                 )
                no.pack()
                other.no = no

                other.masta.bind('<Escape>', lambda e: self._exitquit())
                other.masta.protocol('WM_DELETE_WINDOW',self._exdestroy)
                
            else :
                showinfo(title = 'Alert',
                         message ='Please Close the Window First')

    def Helps(self, event=None, *args):
        if not prep.clockrun:
            showinfo(title = 'Alert',
                      message ='Please Stop the Clock First')
        else:
            if not prep.funs:
                rand = random.randint(0,3)
                alabel['text'] = prep.helping[rand]

            elif prep.funs :
                rand = random.randint(0,7)
                if prep.helpcounter == 0:
                    alabel['text'] = prep.helping[4]
                    prep.helpcounter += 1
                elif prep.helpcounter == 1:
                    alabel['text'] = prep.helping[5]
                    prep.helpcounter += 1
                elif prep.helpcounter == 2:
                    alabel['text'] = prep.helping[6]
                    prep.helpcounter += 1
                elif prep.helpcounter == 3:
                    alabel['text'] = prep.helping[7]
                    prep.helpcounter += 1
                else:
                    alabel['text'] = prep.helping[rand]

class prep(gui):
    '''preparation'''
    
    swcounter = None
    clockcounter = None
    buttoncounter = 0
    exbindcounter = 0
    helpcounter = 0
    clockrun = False
    exitrun = False
    funs = False
    stopwatchrun = False

    list_of_buttons = []
    
    helping = ['StopWatch button makes \n a new stopwatch window',
               'Clock button makes the \n label change into a clock',
               'Exit button closes \n the window',
               'Fun button makes a \n puzzle to quit the window'
               ]
                                  
    morehelp = ['Oh no i can\'t quit the window',
                'Chill for a second and make it count',
                'Tick.. Tick.. Tick..',
                'The clock is ticking'
                ]
def main():
    
    global root
    root = Tk()                         # Make window
    my_gui = 'a'
    gui(root)
    root.mainloop()
            
if __name__ == '__main__':
    main()
