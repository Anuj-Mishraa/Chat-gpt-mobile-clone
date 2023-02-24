import requests
import time
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

model = "text-davinci-003"
class ErrorMessage(BoxLayout):

    def __init__(self,tex, **kwargs):
        super().__init__(**kwargs)
        # Create a label to show the error message 
        self.label = Label(text=tex, font_size=20, size_hint=(1, 0.2),pos_hint={"x": 0.6,"y":0.4})
        # Add the label to the layout
        self.bt = Button(text="Login",size_hint=(0.2,0.2),pos_hint={"x": 0.2,"y":0.4},on_press =self.show)
        self.add_widget(self.label)
        self.add_widget(self.bt)
        self.error_message = None

    # Display the message box given an error message string
    def show(self,instance):
        app1 = App.get_running_app()    
        app1.root.clear_widgets()  
        Log = LoginWindow()
        app1.root_window.add_widget(Log) 

class ErrorPopup(Popup):
        pass

class LoginWindow(Popup):
    username = StringProperty('')
    api_key = StringProperty('')

    def login_and_enter_chat(self):
        username_input = self.ids.username_input
        api_key_input = self.ids.api_key_input

        username = username_input.text.strip()
        api_key = api_key_input.text.strip()
        app = App.get_running_app()
        app.username = username + " GPT"
        app.api_key = api_key
        if not username or not api_key:
            return
        url = 'https://api.openai.com/v1/completions' 

        
        response = requests.post(
            f"https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {app.api_key}"
            },
            json={
                "model": model,
                "prompt": "prompt",
                "max_tokens": 100
            }).json()
        try:
            res = response['choices'][0]['text'][1:]
            app.root_window.remove_widget(self)
            chat_window = ChatWindow()
            app.root_window.add_widget(chat_window)
        except:
            errorAlert = ErrorPopup(title='Error', content=ErrorMessage("Invailed Key Login again"))
            errorAlert.open()
        


class ChatWindow(BoxLayout):
    chat_input = ObjectProperty()
    chat_history = ObjectProperty()
    def __init__(self, **kwargs):
        super(ChatWindow, self).__init__(**kwargs)
        self.width_mes = Window.width - 200
        self.chat_history.text = "ChatGpt: Hello, how can I assist you today?\n"

    def send_message(self):
        prompt = self.chat_input.text
        if prompt:
            self.chat_input.text = ""
            response = self.chat_with_chatgpt(prompt)
            self.chat_history.text += f"You: {prompt}\n\n"
            self.chat_history.text += f"ChatGpt: {response}\n\n"
    
    def chat_with_chatgpt(self, prompt):
        app = App.get_running_app()
        res = requests.post(
            f"https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {app.api_key}"
            },
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": 100
            }).json()
        
        return res['choices'][0]['text'][1:]

    def clear_chat(self):
        self.chat_history.text = ""


class ChatGptApp(App):
    Builder.load_file('test.kv')
    username = ''
    api_key = ''

    def build(self):
        return LoginWindow()

if __name__ == '__main__':
    ChatGptApp().run()
