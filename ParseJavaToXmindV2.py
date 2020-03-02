import os
import re
import xmind
import argparse

class ParseJavaToXmind:
    def __init__(self,mainTitle):
        self.fileList = []
        self.lineList = []
        self.contentList=[]
        self.lineDic = {}
        self.filepath=''
        self.mainTitle = mainTitle
        self.xFileName = './'+'target/'+mainTitle+'.xmind'

    def getSrcFiles(self,filedir):
        self.filepath=filedir
        for root, dir, files in os.walk(filedir,topdown=False):
            for file in files:
                if file[-5:]=='.java':
                    ffile= root+'\\'+str(file)
                    self.fileList.append(ffile)
        print('all files------')
        print(self.fileList)

    def parse(self):
        for onefile in self.fileList:
            with open(onefile,'r',encoding='utf-8') as f:
                line =f.readline()
                while line:
                    sline = line.strip()
                    if(re.match(r'//\d',sline)):
                        self.lineList.append(sline[2:])
                        content = f.readline()
                        if content:
                            ClaName = os.path.basename(onefile)
                            self.contentList.append(ClaName+'--------'+content.strip())
                    line = f.readline()
        print('find all tags------')

    def classify(self):
        i=0
        for sline in self.lineList:
            cline = self.contentList[i]
            sp = sline.split()
            dicList=[sline,cline]
            self.lineDic[sp[0]]=dicList
            i=i+1
        print('classify------')
        #print(self.lineDic)

    def genTree(self):
        topicList=[]
        max = 0
        targetPath = './target'
        isExists =  os.path.exists(targetPath)
        if not isExists:
            os.mkdir(targetPath)
        w = xmind.load(self.xFileName)  # load an existing file or create a new workbook if nothing is found
        s1 = w.getPrimarySheet()  # get the first sheet
        s1.setTitle(self.mainTitle)  # set its title
        r1 = s1.getRootTopic()  # get the root topic of this sheet
        r1.setTitle(mainTitle)  # set its title
        for key in self.lineDic.keys():
            keyLen = len(key)
            if (keyLen > max):
                max = keyLen
        print('max len tags')
        print(max)
        for i in range(1,max+1,2):
            if(i==1):
                oneList =[x for x in self.lineDic.keys() if len(x)==i]
                for onekey in oneList:
                    topTopic=r1.addSubTopic()
                    topTopic.setTitle(self.lineDic[onekey][0])
                    topTopic.setPlainNotes(self.lineDic[onekey][1])
                    topicList.append(topTopic)

            else:
                moreList=[x for x in self.lineDic.keys() if len(x)==i]
                for morekey in moreList:
                    supKey=morekey[0:i-2]
                    print('process key------')
                    #print(str(supKey))
                    for findr in topicList:
                        findkey=findr.getTitle().split()[0]
                        if findkey==supKey:
                            subTopic=findr.addSubTopic()
                            subTopic.setTitle(self.lineDic[morekey][0])
                            subTopic.setPlainNotes(self.lineDic[morekey][1])
                            topicList.append(subTopic)
                            break
                        else:
                            continue
        xmind.save(w, self.xFileName)
        print('Process Success-------')



if __name__ == '__main__':
    fileParser = argparse.ArgumentParser(description='scan file to xmind')
    fileParser.add_argument("--F", type=str, default=r'H:\CDB\workspace')
    fileParser.add_argument("--M", type=str, default=r'A0332R100')
    args = fileParser.parse_args()
    filedir = args.F
    mainTitle = args.M
    parse = ParseJavaToXmind(mainTitle)
    if os.path.isdir(filedir):
        fileList=parse.getSrcFiles(filedir)

        parse.parse()
        parse.classify()
        parse.genTree()