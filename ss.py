import requests
import time
import sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from functools import partial
import threading

payload = "{\"action\":\"click\",\"amount\":3}"
headers = {
    'user-agent': "python script | https://github.com/Hitsounds/twitch.tv-live-pet-bot",
    'accept': "application/json, text/javascript, */*; q=0.01",
    'accept-language': "en-US,en;q=0.5",
    'accept-encoding': "gzip, deflate, br",
    'content-type': "application/json",
    'authorization': "I think not.",
    }


class AuthScreen(GridLayout):
        def request(self, lab, runout):
                while True:
                        headers["authorization"] = self.auth.text
                        url = "https://pet.porcupine.tv/channel/{}/message".format(self.chan.text)
                        res = requests.request("POST", url, data=payload, headers=headers)
                        data = res.text
                        self.t = str("Points : "+ str(self.points))
                        lab.text = self.t
                        try:
                                if data == "Unauthorized":
                                        runout.text = "Auth : Unauthorised"        
                                elif data[12] == "0" or data[12] == "1":
                                        self.points = self.points + 30
                                        runout.text = "Auth : Authorised"
                        except IndexError:
                                runout.text = "Auth : Authorised"
                        time.sleep(0.005)
                           

        def quit(self, btn):
                App.get_running_app().stop()                


        def __init__(self, **kwargs):
                super(AuthScreen, self).__init__(**kwargs)
                self.points = 0
                self.cols = 2
                self.add_widget(Label(text='Channel ID'))
                self.chan = TextInput(multiline=False)
                self.add_widget(self.chan)
                self.chan.text = "148072511"
                self.run = Label(text='Auth : Unauthorised')
                self.add_widget(self.run)    
                self.auth = TextInput(multiline=True)
                self.add_widget(self.auth)
                self.auth.text = "E.g. Bearer sdasds231as..."
                self.res = Label(text='Points :', font_size=35)
                self.add_widget(self.res)
                self.btn1 = Button(text='Quit')
                self.btn1.bind(on_press=self.quit)
                self.add_widget(self.btn1)
                self.thread = threading.Thread(target=partial(self.request, self.res, self.run), daemon=True)
                self.thread.start()

class A_App_About_My_UncleApp(App):
        def build(self):
                return AuthScreen()

A_App_About_My_UncleApp().run()

print("Thank you for using this app!")
