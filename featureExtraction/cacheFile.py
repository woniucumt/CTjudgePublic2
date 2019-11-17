CACHE_FILE = 'Counter.dump'
CACHE_DUMPER, CACHE_GEN = None, None
from json import dump, JSONDecoder

def CounterDump(data):
    global CACHE_DUMPER
    if CACHE_DUMPER == None:
        CACHE_DUMPER = open(CACHE_FILE, 'w')
    dump(data, CACHE_DUMPER)


def ParseJson(jsonData):
    endPos = 0
    while True:
        jsonData = jsonData[endPos:].lstrip()
        try:
            pyObj, endPos = JSONDecoder().raw_decode(jsonData)
            yield pyObj
        except ValueError:
            break
def CounterLoad():
    global CACHE_GEN
    if CACHE_GEN == None:
        CACHE_GEN = ParseJson(open(CACHE_FILE, 'r').read())
    try:
        return next(CACHE_GEN)
    except StopIteration as e:
        return []
def shouldUseCache(keep, detail, basename, cache, target):
    if not cache:  #未指定启用缓存
        return False
    try:
        (_keep, _detail, _basename, _target) = CounterLoad()
    except (IOError, EOFError, ValueError): #缓存文件不存在或内容为空或不合法
        return False
    if keep == _keep and detail == _detail and basename == _basename \
       and sorted(target) == sorted(_target):
        return True
    else:
        return False
