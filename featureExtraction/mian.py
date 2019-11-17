import os,sys
from featureExtraction import astAnalysis
from featureExtraction import calculines
from featureExtraction import ParseCmdArgs
from featureExtraction import cacheFile
from featureExtraction import lexicalAnalysis as lex
from featureExtraction import pinYinCheck
from featureExtraction import astAnalysis
from featureExtraction import writeCSV
import os
from featureExtraction import astAnalysis
from featureExtraction import writeCSV
from flask import Flask
from os.path import dirname, abspath
# ======================================================
# =========此文件用于分析代码，拿到各个想要的值================
# ======================================================
# 文件上传需要
ALLOWED_EXTENSIONS = {'txt','py'}
UPLOAD_FOLDER=dirname(abspath(__file__))+"/upload"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
rawCountInfo = [0, 0, 0, 0, 0]
mainList = {}
f = open(os.path.abspath(os.path.dirname(__file__))+'/pinyin.txt', 'r')

def SafeDiv(dividend, divisor):
    if divisor:
        return float(dividend)/divisor
    elif dividend:
        return -1
    else:
        return 0
gProcFileNum = 0
SORT_ORDER = (lambda x:x[0], False)
def averageOfList(array): #求列表平均值
    avg = 0.0
    n = len(array)
    for num in array:
        avg+= 1.0*num/n
    return avg

def additionOfList(array):
    add = 0
    for i in array:
        add += 1*i
    return add

def CountFileLines(filePath, pinYinLib, isRawReport=True, isShortName=False):
    print("wwwwwwwwwwwwwwww")
    keyWordsInFile = []
    numInFile = []
    parenthesesNum = 0          #圆括号数量
    delimitersNum = 0           #界符数量
    commaNum = 0                #逗号数量
    ifNum = 0                   #if数量
    whileNum = 0                #while数量
    forNum = 0                  #for数量
    operatorNumInEachLine = []  #每行逻辑运算符的个数
    pinYinList = []             #拼音，暂时不用
    comparisonOperatorNum = 0   #比较运算符
    arithmeticOperatorNum = 0   #数学运算符

    mainListLine = ['']*len(writeCSV.attr) #这个应该是写csv的。写入csv文件的每一行，一个文件填一行
                                           #这里需要这东西，就是数组吧。

    defNum = 0                  #一个样例文件检测有几个def
    maxLineLength = 0           #最大行数
    detailCountInfo = []        # 一个文件更新一次
    codeDepth = []              # 一个文件更新一次
    operatorNumEachLine = []    #每行逻辑运算符个数
    print("daozheli")
    fileExt = os.path.splitext(filePath[0])
    mainListLine[0] = os.path.basename(filePath[0])
    print('&'*30)
    print(mainListLine[0])

    # ------------------------判断文件类型的-------------------------
    if fileExt[1] == '.c' or fileExt[1] == '.h':
        fileType = 'ch'
    elif fileExt[1] == '.py': #==(比较运算符)判断对象值(value)是否相同
        fileType = 'py'
    elif fileExt[1] == '.txt': #==(比较运算符)判断对象值(value)是否相同
        fileType = 'py'
    else:
        return
    global gProcFileNum; gProcFileNum += 1
    sys.stderr.write('%d files processed...\r'%gProcFileNum)
    isBlockComment = [False]*2  #或定义为全局变量，以保存上次值
    lineCountInfo = [0]*5       #[代码总行数, 代码行数, 注释行数, 空白行数, 注释率]
    #真正打开的是在这里
    print("open卡住了")
    with open(os.path.join('/Users/woniu/show3/upload/', filePath[0]), 'r', encoding='UTF-8') as file:
        token = []
        lineLength = []
        astAnalysis.astAnalysis(file)
        file.seek(0)            #回到文件起始处
        for line in file:
            if(len(line)>maxLineLength):        #最大行长
                maxLineLength = len(line)
            if("def " in line):                 #函数数量
                defNum += 1
            if("if" in line):                   #if
                ifNum += 1
            if ("while" in line):               #while
                whileNum += 1
            if ("for" in line):                 #for
                forNum += 1
            if line.count("    ")!=0:
                codeDepth.append(line.count("    "))#你别告诉我这是在算代码深度
            elif line.count("\t")!=0:
                codeDepth.append(line.count("\t"))  #这个也是吧，按制表符算的


            lineLength.append(len(line))

            word_line, identifier = lex.Scan(line.strip())  #进入句中分析。
            operatorNumInThisLine = 0
            for i in word_line:
                valueInline = list(i.values())[0]
                if valueInline>=(len(lex.key_word)+len(lex.delimiters)) and valueInline<(len(lex.key_word)+len(lex.delimiters)+len(lex.operator)):
                    operatorNumInThisLine += 1
                token.append(i)
            operatorNumInEachLine.append(operatorNumInThisLine)
            lineType = calculines.CalcLinesPy(line.strip(), isBlockComment)
            lineCountInfo[0] += 1
            if   lineType == 0:  lineCountInfo[3] += 1
            elif lineType == 1:  lineCountInfo[1] += 1
            elif lineType == 2:  lineCountInfo[2] += 1
            elif lineType == 3:  lineCountInfo[1] += 1; lineCountInfo[2] += 1
            else:
                assert False, 'Unexpected lineType: %d(0~3)!' %lineType
        # print(token)
        # print('#' * 20)
        # print(token)
        # print(lex.identifier)
        # print(lex.error_word)
        # print(lineLength)
        # print(defNum)
        # print(codeDepth)
        # print("最大缩进数目：", max(codeDepth))
        # print(blankLine)

        # for i in lex.identifier:
        #     print(len(i),i)
        # print("\n")
    if isRawReport:
        global rawCountInfo
        rawCountInfo[:-1] = [x+y for x,y in zip(rawCountInfo[:-1], lineCountInfo[:-1])]
        rawCountInfo[-1] += 1
    elif isShortName:
        lineCountInfo[4] = SafeDiv(lineCountInfo[2], lineCountInfo[2]+lineCountInfo[1])
        detailCountInfo.append([os.path.basename(filePath), lineCountInfo])
    else:
        lineCountInfo[4] = SafeDiv(lineCountInfo[2], lineCountInfo[2]+lineCountInfo[1])
        detailCountInfo.append([filePath, lineCountInfo])

    mainListLine[1] = lineCountInfo[0]              #这个数获取文件名的
    mainListLine[2] = maxLineLength
    mainListLine[3] = max(codeDepth) if len(codeDepth)!=0 else 0
    #我也不知道下面再干嘛，就这个用吧。
    for i in range(len(token)):
        key = list(token[i].keys())[0]
        value = list(token[i].values())[0]
        if key=='key_word' and value<len(lex.key_word):
            keyWordsInFile.append(lex.key_word[value])
        if value==-1:
            numInFile.append(token[i].keys())
        if key=='(' or key==')':
            parenthesesNum += 1
        if value>=len(lex.key_word) and value<(len(lex.key_word)+len(lex.delimiters)):
            delimitersNum += 1
        if key==',':
            commaNum +=1
        if value>=len(lex.key_word) + len(lex.delimiters) and value<=len(lex.key_word) + len(lex.delimiters) + 10:
            arithmeticOperatorNum+=1
        if value>=len(lex.key_word) + len(lex.delimiters)+11 and value<=len(lex.key_word) + len(lex.delimiters) + 16:
            comparisonOperatorNum+=1
    mainListLine[4] = len(keyWordsInFile)
    mainListLine[5] = len(astAnalysis.identifier)
    maxIdentifierLength = 0
    for i in range(len(astAnalysis.identifier)):
        if len(astAnalysis.identifier[i])>maxIdentifierLength:
            maxIdentifierLength = len(astAnalysis.identifier[i])
    mainListLine[6] = maxIdentifierLength
    mainListLine[7] = len(numInFile)
    mainListLine[8] = parenthesesNum
    mainListLine[9] = delimitersNum
    mainListLine[10] = lineCountInfo[3]
    mainListLine[11] = lineCountInfo[2]
    mainListLine[12] = commaNum
    mainListLine[13] = len(astAnalysis.expressionNum) #只检测了while /if /a if a else b
    mainListLine[14] = ifNum
    mainListLine[15] = whileNum
    mainListLine[16] = forNum
    mainListLine[17] = len(astAnalysis.assignNum)
    mainListLine[18] = comparisonOperatorNum
    mainListLine[19] = defNum
    mainListLine[20] = lineCountInfo[0]
    mainListLine[21] = max(astAnalysis.funcArgsNum) if len(astAnalysis.funcArgsNum)!=0 else 0
    mainListLine[22] = averageOfList(astAnalysis.funcArgsNum)
    mainListLine[23] = max(codeDepth) if len(codeDepth)!=0 else 0
    mainListLine[24] = max(operatorNumInEachLine) if len(operatorNumInEachLine)!=0 else 0
    mainListLine[25] = additionOfList(operatorNumInEachLine)
    for i in astAnalysis.identifier:
        temp = pinYinCheck.pinyin_or_word(i,pinYinLib)
        if len(temp)!=0:
            for j in temp:
                pinYinList.append(j)
    mainListLine[26] = len(pinYinList)
    mainListLine[27] = '**'
    avg = 0
    n = len(astAnalysis.identifier)
    for i in astAnalysis.identifier:
        avg+=len(i)/n
    mainListLine[28] = avg
    mainListLine[29] = arithmeticOperatorNum
    mainListLine[30] = max(astAnalysis.funcArgs)
    mainListLine[31] = max(astAnalysis.funcArgsLen)
    mainListLine[32] = max(astAnalysis.listDepth)
    mainList[mainListLine[0]] = mainListLine
    #到这一步算是可以了。
    print(writeCSV.attr)
    print(mainList)


def ReportCounterInfo(isRawReport=True, stream=sys.stdout):
    # 代码注释率 = 注释行 / (注释行+有效代码行)
    print('FileLines  CodeLines  CommentLines  BlankLines  CommentPercent  %s' \
          % (not isRawReport and 'FileName' or ''), file=stream)
    if isRawReport:
        print('%-11d%-11d%-14d%-12d%-16.2f<Total:%d Code Files>' % (rawCountInfo[0], \
                                                                    rawCountInfo[1], rawCountInfo[2], rawCountInfo[3], \
                                                                    SafeDiv(rawCountInfo[2],
                                                                            rawCountInfo[2] + rawCountInfo[1]),
                                                                    rawCountInfo[4]), file=stream)
        return
    total = [0, 0, 0, 0]
    # 对detailCountInfo排序。缺省按第一列元素(文件名)升序排序，以提高输出可读性。
    detailCountInfo.sort(key=SORT_ORDER[0], reverse=SORT_ORDER[1])
    for item in detailCountInfo:
        print('%-11d%-11d%-14d%-12d%-16.2f%s' % (item[1][0], item[1][1], item[1][2], \
                                                 item[1][3], item[1][4], item[0]), file=stream)
        total[0] += item[1][0];
        total[1] += item[1][1]
        total[2] += item[1][2];
        total[3] += item[1][3]
    print('-' * 90, file=stream)  # 输出90个负号(minus)或连字号(hyphen)
    print('%-11d%-11d%-14d%-12d%-16.2f<Total:%d Code Files>' \
          % (total[0], total[1], total[2], total[3], \
             SafeDiv(total[2], total[2] + total[1]), len(detailCountInfo)), file=stream)


def ParseTargetList(targetList):
    fileList, dirList = [], []
    if targetList == []:
        targetList.append(os.getcwd())
    print(os.getcwd())
    for item in targetList:
        if os.path.isfile(item):
            fileList.append(os.path.abspath(item))
        elif os.path.isdir(item):
            dirList.append(os.path.abspath(item))
        else:
            print("'%s' is neither a file nor a directory!" % item, file=sys.stderr)
    return [fileList, dirList]


def CountDir(dirList, pinYinLib, isKeep=False, isRawReport=True, isShortName=False):
    for dir in dirList:
        if isKeep:
            for file in sorted(os.listdir(dir)):
                CountFileLines(os.path.join(dir, file), pinYinLib, isRawReport, isShortName)
        else:
            for root, dirs, files in os.walk(dir):
                for file in files:
                    CountFileLines(os.path.join(root, file), pinYinLib, isRawReport, isShortName)


def CountFile(file, pinYinLib, isRawReport=True, isShortName=False):
    #因为只有一个文件，直接就这个就行了。
    print("00000000000000000")
    print(file)
    CountFileLines(file, pinYinLib, isRawReport, isShortName, )

    # for file in fileList:
    #     CountFileLines(file, pinYinLib, isRawReport, isShortName, )

def SetSortArg(sortArg=None):
    global SORT_ORDER
    if not sortArg:
        return
    if any(s in sortArg for s in ('file', '0')): #条件宽松些
    #if sortArg in ('rfile', 'file', 'r0', '0'):
        keyFunc = lambda x:x[1][0]
    elif any(s in sortArg for s in ('code', '1')):
        keyFunc = lambda x:x[1][1]
    elif any(s in sortArg for s in ('cmmt', '2')):
        keyFunc = lambda x:x[1][2]
    elif any(s in sortArg for s in ('blan', '3')):
        keyFunc = lambda x:x[1][3]
    elif any(s in sortArg for s in ('ctpr', '4')):
        keyFunc = lambda x:x[1][4]
    elif any(s in sortArg for s in ('name', '5')):
        keyFunc = lambda x:x[0]
    else: #因argparse内已限制排序参数范围，此处也可用assert
        print('Unsupported sort order(%s)!' %sortArg,file = sys.stderr)
        return
    isReverse = sortArg[0]=='r' #False:升序(ascending); True:降序(decending)
    SORT_ORDER = (keyFunc, isReverse)

def LineCounter(pinYinLib, isKeep=False, isRawReport=True, isShortName=False, targetList=[]):
    fileList, dirList = ParseTargetList(targetList)
    #因为这个项目不用，所以上面那两项是空的，没用，后面地址写死了。
    print(fileList, dirList)
    print("linecounter")
    print(targetList)
    CountFile(targetList, pinYinLib, isRawReport, isShortName)

    # if fileList != []:
    #     CountFile(fileList, pinYinLib, isRawReport, isShortName)
    # if dirList != []:
    #     CountDir(dirList, pinYinLib, isKeep, isRawReport, isShortName)


def main(pinYinLib,target2):

    print("进入main")

    global rawCountInfo, detailCountInfo
    (keep, detail, basename, sort, out, cache, target) = ParseCmdArgs.ParseCmdArgs()
    stream = sys.stdout if not out else open(out, 'w')
    SetSortArg(sort)
    #如果使用target上面那句话会覆盖掉
    print(target2)
    cacheUsed = cacheFile.shouldUseCache(keep, detail, basename, cache, target)
    print(cacheUsed)
    print(target)
    target=target2
    print(target)

    if cacheUsed:
        try:
            (rawCountInfo, detailCountInfo) = cacheFile.CounterLoad()
        except (EOFError, ValueError) as e: #不太可能出现
            print( 'Unexpected Cache Corruption(%s), Try Counting Directly.'%e,file = sys.stderr)
            LineCounter(pinYinLib, keep, not detail, basename, target)
    else:
       LineCounter(pinYinLib, keep, not detail, basename, target)
    ReportCounterInfo(not detail, stream)
    # cacheFile.CounterDump((keep, detail, basename, target))
def start(target):
    print("从这里进")
    pinyin_Lib = []
    for line in f:
        pinyin_Lib.append(str(line.strip()))

    from time import clock
    # startTime = clock()
    print(target)
    targetList=[]
    targetList.append(str(target))
    print(targetList)
    main(pinyin_Lib,targetList)

    # endTime = clock()
    # print('Time Elasped: %.2f sec.' %(endTime-startTime),file = sys.stderr)
    # print(pinYinCheck.pinyin_or_word("clock",pinyin_Lib))
    f.close()
    writeCSV.writeCSV(mainList)


#其实是从这里开始的。之前顺序结构是从上往下。其实这个也是自上往下。
if __name__ == '__main__':
    print("从这里进")
    pinyin_Lib = []
    for line in f:
        pinyin_Lib.append(str(line.strip()))

    from time import clock
    # startTime = clock()
    main(pinyin_Lib)
    # endTime = clock()
    # print('Time Elasped: %.2f sec.' %(endTime-startTime),file = sys.stderr)
    # print(pinYinCheck.pinyin_or_word("clock",pinyin_Lib))
    f.close()
    writeCSV.writeCSV(mainList)