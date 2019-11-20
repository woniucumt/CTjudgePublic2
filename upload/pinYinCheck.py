#by https://www.cnblogs.com/aloiswei/p/8976596.html

def pinyin_or_word(string,pinyin_Lib):
    # print(pinyin_Lib)
    '''
    judge a string is a pinyin or a english word.
    pinyin_Lib comes from a txt file.
    '''
    string = string.lower()
    stringlen = len(string)
    result = []
    while True:
        i_list = []
        for i in range(1,stringlen+1):
            if string[0:i] in pinyin_Lib:
                i_list.append(i)
        if len(i_list) == 0:
            # print("这可能是一个英语单词！")
            temp_result = []
            break
        else:
            temp = max(i_list)
            result.append(string[0:temp])
            string = string.replace(string[0:temp],'')
            stringlen = len(string)
            if stringlen == 0:
#                print("这是一个拼音！")
#                print(result)
                break
    return result
