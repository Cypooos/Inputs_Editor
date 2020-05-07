

class Converter():

  def __init__(self):
    self.supportedFormats = {"TAS":"Absolute TAS format","RTAS":"Relative TAS format","SSFCT":"Switch only Single Controller Tas Format"}

  def RTAStoTAS(self,fileToConvert,fileOutput):
    file_r = open(fileToConvert,"r")
    file_w = open(fileOutput,"w")
    position = 0
    while True:
      content = file_r.readline()
      if content == "":break;
      nb_frame = int(content.split(" ")[0])
      for x in range(nb_frame):
        file_w.write(str(position)+" "+" ".join(content.split(" ")[1:]))
        position +=1
    file_r.close()
    file_w.close()
  
  def convert(self,file,formatIN,formatOUT,fileOut=None):
    if not formatIN in self.supportedFormats.keys(): raise AssertionError("Format IN is not supported to convert :"+str(formatIN))
    if not formatOUT in self.supportedFormats.keys(): raise AssertionError("Format OUT is not supported to convert :"+str(formatOUT))
    if fileOut == None: fileOut = file