# coding:utf-8

import math
import re
import csv
# 注意这个的新的标准
import os

s = []

list_name = ['name', "Abstraction", "FlowControl", "UserInteractivity", "LogicalThinking", "DataRepresentation",
             'zongfen']
liat_value = []

NUM = 1

def cal2(name):
    sname = name
    with open(sname) as archivo:
        Abstraction = [0]
        Parallelism = [0]
        FlowControl = [1]
        UserInteractivity = [0]
        LogicalThinking = [0]
        DataRepresentation = [2]
        Synchronization = [0]
        numif = 0;
        foreverTemp = 0;
        intNUM = 0
        lenNUM = 0
        h1 = 0
        h2 = 0
        H1 = 0
        H2 = 0
        inttemp = 0
        lentemp = 0
        strtemp = 0
        neizhitemp = 0
        xunhuantiTemp = 0
        for linea in archivo:
            print(linea)
            linea = linea.lstrip()
            linea = linea.rstrip()

            # ****************************************************#
            # 抽象,标记检测是，内置函数，neizhi=2
            if "def " in linea:
                Abstraction.append(3)
            if "class " in linea:
                Abstraction.append(4)
            if "import " in linea:
                Abstraction.append(2)
            if "len(" in linea:
                Abstraction.append(1)
            if "str(" in linea:
                Abstraction.append(1)
            if "int(" in linea:
                Abstraction.append(1)
            # ****************************************************#


            # ****************************************************#
            # 用户交互
            if ("print" in linea):
                UserInteractivity.append(1)
            if ("input" in linea):
                UserInteractivity.append(1)
            if ("open" in linea) | ("write" in linea) | ("read" in linea):
                UserInteractivity.append(2)
            if ('plot' in linea):
                UserInteractivity.append(3)
            if ('wenjian' in linea):
                UserInteractivity.append(2)
            # ****************************************************#


            # ****************************************************#
            # 流控制，
            # if("while" in linea):
            #	foreverTemp=2;
            #	if("True" in linea):
            #		foreverTemp=foreverTemp-1;
            # FlowControl.append(foreverTemp)

            if ("while" in linea):
                FlowControl.append(2)
                xunhuantiTemp += 1
            if ("range" in linea):
                FlowControl.append(2)
            if (("for" in linea) & ("in" in linea)):
                FlowControl.append(2)
                xunhuantiTemp += 1
            if (("break" in linea) | ("continue" in linea)):
                FlowControl.append(3)
            # if('xunhuan' in linea):
            #	FlowControl.append(3)
            # 下面的这个就是并列的意思其实
            if (xunhuantiTemp >= 2) & (xunhuantiTemp < 4):
                FlowControl.append(2)
            # if (xunhuantiTemp>=4):
            #	FlowControl.append(4)

            if ('fuza' in linea):
                FlowControl.append(4)
            if ('#bl' in linea):
                FlowControl.append(2)
            if ('#qt' in linea):
                FlowControl.append(3)
            # ****************************************************#


            # ****************************************************#
            # 逻辑，这一项对应的是最好的。
            if "if" in linea:
                LogicalThinking.append(1)
                numif = numif + 1
            if "else" in linea:
                numif = numif + 1
                LogicalThinking.append(2)
            if ("elif" in linea):
                numif = numif + 1
                LogicalThinking.append(2)
            if ("if" in linea) & (("&" in linea) | ("|" in linea) | ("not" in linea)):
                LogicalThinking.append(3)
            if (numif > 3):
                LogicalThinking.append(4)
            # ****************************************************#


            # ****************************************************#
            # 并行是0
            #
            # 同步是2，没有就算是0
            # if("return" in linea):
            #	Synchronization.append(2)
            # ****************************************************#


            # ****************************************************#
            # 数据呈现
            if ('[' in linea):
                DataRepresentation.append(3)

            if ('append' in linea) | ('index' in linea) | ('insert' in linea):
                DataRepresentation.append(3)
            if ('duixiang' in linea) | ("duixaing" in linea):
                DataRepresentation.append(4)
            # ****************************************************#


            # 抽象和问题分解中的第二级。
            if (("int(" in linea) & ("print" not in linea)):
                inttemp = 1
                intNUM += 1
            if ("len(" in linea):
                lentemp = 1
                lenNUM += 1
            if ("str(" in linea):
                strtemp = 1

        if ((inttemp == 1) | (lentemp == 1) | (strtemp == 1)):
            neizhitemp = 1
            Abstraction.append(2)

        if inttemp == 1:
            h1 += 1
        if inttemp == 1:
            h1 += 1
        h2 = intNUM + lenNUM
        H1 = intNUM + lenNUM
        H2 = intNUM + lenNUM
        zongfen = max(Abstraction) + max(FlowControl) + max(UserInteractivity) + max(LogicalThinking) + max(
            DataRepresentation)
        # 这个是抬头
        print ("您本次的得分是：\n" \
        "抽象：", max(Abstraction), "\n" \
        "控制：", max(FlowControl), "\n" \
        "交互：", max(UserInteractivity), "\n" \
        "逻辑思维：", max(LogicalThinking), "\n" \
        "数据呈现：", max(DataRepresentation), "\n" \
        "您的总分是：", zongfen, "\n")
        return [max(Abstraction),max(FlowControl),max(UserInteractivity),max(LogicalThinking),max(DataRepresentation)]
        # liat_value = [sname, max(Abstraction), max(FlowControl), max(UserInteractivity), max(LogicalThinking),
        #                       max(DataRepresentation), zongfen]
        # with open("score1206.csv", "ab") as csvfile:
        #     writer = csv.writer(csvfile)
        #     if NUM == 1:
        #         writer.writerow(list_name)
        #         NUM = NUM + 1
        #     writer.writerow(liat_value)

