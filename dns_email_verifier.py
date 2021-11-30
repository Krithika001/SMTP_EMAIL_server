# -*- coding: utf-8 -*-
"""
Email server using SMTP
19pd10-Divya Sivaraman
19d19-KRITHIKA
"""


import re
import smtplib
import dns.resolver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter
from tkinter import *
import imaplib
import email

def verify_email(addressToVerify):
        
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not(re.search(regex,addressToVerify)):
          raise ValueError('email seems invalid!')
             
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)
    
    records = dns.resolver.resolve(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    server = smtplib.SMTP('smtp.gmail.com',25)
    fromAddress = 'kanirajan@gmail.com'
    
    #print(mxRecord)
    server.connect(mxRecord)
    # SMTP Conversation
    server.helo(server.local_hostname) 
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()
    
    print("code:",code)
    print("message:",message)
    
    # Assume SMTP response 250 is success
    if code == 250:
    	print('Success')
        
    else:
    	print('Bad')


def send_message():
    verify_email(toaddr.get())

    msg = MIMEMultipart()
    
    msg['From'] = fromaddr.get()
    msg['To'] = toaddr.get()
    msg['Subject'] = "This is mail send through SMTP!!!"
    msg.attach(MIMEText(body.get(), 'plain'))
    filename = "G:/sem 5/DC/bmp_13.png"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr.get(),password.get())
    text = msg.as_string()
    
    server.send_message(msg)
    root=Tk()
    root.title("Mail Sent")
    
    heading = Label(text="Python Email Sending ",bg="black",fg="white",font="10",width="200",height="3")
    
    heading.pack()
    root.geometry("200x200")
    label = Label(root, text="Mail Sent")
    label.place(x=50,y=50)
    
    print("Mail Sent!!!")
    server.quit()

def get_inbox():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(fromaddr.get(), password.get())
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    root=Tk()
    root.title("Inbox")
    
    heading = Label(text="Unseen Messages ",bg="black",fg="white",font="10",width="700",height="3")
    
    heading.pack()
    root.geometry("700x200")
    label = Label(root, text=my_message)
    label.place(x=15,y=50)
    
    print(my_message)    
    
app=Tk()
app.geometry("500x580")

app.title("Python Mail Send App")

heading = Label(text="Python Email Sending ",bg="black",fg="white",font="10",width="500",height="3")

heading.pack()


FromAdd = Label(text="Your email address :")
Pass = Label(text="Email Password :")
ToAdd=Label(text="To Address : ")
B=Label(text="Body of email : ")

FromAdd.place(x=15,y=70)
Pass.place(x=15,y=140)
ToAdd.place(x=15,y=210)
B.place(x=15,y=280)

froma = StringVar()
passw =StringVar()
toa =StringVar()
bo=StringVar()

fromaddr = Entry(textvariable=froma,width="30")
password = Entry(textvariable=passw,width="30",show='*')
toaddr = Entry(textvariable=toa,width="30")
body = Entry(textvariable=bo,width="30")

fromaddr.place(x=15,y=100)
password.place(x=15,y=180)
toaddr.place(x=15,y=250)
body.place(x=15,y=310)

button = Button(app,text="Send Message",command=send_message,width="30",height="2",bg="grey")

button.place(x=15,y=360)

b=Button(app,text="Show Inbox",command=get_inbox,width="30",height="2",bg="grey")
b.place(x=15,y=410)

Q=Button(app,text="Quit",command=app.quit,width="30",height="2",bg="grey")
Q.place(x=15,y=460)

mainloop() 
