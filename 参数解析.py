# coding:utf-8

import argparse


parse = argparse.ArgumentParser()
#parse.add_argument('echo',help="echo is first test")
parse.add_argument('-p',help='添加测试')
args = parse.parse_args()
#print args.echo
if args.p:
    print args.p