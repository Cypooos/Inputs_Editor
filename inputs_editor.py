import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.scrolledtext as scrolledtext
import traceback
import sys, os
from core.converter import Converter
from core.FileLoader import FileLoader



def alert():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be created.")
def link():
  messagebox.showinfo("hellow !","Hey !\nI am yet to be linked.")

class Inputs_Editor():

  def __init__(self):
    self.debugmode = False
    self.windows = tk.Tk()
    self.windows.geometry("500x300")
    self.windows.minsize(250, 150) 
    self.fileLoader = FileLoader()
    self.converter = Converter()
    self.options = {}
    self.reloadOptions()
    self.menubar = None
  
  def reloadOptions(self):
    f = open("core/options.txt","r")
    self.options = {}
    for line in f.read().replace("\n","").split(";"):
      self.options[line.split(":")[0]] = ":".join(line.split(":")[1:])
    f.close()
  
  def saveOptions(self):
    f = open("core/options.txt","w")
    for key,value in self.options.items():
      f.write(key+":"+value+";\n")
    f.close()

  
  def ask(self,question):
    askWin=tk.Tk()
    a=tk.StringVar()
    tk.Label(askWin, text=question).pack()
    tk.Entry(askWin, textvariable=a).pack()
    tk.Button(askWin, text='Ok', command=lambda:askWin.destroy()).pack()
    askWin.mainloop()
    return a.get


  def newFile(self):
    self.fileData.delete(1.0,tk.END)
    self.fileLoader.path = None
    self.fileLoader.f_format = None


  def openFile(self):
    filepath = filedialog.askopenfilename(title="Open file",filetypes=[(y,"."+x) for x,y in self.converter.supportedFormats.items()],defaultextension="."+list(self.converter.supportedFormats.keys())[0])
    if (not filepath) or filepath == "": print("Open canceled"); return
    print(filepath.split(".")[-1])
    if not any([filepath.split(".")[-1] == x for x in [x.lower() for x in self.converter.supportedFormats.keys()]]):
      f_format = self.ask("Please specified the format of the file")
    else:
      f_format = filepath.split(".")[-1]
    self.fileLoader.openFile(filepath,f_format)
    self.fileData.delete("1.0",tk.END)
    self.fileData.insert("1.0", self.fileLoader.data)

  def saveFile(self):
    if self.fileLoader.path == None:
      self.saveAsFile()
    else:
      self.fileLoader.data = self.fileData.get("1.0", tk.END)
      self.fileLoader.save()


  def saveAsFile(self):
    self.fileLoader.data = self.fileData.get("1.0", tk.END)
    path = filedialog.asksaveasfilename(title="Save as",filetypes=[(y,"."+x) for x,y in self.converter.supportedFormats.items()],defaultextension="."+list(self.converter.supportedFormats.keys())[0])
    if not path.split(".")[-1] in list(self.converter.supportedFormats.keys()):
      path+=".tas"
    if (not path) or path == "": print("SaveAs canceled"); return
    cut_path = ".".join(path.split(".")[:-1])
    f_format = path.split(".")[-1]
    print(path)
    self.fileLoader.save(cut_path,f_format)



  def setupMenu(self):

    self.menubar = tk.Menu(self.windows)

    menu_file = tk.Menu(self.menubar, tearoff=0)
    menu_file.add_command(label="Create", command=lambda : self.newFile())
    menu_file.add_command(label="Open", command=lambda : self.openFile())
    menu_file.add_command(label="Save", command=lambda : self.saveFile())
    menu_file.add_command(label="Save as", command=lambda : self.saveAsFile())
    menu_file.add_separator()

    menu_file_convert = tk.Menu(menu_file, tearoff=0) # file save
    def conv(typeOut):
      self.converter.convert(self.fileLoader.path+"."+self.fileLoader.f_format,self.fileLoader.f_format,typeOut)
      self.fileLoader.delete()
      self.fileLoader.f_format = typeOut
      self.fileLoader.save()
    menu_file_convert.add_command(label="To RTAS", command=lambda : conv("RTAS"))
    menu_file_convert.add_command(label="To TAS", command=lambda : conv("TAS"))
    menu_file_convert.add_command(label="To SSFCT", command=lambda : conv("SSFCT"))

    menu_file.add_cascade(label="Convert to", menu=menu_file_convert)
    menu_file.add_command(label="Quit", command=self.windows.quit)
    self.menubar.add_cascade(label="File", menu=menu_file)

    menu_info = tk.Menu(self.menubar, tearoff=0)
    menu_info.add_command(label="Informations", command=lambda : messagebox.showinfo("Informations","Go to the GitHub for more information about the project !\nhttps://github.com/Discursif/Inputs_Editors"))
    menu_info.add_command(label="Credits", command=lambda : messagebox.showinfo("Credits","Inputs_Editors is created by </Discursif>\nWith the help of the TASbot discord"))
    menu_info.add_command(label="Help", command=lambda : messagebox.showinfo("Help","Sorry, nobody can help you :("))
    menu_info.add_command(label="Formats", command=lambda : messagebox.showinfo("Formats","The valids and implemented formats are :\n"+", ".join([("."+x) for x in self.converter.supportedFormats.keys()])))
    menu_info.add_separator()
    menu_info.add_command(label="Options", command=lambda:self.setOptions())
    self.menubar.add_cascade(label="Infos", menu=menu_info)

    self.windows.config(menu=self.menubar)

  def setupMainFrame(self):
    tasFrame = tk.LabelFrame(self.windows, text="File", width=20)
    tasFrame.grid(column=0)
    self.fileData = scrolledtext.ScrolledText(tasFrame)
    self.fileData.pack(expand = True, fill = tk.BOTH)

    infoFrame = tk.LabelFrame(self.windows, text="Informations")
    infoFrame.grid(column=1)

  def showError(self, *args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Error !', err[-1])
    print("".join(err))

  def start(self):
    self.setupMenu()
    tk.Tk.report_callback_exception = self.showError
    self.setupMainFrame()
    self.windows.mainloop()
  
    
  def askInputs(self,inputs):
    askWin = tk.Tk()
    values = {}
    count = 0
    for key in inputs:
      tk.Label(askWin, text=key).grid(row=count, sticky=tk.W)
      en = tk.Entry(askWin)
      values[key] = en
      en.grid(row=count, column=1)
      count +=1
    tk.Button(askWin, text = "Send", command = lambda: askWin.destroy()).grid(row=count,column=2)
    askWin.mainloop()
    return [y.get() for y in values.values()]

  def setOptions(self):
    entrys = {}

    def refreshOpts():
      for widget in OptWindow.winfo_children():
        widget.destroy()
      entrys = {}
      count = 1
      tk.Label(OptWindow,text="Options :").grid(row=0)
      for key,value in self.options.items():
        tk.Label(OptWindow, text=key).grid(row=count, sticky=tk.W)
        val = tk.StringVar(OptWindow, value=value)
        en = tk.Entry(OptWindow, textvariable=val)
        entrys[key] = en
        en.grid(row=count, column=1)
        count +=1
      tk.Button(OptWindow, text ="Save", command = lambda: saveConf()).grid(row=count)
      tk.Button(OptWindow, text ="Exit", command = lambda: OptWindow.destroy()).grid(row=count,column=1)
      tk.Button(OptWindow, text ="Add & Save", command = lambda: addOpt()).grid(row=count+1)
      tk.Button(OptWindow, text ="Open file", command = lambda: openOpt()).grid(row=count+1,column=1)
    
    def saveConf():
      self.options = {x:y.get() for x,y in entrys.items()}
      refreshOpts()
    
    def openOpt():
      print("Opening:"+ os.path.dirname(os.path.realpath(__file__))+"/core/options.txt")
      webbrowser.open('file:///' +os.path.dirname(os.path.realpath(__file__))+"/core/options.txt")
    
    def addOpt():
      vals = self.askInputs(["Key :","Value :"])
      self.options = {x:y.get() for x,y in entrys.items()}
      self.options[vals[0]] = vals[1]
      refreshOpts()
      OptWindow.destroy()
    
    OptWindow = tk.Tk()
    OptWindow.geometry("200x350")
    OptWindow.minsize(200,150)
    OptWindow.maxsize(200,600)
    refreshOpts()
    OptWindow.mainloop()


if __name__ == "__main__":
  ie = Inputs_Editor()
  ie.start()