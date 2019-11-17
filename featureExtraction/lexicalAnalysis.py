import sys
import re

#保留字
key_word = ['abstract','assert','boolean','break','byte',
      'case','catch','char','class','const',
      'continue','default','do','double','else',
      'enum','extends','final','finally','float',
      'for','goto','if','implements','import',
      'instanceof','int','interface','long','native',
      'new','package','private','protected','public',
      'return','short','static','strictfp','super',
      'switch','synchronized','this','throw','throws',
      'transient','try','void','volatile','while',
      'pass','None','in','True','False','def']

#运算符
operator = ['+','-','*','/','%','++','--','+=','-=','+=','/=',#算术运算符 0-10 如果修改了算术运算符个数，那么要更新main.py的161附近分支逻辑
      '==','!=','>','<','>=','<=',#关系运算符 11-16 如果修改了关系运算符个数，那么要更新main.py的163附近分支逻辑
      '&','|','^','~','<<','>>','>>>',#位运算符 17-23
      '&&','||','!',#逻辑运算符24-26
      '=','+=','-=','*=','/=','%=','<<=','>>=','&=','^=','|=',#赋值运算符
      '?:']#条件运算符

#界符
delimiters = ['{','}','[',']','(',')','.',',',':',';','\\']

#标识符表
identifier = []


#错误标识符
error_word = []

#检测多字符串
def checkOperator(line,s,i,word_line):
    s = s + line[i + 1]
    if s not in operator:
        word_line.append({s[:-1]: len(key_word) + len(delimiters) + operator.index(s[:-1])})
        return i
    else:
        return checkOperator(line,s,i+1,word_line)


#预处理
def filterResource(file,new_file):
  f2 = open(new_file,'w+')
  txt = ''.join(open(file,'r').readlines())
  deal_txt = re.sub(r'\/\*[\s\S]*\*\/|\/\/.*','',txt)
  for line in deal_txt.split('\n'):
      line = line.strip()
      line = line.replace('\\t','')
      line = line.replace('\\n','')
      if not line:
        continue
      else:
        f2.write(line+'\n')
  f2.close()
  return sys.path[0]+'\\'+ new_file

def preprocessLines(line):
    #删掉输出中的换行符和制表符
    line = line.replace('\\t', ' ')
    line = line.replace('\\n', ' ')
    return line

def searchReserve(word):
    for item in key_word:
        if item == word:
            return True
    return False


def Scan(line):
    # print(line)
    line = line + ' '
    i = 0
    word_line = []
    word = []
    while i < len(line):
        word += line[i]
        # print(word)
        if line[i] == ' ' or line[i] in delimiters or line[i] in operator:
            if word[0].isalpha() or word[0] == '$' or word[0] == '_':
                word = word[:-1]
                word = ''.join(word)
                # print(word)
                # print('\n' * 10)
                # print(''.join(word))
                # print('\n'*10)
                if word in key_word:
                    # 保留字
                    word_line.append({'key_word': key_word.index(word)})
                else:
                    # 标识符
                    if word not in identifier:
                        identifier.append(word)
                    word_line.append({word: identifier.index(word)})
            # 常数
            elif ''.join(word[:-1]).isdigit():
                word_line.append({''.join(word[:-1]): -1})

            # 字符是界符
            if line[i] in delimiters:
                word_line.append({line[i]: len(key_word) + delimiters.index(line[i])})
            # 字符是运算符
            elif line[i] in operator:
                s = line[i] + line[i + 1]
                if s in operator:
                    i += 1
                    i = checkOperator(line,s,i,word_line)
                    print(line,i)
                else:
                    word_line.append({line[i]: len(key_word) + len(delimiters) + operator.index(line[i])})
            word = []
        i += 1
    # print("word_line")
    # print(word_line)
    # print("identifier")
    # print(identifier)
    # print("error_word")
    # print(error_word)
    # token.append(word_line)
    return word_line,identifier


# def check(number):
#   hanzi = ''
#   q = len(key_word)
#   w = len(delimiters)
#   e = len(operator)
#   if 0<number<=q:
#     hanzi = '保留字'
#   elif q<number <= q+w:
#     hanzi = '界符'
#   elif q+w<number <=q+w+e:
#     hanzi = '运算符'
#   elif number == -1:
#     hanzi ='常数'
#   elif number == -2:
#     hanzi ='标识符'
#   return hanzi
