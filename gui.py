import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst
from tkinter import *
import webbrowser
import os

from bagging import bagging

class Gui(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.dataset=None
        self.bagging = bagging()
        self.log_dataset_name="-"
        self.log_testsize="-"
        self.log_bagsize="-"
        self.log_n_bag='-'
        self.log_svmmodels="-"
        self.log_mlpmodels="-"
        self.accuracy_bagging="-"
        self.accuracy_svm="-"
        self.accuracy_mlp="-"
        self.filename=None

    def create_widgets(self):


        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        # self.mainframe.columnconfigure(0, weight=1)
        # self.mainframe.rowconfigure(0, weight=1)

        self.subframe = ttk.Frame(self.mainframe,padding="1 1 10 1")
        self.subframe.grid(column=0,row=1,sticky=(tk.N, tk.W, tk.E, tk.S))

        self.subframesetting=ttk.Frame(self.subframe,borderwidth='2',relief='sunken',padding="1 1 1 1")
        self.subframesetting.grid(column=0,row=1,sticky=(tk.N, tk.W, tk.E, tk.S))

        self.subframesummary= ttk.Frame(self.subframe,borderwidth='2',relief='sunken',padding="1 1 1 1")
        self.subframesummary.grid(column=0,row=2,sticky=(tk.N, tk.W, tk.E, tk.S))

        self.testsizelabel = Label(self.subframesetting,text="Test size (0-1)",width='15',anchor='w')
        self.testsizelabel.grid(column=0,row=1,sticky=(tk.N, tk.W, tk.E, tk.S))
        self.testsizeentry = ttk.Entry(self.subframesetting,width='10')
        self.testsizeentry.grid(column=2,row=1,sticky=(tk.N, tk.W, tk.E, tk.S))


        self.bagsizelabel = Label(self.subframesetting,text="Bag size (0-1]",width='15',anchor='w')
        self.bagsizelabel.grid(column=0,row=2,sticky=(tk.N, tk.W, tk.E, tk.S), pady=10)
        self.bagsizeentry = ttk.Entry(self.subframesetting,width='10')
        self.bagsizeentry.grid(column=2 , row=2,sticky=(tk.N, tk.W, tk.E, tk.S),pady=10)


        self.svmmodellabel = Label(self.subframesetting,text="SVM Models",width='15',anchor='w')
        self.svmmodellabel.grid(column=0,row=3,sticky=(tk.N, tk.W, tk.E, tk.S))
        self.svmmodelentry = ttk.Entry(self.subframesetting,width='10')
        self.svmmodelentry.grid(column=2 , row=3,sticky=(tk.N, tk.W, tk.E, tk.S))


        self.mlpmodellabel = Label(self.subframesetting,text="MLP Models",width='15',anchor='w')
        self.mlpmodellabel.grid(column=0,row=4,sticky=(tk.N, tk.W, tk.E, tk.S), pady=10)
        self.mlpmodelentry = ttk.Entry(self.subframesetting,width='10')
        self.mlpmodelentry.grid(column=2 , row=4,sticky=(tk.N, tk.W, tk.E, tk.S),pady=10)


        self.defaultbutton = ttk.Button(self.subframesetting, text="Default Setting")
        self.defaultbutton.grid(column=0,row=5,padx=(50,0))
        self.defaultbutton.bind("<Button-1>",self.changeToDefault)

        self.testsizeentry.configure(state='disabled')
        self.bagsizeentry.configure(state='disabled')
        self.svmmodelentry.configure(state='disabled')
        self.mlpmodelentry.configure(state='disabled')        
        self.defaultbutton.configure(state='disabled')







        self.subframesummaryforlabel = ttk.Frame(self.subframesummary)
        self.subframesummaryforlabel.grid(column=0,row=0,sticky=(tk.N, tk.W, tk.E, tk.S))

        self.subframesummaryforsum = ttk.Frame(self.subframesummary)
        self.subframesummaryforsum.grid(column=0,row=1,sticky=(tk.N, tk.W, tk.E, tk.S))

        self.summarylabel = Label(self.subframesummaryforlabel,text="=========Summary=========")
        self.summarylabel.grid(column=0,row=1,sticky=(tk.N, tk.W, tk.E, tk.S),pady=(5,0),padx=(0,0))
        self.summaryscrolltext = tkst.ScrolledText(self.subframesummaryforsum,width=23,height=13,state=tk.DISABLED)
        self.summaryscrolltext.grid(column=0,row=2,sticky=(tk.N, tk.W, tk.E, tk.S))










        self.toolbar = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.btnRun = ttk.Button(self.toolbar,text="Run",state='disabled')
        self.btnRun.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.btnRun.bind("<Button-1>", self.runClassifying)

        self.btnRetry = ttk.Button(self.toolbar,text="Retry")
        self.btnRetry.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.btnRetry.bind("<Button-1>", self.retryClassifying)
        self.btnRetry.grid_remove() #make it invisible on the first display

        self.btnOpen = ttk.Button(self.toolbar,text="Open File")
        self.btnOpen.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnOpen.bind("<Button-1>",self.openFile)








        self.workspace = ttk.Frame(self.mainframe,padding="0 0 0 0")
        self.workspace.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrolltext = tkst.ScrolledText(self.workspace, width=50, height=25, borderwidth = 5, relief = "sunken",state=tk.DISABLED)
        self.scrolltext.grid(column=3, row = 1, sticky=(tk.N, tk.W, tk.E, tk.S))

        
        # self.textentry.pack()

    def log_history(self, msg, clear=False):
        msg = str(msg)
        self.scrolltext.config(state=tk.NORMAL)
        if clear == True:
            self.scrolltext.delete('1.0', tk.END)
        else:
            self.scrolltext.insert(tk.INSERT,msg+'\n')
        self.scrolltext.see("end")
        self.scrolltext.config(state=tk.DISABLED)

    def log_summary(self,msg,clear=False):
        msg = str(msg)
        self.summaryscrolltext.config(state=tk.NORMAL)
        if clear == True:
            self.summaryscrolltext.delete('1.0', tk.END)
        else:
            self.summaryscrolltext.insert(tk.INSERT,msg+'\n')
        self.summaryscrolltext.see("end")
        self.summaryscrolltext.config(state=tk.DISABLED)

    def convertStrToFloat(self,data):
        return float(data)

    def convertFloatToInt(self,data):
        return int(data)

    def convertFloatToStr(self,data):
        return str(data)

    def popErrorWindow(self,msg=None):
        messagebox.showerror("Error", msg)

    def cetakLogSummary(self):
        self.log_summary("clear",clear=True)
        self.log_summary("Dataset : "+self.log_dataset_name+"\n")
        self.log_summary("Test size     : "+self.log_testsize)
        self.log_summary("Bag Size      : "+self.log_bagsize)
        self.log_summary("SVM-Models    : "+self.log_svmmodels)
        self.log_summary("MLP-Models    : "+self.log_mlpmodels)
        self.log_summary("Amount of Bag : "+self.log_n_bag )
        self.log_summary("SVM-Acc       : "+self.accuracy_svm)
        self.log_summary("MLP-Acc       : "+self.accuracy_mlp)
        self.log_summary("Bagging-Acc   : "+self.accuracy_bagging)

    def retryClassifying(self,event):
        self.btnRun.grid()
        self.btnRetry.grid_remove()
        del self.bagging
        self.bagging=bagging()
        self.log_history("delete",clear=True)
        self.log_history("Reading "+self.filename)
        self.bagging.read_dataset(self.filename)
        self.log_history("Dataset loaded successfully.....")
        self.cetakLogSummary()

    def runClassifying(self,event):
        self.resetLogSummary()
        testsize = self.testsizeentry.get()
        if(testsize==""):
            self.popErrorWindow(msg="Please insert the test size!")
            return            
        inttestsize = self.convertStrToFloat(testsize)
        self.log_testsize=self.convertFloatToStr(inttestsize*100)+"%"
        if(inttestsize>=1 or inttestsize<=0):
            self.popErrorWindow(msg="Test Size must (0-1) Exclusive-Exclusive!")
            return

        bagsize =self.bagsizeentry.get()
        if(bagsize==""):
            self.popErrorWindow(msg="Please insert the bag size!")
            return 
        intbagsize = self.convertStrToFloat(bagsize)
        self.log_bagsize = self.convertFloatToStr(intbagsize*100)+"%"
        if(intbagsize>1 or intbagsize<=0):
            self.popErrorWindow(msg="Bag Size must (0-1] Exclusive-Inclusive!")
            return

        svmmodel = self.svmmodelentry.get()
        if(svmmodel==""):
            self.popErrorWindow(msg="Please insert the SVM Model size!")
            return 
        intsvmmodel = self.convertStrToFloat(svmmodel)
        self.log_svmmodels=svmmodel

        mlpmodel = self.mlpmodelentry.get()
        if(mlpmodel==""):
            self.popErrorWindow(msg="Please insert the MLP Model size!")
            return 
        intmlpmodel=self.convertStrToFloat(mlpmodel)
        self.log_mlpmodels=mlpmodel

        self.log_n_bag=self.convertFloatToStr(intsvmmodel+intmlpmodel)
        intsvmmodel=self.convertFloatToInt(intsvmmodel)
        intmlpmodel=self.convertFloatToInt(mlpmodel)

        if(intsvmmodel<0):
            self.popErrorWindow(msg="SVM Models must be an unsigned int!")
            return
        if(intmlpmodel<0):
            self.popErrorWindow(msg="MLP Models must be an unsigned int!")
            return

        if(intsvmmodel==0 and intmlpmodel==0):
            self.popErrorWindow(msg="At least 1 model assigned!")
        
        self.btnRun.grid_remove()
        self.btnRetry.grid()
        self.cetakLogSummary()

        if(self.bagging.create_bag(amount=(intsvmmodel+intmlpmodel),
            test_size=inttestsize,bag_size=intbagsize)):
            self.log_history("Crafting "+self.log_n_bag+" bags...")
        else:
            self.log_history("Error occured while crafting bags!")
            return

        self.bagging.train_data(svm_models=intsvmmodel,mlp_models=intmlpmodel)

        self.bagging.test_model()

        self.bagging.calculate_model_average()

        self.accuracy_bagging=str(self.bagging.getAccuracy()*100)+"%"

        self.cetakLogSummary()


    def changeToDefault(self,event):
        self.log_history("Restoring bagging setting to default.")
        self.returnToDefaultSetting()


    def returnToDefaultSetting(self):
        self.testsizeentry.delete(0,END)
        self.testsizeentry.insert(END,"0.33")
        self.bagsizeentry.delete(0,END)
        self.bagsizeentry.insert(END,"0.9")
        self.svmmodelentry.delete(0,END)
        self.svmmodelentry.insert(END,"6")
        self.mlpmodelentry.delete(0,END)
        self.mlpmodelentry.insert(END,"4")

    def resetLogSummary(self):
        self.log_testsize="-"
        self.log_bagsize="-"
        self.log_n_bag='-'
        self.log_svmmodels="-"
        self.log_mlpmodels="-"
        self.accuracy_bagging="-"
        self.accuracy_svm="-"
        self.accuracy_mlp="-"


    def openFile(self,event):
        self.filename = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.log_history("Reading "+self.filename)
        if(self.bagging.read_dataset(self.filename)):
            self.log_history("Dataset loaded successfully.....")
            self.btnRun.configure(state=True)
            filename_w_ext = os.path.basename(self.filename)
            filename, file_extension = os.path.splitext(filename_w_ext)
            self.log_dataset_name=filename+file_extension
            self.testsizeentry.configure(state=True)
            self.bagsizeentry.configure(state=True)
            self.svmmodelentry.configure(state=True)
            self.mlpmodelentry.configure(state=True)        
            self.defaultbutton.configure(state=True)
            self.returnToDefaultSetting()
            self.cetakLogSummary()
        else:
            self.log_history("Error while loading data!")
        
