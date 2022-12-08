from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
import os
import ast


class MenuScreen(Screen):
    def __init__(self, **kw):
        super(MenuScreen, self).__init__(**kw)
        box = FloatLayout()
        box.add_widget(Label(text='Добро пожаловать! В Plusani',
                             pos_hint={'x': .38, 'y': .65},
                             size_hint=(.25, .25)
                             ))
        box.add_widget(Button(text='Начать!',
                              pos_hint={'x': .38, 'y': .25},
                              size_hint=(.25, .25),
                              on_press=lambda x: set_screen('add_person')

                              ))
        self.add_widget(box)


class AddPerson(Screen):

    def buttonClicked(self, btn1):
        if not self.txt1.text:
            return
        self.app = App.get_running_app()
        self.app.user_data = ast.literal_eval(
            self.app.config.get('General', 'user_data'))
        self.app.user_data[self.txt1.text.encode('u8')] = int()

        self.app.config.set('General', 'user_data', self.app.user_data)
        self.app.config.write()

        text = "Последней добавленный человек  " + self.txt1.text
        self.result.text = text
        self.txt1.text = ''

    def person_clear(self, clear_button, *largs):
        self.app = App.get_running_app()
        self.delet = ast.literal_eval(
            self.app.config.get('General', 'user_data'))

        if not self.delet:
            return
        else:
            open('plusani.ini', 'w').close()
            return SortedListAccounts.on_leave

    def __init__(self, **kw):
        super(AddPerson, self).__init__(**kw)
        box = BoxLayout(orientation='vertical')

        self.txt1 = TextInput(text='', multiline=False, height=dp(40),
                              size_hint_y=None, hint_text="Имя человека")
        box.add_widget(self.txt1)
        btn1 = Button(text="Добавить человека", size_hint_y=None, height=dp(40))
        btn1.bind(on_press=self.buttonClicked)
        box.add_widget(btn1)

        clear_button = Button(text='Очистка',
                              on_press=self.person_clear,
                              size_hint_y=None, height=dp(40))
        box.add_widget(clear_button)

        back_button = Button(text='Начать счет!', on_press=lambda x:
        set_screen('list_accounts'), size_hint_y=None, height=dp(40))
        box.add_widget(back_button)
        self.result = Label(text='')
        box.add_widget(self.result)
        self.add_widget(box)


class SortedListAccounts(Screen):
    def __init__(self, **kw):
        super(SortedListAccounts, self).__init__(**kw)

    def add_rects(self, label, count, *largs):
        label.text = str(int(label.text) + count)

    def on_enter(self):  # Будет вызвана в момент открытия экрана
        self.box_layout = FloatLayout(size=(100, 100))

        self.layout = GridLayout(cols=3, spacing=10, size_hint_y=.01, pos=(-25, 590))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        back_button = Button(text='< Назад в настройки',
                             on_press=lambda x: set_screen('add_person'),
                             size_hint_y=None, height=dp(40))
        root = RecycleView(size_hint=(1, None), size=(Window.width,
                                                      Window.height))
        root.add_widget(self.box_layout)

        dic_foods = ast.literal_eval(
            App.get_running_app().config.get('General', 'user_data'))

        if not dic_foods:
            lab = Label(text='Список пуст', pos=(0, 50))
            self.box_layout.add_widget(lab)

        else:
            for f, d in sorted(dic_foods.items(), key=lambda x: x[1]):
                fd = f.decode('u8') + '!'
                lbl = Label(text=fd, size_hint_y=None, height=dp(40))
                label = Label(text='0')
                btn = Button(text='+ 1 Бал', on_press=partial(self.add_rects, label, 1))
                self.layout.add_widget(lbl)
                self.layout.add_widget(label)
                self.layout.add_widget(btn)

        self.box_layout.add_widget(back_button)
        self.add_widget(root)

        self.box_layout.add_widget(self.layout)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.layout.clear_widgets()  # очищаем список


def set_screen(name_screen):
    sm.current = name_screen


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AddPerson(name='add_person'))
sm.add_widget(SortedListAccounts(name='list_accounts'))


class PlusaniApp(App):
    def __init__(self, **kvargs):
        super(PlusaniApp, self).__init__(**kvargs)
        self.config = ConfigParser()

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def set_value_from_config(self):
        self.config.read(os.path.join(self.directory, 'plusani.ini'))
        self.user_data = ast.literal_eval(self.config.get(
            'General', 'user_data'))

    def get_application_config(self):
        return super(PlusaniApp, self).get_application_config(
            'plusani.ini'.format(self.directory))

    def build(self):
        return sm


if __name__ == '__main__':
    PlusaniApp().run()