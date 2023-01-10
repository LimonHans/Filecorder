#coding=utf-8
###############################
#   HansLimon on 2021/11/14   #
#                             #
#       for public use        #
#                             #
#     CopyLEFT Mongrokey      #
###############################
import argparse
import email
import imaplib
import os
import smtplib
import sys
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

local_position = sys.path[0]
customname_content = "Content"
customname_attachment = ""

def send(args):
    full_mail = MIMEMultipart()
    if args.errormode:
        full_mail.attach(MIMEText(
            'An error occurred while trying to read your file.'
            ' The file has been deleted and please contact hslimonffs@outlook.com immediately.',
            'plain', 'utf-8'))
    else:
        with open(os.path.join(local_position, f"{customname_content}.txt"), "r", encoding="utf-8") as f:
            full_mail.attach(MIMEText(f.read(), 'plain', 'utf-8'))
            f.close()
    if args.attachment:
        mail_file = MIMEBase('application', 'octet-stream')
        with open(os.path.join(local_position, customname_attachment), "rb") as f:
            mail_file.set_payload(f.read())
        encode_base64(mail_file)
        mail_file.add_header('Content-Disposition', 'attachment', filename=customname_attachment)
        full_mail.attach(mail_file)

    ################################################
    # You're supposed to fill the following parts. #
    # Here is an example:                          #
    # 'From' = hanslimon<myemail@domain>           #
    # 'To' = receiver<email@domain2>               #
    ################################################
    full_mail['From'] = ""
    full_mail['To'] = args.prefix + "<" + args.name + ">"
    full_mail['Subject'] = args.subject
    full_mail['Date'] = formatdate()

    try:
        mail = smtplib.SMTP_SSL(host="", port=465)# host is the smtp server, it's usually smtp.[server]
    except:
        print("Send failed at [connect to server]", end="|")
        return
    try:
        mail.login(user="", password="")
        Eaddress = []
        Eaddress = args.name.split(" ")
        #print(Eaddress)
        mail.sendmail(from_addr="", to_addrs=Eaddress, msg=full_mail.as_string())
    except:
        print("Send failed at [sendmail]", end="|")
    mail.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default=argparse.SUPPRESS)# 目标邮件地址
    parser.add_argument("--prefix", type=str, default="Unknown")# 称呼
    parser.add_argument("--subject", type=str, default="默认主题")# 主题
    parser.add_argument("--attachment", action="store_true")# 是否有附件
    parser.add_argument("--errormode", action="store_true")# 错误模式
    args = parser.parse_args()

    print("PreparedToRun", end="|")

    if not hasattr(args, "name"):
        print("Error: No receiver OR No sender")
        exit(412)

    send(args)
    print("Process Completed")

    exit(0)