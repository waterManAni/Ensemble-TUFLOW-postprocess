def containsstring (string, includetexts,excludetexts):
    contain_TF, doesntcontain_TF =1,1
    if len (''.join(includetexts))>0:
        contains=[x.upper () for x in includetexts]
        contain_TF= all(substring in string.upper() for substring in contains)
    if len (''.join(excludetexts))>0:
        doesntcontain = [x.upper () for x in excludetexts]
        doesntcontain_TF = not any(substring in string.upper() for substring in doesntcontain)
    print ('-'*10+'\n'+string+ ':  '+str(contain_TF)+'    '+str(doesntcontain_TF))
    return all ([contain_TF, doesntcontain_TF])
    

def findfiles (directory,includetexts, excludetexts):
    foundfiles =[]
    for dirloc, subdir, filelist in os.walk(directory):
        clrscr()
        print ('Searching directory:......'+dirloc+'\n'+'-'*50)
        if len(filelist)>0:
            for filename in filelist:
                 if containsstring (filename,includetexts,excludetexts):
                     foundfiles.append(os.path.join(dirloc, filename))
    return foundfiles
  
##### USE THIS BLOCK IF YOU WANT TO USE USE GRAPHIC INTERFACE TO SELECT FILES AND FOLDERS, REMOVE IF YOU GOOD######
import tkinter as tk
from tkinter import filedialog
def browse_file (dialog,filecategory,ext):
    currdir = os.getcwd()
    tk.Tk().withdraw() #use to hide tkinter window
    locatefile = tk.filedialog.askopenfilename(initialdir=currdir,title=dialog,filetypes =[(filecategory,ext)])
    return locatefile
def browse_directory (dialog):
    currdir = os.getcwd()
    tk.Tk().withdraw() #use to hide tkinter window
    locatefolder = tk.filedialog.askdirectory(initialdir=currdir, title=dialog)
    return locatefolder

#########
resultfolder = browse_directory ("SELECT RESULTS PARENT DIRECTORY")
savefile=file_save('SAVE CSV FILE AS: ', 'Comma Separated Value','.csv')
