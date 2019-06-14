# -*- coding: utf-8 -*-
import mimetypes
import mysmtplib
import theater_info
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def sendGmail(bookmark):
#global value
    host = "smtp.gmail.com" # Gmail STMP 서버 주소.
    port = "587"
    htmlFileName = "logo.html"

    senderAddr = "dpldp92@gmail.com"     # 보내는 사람 email 주소.
    recipientAddr = "cjpark0119@naver.com"   # 받는 사람 email 주소.

    msg = MIMEBase("multipart", "alternative")
    msg['Subject'] = "Movie"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    # MIME 문서를 생성합니다.
    info_dic = bookmark
    info_str = ''
    theater_dic = list()

    for n in range(len(info_dic)):
        theater_dic = theater_info.GetMovieInfo(info_dic[n])['info']

        if theater_dic:
            info_str = '['+str(info_dic[n]['name'])+']'
            MovieHtmlPart = MIMEText(info_str, 'html', _charset='UTF-8')
            msg.attach(MovieHtmlPart)
            for i in range(len(theater_dic)):
                info_str = '○' + theater_dic[i]['movie'] + ' :'
                for n in range(len(theater_dic[i]['time'])):
                    info_str += ' [' + theater_dic[i]['time'][n] + ']'
                MovieHtmlPart = MIMEText(info_str, 'html', _charset='UTF-8')
                msg.attach(MovieHtmlPart)
        info_str = ''
        MovieHtmlPart = MIMEText(info_str, 'html', _charset='UTF-8')
        msg.attach(MovieHtmlPart)
        theater_dic.clear()

    #MovieHtmlPart = MIMEText(info_str, 'html', _charset = 'UTF-8' )
    #msg.attach(MovieHtmlPart)
    # 만들었던 mime을 MIMEBase에 첨부 시킨다.
    #msg.attach(MovieHtmlPart)

    # 메일을 발송한다.
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("dpldp92@gmail.com", "")
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()













































































