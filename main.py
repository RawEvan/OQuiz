# -*- coding: utf-8 -*-
import kivy
import time
from random import randint

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock

from quiz_client import Client
client = Client()


kivy.resources.resource_add_path("")

class Selection(Label):
    selection_str = StringProperty(None)
    is_answer = BooleanProperty(False)

    def on_touch_down(self, touch):
        if not self.parent.parent.finish and \
                self.collide_point(touch.x, touch.y):
            self.font_size = '40sp'
            if not self.is_answer:
                self.parent.parent.wrong_num += 1
                self.selection_str = 'Error'
                if self.parent.parent.wrong_num >= 3:
                    self.parent.parent.finish = True
            else:
                self.parent.parent.finish = True
        else:
            return False


class Quiz(BoxLayout):
    question = ObjectProperty(None)
    question_str = StringProperty()
    selections_lay = ObjectProperty(None)
    title_lay = ObjectProperty(None)
    start_btn = ObjectProperty(None)
    finish = BooleanProperty(False)
    start_time = time.time()
    status = 'stopped'
    mark_num = 0
    wrong_num = 0
    info = StringProperty(u'得分：0')

    def start_game(self):
        self.start_time = time.time()
        self.mark_num = 0
        self.wrong_num = 0

    def start_quiz(self):
        self.wrong_num = 0
        self.start_btn.text = 'Next'
        if self.status == 'stopped':
            self.status = 'playing'
            self.start_time = time.time()
        # quiz = client.get_quiz()
        quiz = client.get_lol_quiz()
        self.question_str = quiz['question']
        self.selections_lay.clear_widgets()
        for selec in quiz['selections']:
            selection = Selection(
                selection_str= selec['string'],
                rotation=randint(-30, 30),
                is_answer=selec['is_answer'])
            self.selections_lay.add_widget(selection)

    def judge(self, dt):
        self.set_info()
        if self.finish:
            # doens't work?
            self.mark_num += 1
            time.sleep(0.5)
            self.finish = not self.finish
            self.start_quiz()
        if self.status == 'playing' and \
                time.time() - self.start_time >= 60:
            over_label = Label(text='Game Over', font_size='50sp')
            self.start_btn.text = 'Restart'
            self.selections_lay.clear_widgets()
            self.question_str = u''
            self.selections_lay.add_widget(over_label)
            self.status = 'stopped'
            self.start_game()

    def set_info(self):
        self.info = u'得分： ' + str(self.mark_num)
        if self.status == 'playing':
            self.info = self.info + u'    剩余时间：' + str(60 - int(time.time() - self.start_time))


class QuizApp(App):
    def build(self):
        quiz = Quiz()
        Clock.schedule_interval(quiz.judge, 1.0/60.0)
        return quiz


if __name__ == '__main__':
    QuizApp().run()
