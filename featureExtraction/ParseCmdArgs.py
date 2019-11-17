import sys
import argparse

def ParseCmdArgs(argv=sys.argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] target',
                      description='Count lines in code files.')
    parser.add_argument('target', nargs='*',
           help='space-separated list of directories AND/OR files')
    parser.add_argument('-k', '--keep', action='store_true',
           help='do not walk down subdirectories')
    parser.add_argument('-d', '--detail', action='store_true',
           help='report counting result in detail')
    parser.add_argument('-b', '--basename', action='store_true',
           help='do not show file\'s full path')
##    sortWords = ['0', '1', '2', '3', '4', '5', 'file', 'code', 'cmmt', 'blan', 'ctpr', 'name']
##    parser.add_argument('-s', '--sort',
##        choices=[x+y for x in ['','r'] for y in sortWords],
##        help='sort order: {0,1,2,3,4,5} or {file,code,cmmt,blan,ctpr,name},' \
##             "prefix 'r' means sorting in reverse order")
    parser.add_argument('-s', '--sort',
           help='sort order: {0,1,2,3,4,5} or {file,code,cmmt,blan,ctpr,name}, ' \
             "prefix 'r' means sorting in reverse order")
    parser.add_argument('-o', '--out',
           help='save counting result in OUT')
    parser.add_argument('-c', '--cache', action='store_true',
           help='use cache to count faster(unreliable when files are modified)')
    parser.add_argument('-v', '--version', action='version',
           version='%(prog)s 3.0 by xywang')
    args = parser.parse_args()
    return (args.keep, args.detail, args.basename, args.sort, args.out, args.cache, args.target)
