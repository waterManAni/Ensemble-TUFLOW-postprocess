import os
import pandas as pdd

def containsstring (string, includetexts,excludetexts):
    contain_TF, doesntcontain_TF =1,1
    if len (''.join(includetexts))>0: #if any strings are passed inside includetexts
        contains=[x.upper () for x in includetexts] #CONVERT EVERYTHING TO UPPER CASE FOR NON CASE SENSITIVE
        contain_TF= all(substring in string.upper() for substring in contains) #TRUE IF ALL INCLUDETEXTS ARE CONTAINED IN THE STRING
    if len (''.join(excludetexts))>0:
        doesntcontain = [x.upper () for x in excludetexts] #CONVERT EVERYTHING TO UPPER CASE FOR NON CASE SENSITIVE
        doesntcontain_TF = not any(substring in string.upper() for substring in doesntcontain) #TRUE IF NO EXCLUDETEXTS ARE IN THE STRING
    return all ([contain_TF, doesntcontain_TF])
    
def clrscr():
    print("\033[H\033[J")
    os.system ('cls')
 
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


def directory_scan (keywordsinclude, keywordsexclude, resultfolder, savefile):
    
    
    listofresults = findfiles (resultfolder,keywordsinclude, keywordsexclude) #file name should contain include but not contain exclude
    
    ##########################################################
    
    ### FIND FILES CONTAINING OR NOT CONTAINING ENTERED KEYWORDS: be very careful with exclude texts, IT CAN MESS THINGS UP
    resultlistdf = pdd.DataFrame (listofresults,columns=['FilePath'])
    resultlistdf.to_csv (savefile,index=False, header=True)
    clrscr()