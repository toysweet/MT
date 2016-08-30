#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__='ToySweet'

import socket
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import optparse
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )




def sendMalifalse(ip):
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="1220766607@qq.com"    #用户名
    mail_pass=""   #口令
    sender = '1220766607@qq.com'
    receivers = ['670417360@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    subject = times + u'生产服务器:' + ip + u'无响应'
    message = MIMEText(subject, 'plain', 'utf-8')
    message['From'] = Header("安全检查", 'utf-8')
    message['To'] =  Header("安全部门><\"test=\"\"", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP(timeout=30)
        smtpObj.connect(mail_host, 587)    # 不加密为25 加密要自定义SMTP端口号
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print times + u"邮件发送成功"
        global SENDSTATUS
        SENDSTATUS = 1
        print SENDSTATUS
    except smtplib.SMTPException,e:
        print times + u"Error: 无法发送邮件 " + str(e)

def sendMalitrue(ip):
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="1220766607@qq.com"    #用户名
    mail_pass=""   #口令
    sender = '1220766607@qq.com'
    receivers = ['670417360@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    subject = times + u'生产服务器:' + ip + u'恢复'
    message = MIMEText(subject, 'plain', 'utf-8')
    message['From'] = Header("安全检查", 'utf-8')
    message['To'] =  Header("安全部门><\"test=\"\"", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP(timeout=30)
        smtpObj.connect(mail_host, 587)    # 不加密为25 加密要自定义SMTP端口号
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print times + u"邮件发送成功"
        global SENDSTATUS
        SENDSTATUS = 0
        print SENDSTATUS
    except smtplib.SMTPException,e:
        print times + "Error: 无法发送邮件 " + str(e)


def reqHttp(url):
    try:
        r = requests.get(url)
        try:
            with open("log.txt",'a') as f:
                f.write(times + "连接到: "+str(url)+'\n')
        except Exception,ex:
            print "读写错误:"+str(ex)
        if r.status_code == 200:
            if SENDSTATUS == 1:
                sendMalitrue(url)
                return
            else:
                return
        else:
            print u"连接错误: "+str(r.status_code)
            if SENDSTATUS == 0:
                sendMalifalse(url)
                return
            else:
                return
    except Exception,ex:
        try:
            with open("log.txt",'a') as f:
                f.write(times+"连接错误: "+str(ex)+'\n')
        except Exception,e:
            print "读写错误: "+str(e)
        if SENDSTATUS == 0:
            sendMalifalse(url)
            return
        else:
            return

#reqHttp('https://www.toysweet.com/123.php')


def reqSocket(ip,port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip,port))
        #banner = s.recv(1024)
        try:
            with open("log.txt",'a') as f:
                f.write(times+"连接到: "+ip+':'+str(port)+'\n')
        except Exception,ex:
            print "读写错误: "+str(ex)
        if SENDSTATUS == 1:
            sendMalitrue(ip+':'+str(port))
            return
        else:
            return
    except Exception ,e:
        try:
            with open("log.txt",'a') as f:
                f.write(times+"连接错误: "+str(e)+'\n')
        except Exception,ex:
            print "读写错误:"+str(ex)
        if SENDSTATUS == 0 :
            sendMalifalse(ip+':'+str(port))
            return
        else:
            return


def main():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    global times
    times = time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
    global SENDSTATUS
    SENDSTATUS = 0
    parser = optparse.OptionParser('usage %prog -u <target url> -H <target host> -p <target port> -r <file>')
    parser.add_option('-u',dest='url',type='string',help='specify target url')
    parser.add_option('-H',dest='host',type='string',help='specify target host')
    parser.add_option('-p',dest='port',type='int',help='specify target port')
    parser.add_option('-r',dest='file',type='string',help='specify target port read for file')
    (options, args) = parser.parse_args()
    url = options.url
    host = options.host
    port = options.port
    # if (host == None) | (port == None):
    #     print parser.usage
    #     exit(0)
    if (url != None) and (host == None and port == None):
        while True:
            print u"开启检查"
            #reqHttp('https://www.toysweet.com/')
            reqHttp(url)
            time.sleep(60)
    elif(host !=None and port !=None and url==None):
        while True:
            print u"开启检查"
            #reqHttp('https://www.toysweet.com/')
            reqSocket(host,port)
            time.sleep(60)
    else:
        print parser.usage
        exit(0)
if __name__ == '__main__':
    main()

