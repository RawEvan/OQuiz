# -*- coding: utf-8 -*-
import random
from random import randint
from utils.get_lol_data import get_file
import json


SEL_NUM = 9
CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/data/zh_CN/champion.json',
CHAMPION_PATH = 'json/champion.json'


class Client():
    def get_test_quiz(self):

        quiz = {'question': None, 'selections': []}
        quiz['question'] = 'question' + str(randint(0, 100))
        for i in range(SEL_NUM):
            quiz['selections'].append({
                'string': 'selection' + str(randint(0, 100)),
                'is_answer': False})
        quiz['selections'][randint(0, SEL_NUM - 1)]['is_answer'] = True
        # quiz['answer'] = quiz['selections'][1]
        return quiz

    def get_lol_quiz(self):
        f = get_file(CHAMPION_URL, CHAMPION_PATH)
        chmp_data = json.loads(f)
        chmps = chmp_data['data']
        chosen_chmps = []
        for i in range(SEL_NUM):
            while 1:
                chosen_chmp = random.choice(chmps.keys())
                if chosen_chmp not in chosen_chmps:
                    chosen_chmps.append(chosen_chmp)
                    break
        right_chmp = chosen_chmps[0]
        # set quiz
        quiz = {'question': None, 'selections': []}
        question = chmps[right_chmp]['blurb'].replace(
            chmps[right_chmp]['title'], u'[b]这个人[/b]')
        question = question.replace(u'。', u'。\n')
        question = question.replace(u'<br>', u'')
        quiz['question'] = question
        quiz['selections'].append({
            'string': right_chmp,
            'is_answer': True})
        for chmp in chosen_chmps[1:]:
            quiz['selections'].append({
                'string': chmp,
                'is_answer': False})
        return quiz


if __name__ == '__main__':
    client = Client()
    print client.get_lol_quiz()
