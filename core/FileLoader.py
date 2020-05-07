from tkinter import filedialog




class FileLoader():

  def __init__(self,*kwargs):
    self.f_format = None # format_no_point
    self.path = None # path/to/file/no/extension
    self.data = "Load a file using\nthe FIle->Load\nOr save this one"
  
  
  def delete(self):
    os.remove(self.path+"."+self.f_format)
    print("Removed the file at "+self.path+"."+self.f_format)
    # delete file at self.path + format
  
  def save(self,path = None, f_format = None):
    if path == None: path = self.path
    if f_format == None: f_format = self.f_format
    ff = open(path+"."+f_format,"w")
    ff.write(self.data)
    ff.close()
  
  def openFile(self,path,f_format):
    self.f_format = f_format
    self.path = ".".join(path.split(".")[:-1])
    ff = open(path,"r")
    self.data = ""
    for x in ff.readlines():
      self.data += x
    ff.close()