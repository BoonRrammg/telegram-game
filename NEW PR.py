#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import json
import telebot

class mob:
    def __init__(self, hp=100, damage=100, damage_multiply=0.0, stun_chance=0.0, damage_return=0.0, no_magic=False, weakness=0.0, drop=tuple([0, 0, 0, 0, 0])):
        self.hp = hp
        self.damage = damage
        self.damage_multiply = damage_multiply
        self.stun_chance = stun_chance
        self.damage_return = damage_return
        self.no_magic = no_magic
        self.stun = 0
        self.weakness = weakness
        self.drop = list(drop)
        self.maxhp = hp

    def copy(self):
        k = 1
        return mob(self.hp * k, self.damage * k, self.damage_multiply, self.stun_chance, self.damage_return,
                   self.no_magic, self.weakness, self.drop)

    def attack(self, enemy):
        damag = self.damage * random.randint(90, 110) / 100
        enemy.hp -= damag * (1 - enemy.shield if enemy.shield_time > 0 else 1)
        self.hp -= damag * (enemy.damage_return if enemy.return_time > 0 else 0)


class hero:
    def __init__(self, hp=100, mana=20, damage=100, potion=(1, 1, 1, 1, 1), ingredients=(0, 0, 0, 0, 0), stunned=0,
                 shield=0, shield_time=0, damage_return=0, return_time=0, weakness=0, rage=0, rage_time=0, lv=1):
        if type(hp) == hero:
            self.maxhp = hp.hp
            self.maxmana = hp.mana
            self.hp = hp.hp
            self.damage = hp.damage
            self.mana = hp.mana
            self.potion = list(hp.potion)
            self.stunned = hp.stunned
            self.shield = hp.shield
            self.shield_time = hp.shield_time
            self.damage_return = hp.damage_return
            self.return_time = hp.return_time
            self.weakness = hp.weakness
            self.rage = hp.rage
            self.rage_time = hp.rage_time
            self.ingredients = list(hp.ingredients)
            self.lv = hp.lv
        else:
            self.maxhp = hp
            self.maxmana = mana
            self.hp = hp
            self.damage = damage
            self.mana = mana
            self.potion = list(potion)
            self.stunned = stunned
            self.shield = shield
            self.shield_time = shield_time
            self.damage_return = damage_return
            self.return_time = return_time
            self.weakness = weakness
            self.rage = rage
            self.rage_time = rage_time
            self.ingredients = list(ingredients)
            self.lv = lv

    def drink(self, num):
        if num == 1:
            if self.potion[0] == 0:
                print('Такого зелья нет в инвентаре.')
                return
            else:
                self.hp = min(self.maxhp, self.hp + 50)
                self.potion[0] = self.potion[0] - 1
                return
        if num == 2:
            if self.potion[1] == 0:
                print('Такого зелья нет в инвентаре.')
                return
            else:
                self.hp = min(self.maxhp, self.hp + 150)
                self.potion[1] = self.potion[1] - 1
                return
        if num == 3:
            if self.potion[2] == 0:
                print('Такого зелья нет в инвентаре.')
                return
            else:
                self.mana = min(self.maxmana, self.mana + 10)
                self.potion[2] = self.potion[2] - 1
                return
        if num == 4:
            if self.potion[3] == 0:
                print('Такого зелья нет в инвентаре.')
                return
            else:
                self.mana = min(self.maxmana, self.mana + 30)
                self.potion[3] = self.potion[3] - 1
        if num == 5:
            if self.potion[4] == 0:
                print('Такого зелья нет в инвентаре.')
                return
            else:
                self.rage = 0.5
                self.rage_time += 12
                self.potion[4] = self.potion[4] - 1

                return
        print('Wrong input!')

    def attack(self, enemy):
        damag = self.damage * (1 + self.rage) * (max(0.1, 1 - self.weakness)) * random.randint(90, 110) / 100
        enemy.hp -= damag
        self.hp -= damag * enemy.damage_return

    def make_potion(self):
        print('Вам доступна варка следующих зелий:')
        one = False
        available = []
        if self.ingredients[0] > 0 and self.ingredients[2] > 0:
            one = True
            available.append('1')
            print('(1) Вы можете сварить малое зелье здоровья (+50 здоровья)')
        if self.ingredients[0] > 3 and self.ingredients[2] > 3:
            one = True
            available.append('2')
            print('(2) Вы можете сварить большое зелье здоровья (+150 здоровья)')
        if self.ingredients[1] > 0 and self.ingredients[3] > 0:
            one = True
            available.append('3')
            print('(3) Вы можете сварить малое зелье маны (+10 маны)')
        if self.ingredients[1] > 2 and self.ingredients[3] > 2:
            one = True
            available.append('4')
            print('(4) Вы можете сварить большое зелье маны (+30 маны)')
        if self.ingredients[3] > 1 and self.ingredients[4] > 1:
            one = True
            available.append('5')
            print('(5) Вы можете сварить зелье ярости (+50% урона)')
        if not one:
            print('Вы не можете сварить ни одного зелья')
            return
        print('Введите номер нужного зелья')
        x = input()
        if x not in available:
            print('Некорректный ввод')
            return
        x = int(x)
        if x == 1:
            self.ingredients[0] -= 1
            self.ingredients[2] -= 1
            self.potion[0] += 1
            print('Зелье сварено')
        if x == 2:
            self.ingredients[0] -= 3
            self.ingredients[2] -= 3
            self.potion[1] += 1
            print('Зелье сварено')
        if x == 3:
            self.ingredients[1] -= 1
            self.ingredients[3] -= 1
            self.potion[2] += 1
            print('Зелье сварено')
        if x == 4:
            self.ingredients[1] -= 3
            self.ingredients[3] -= 3
            self.potion[3] += 1
            print('Зелье сварено')
        if x == 5:
            self.ingredients[3] -= 2
            self.ingredients[4] -= 2
            self.potion[4] += 1
            print('Зелье сварено')


def generate(lv):
    typ = random.randint(1, 10)
    if typ in [1, 2] and lv != 33 and lv != 40 and lv != 50 and lv != 60:
        return [True, random.randint(1, 7)]
    seed = random.randint(0, 10000)
    if lv < 5:
        if seed < 5000:
            return [False, skeleton.copy(), 'Скелет']
        return [False, zombie.copy(), 'Зомби']
    if lv < 12:
        if seed < 3000:
            return [False, skeleton.copy(), 'Скелет']
        if seed < 6200:
            return [False, zombie.copy(), 'Зомби']
        return [False, crazy.copy(), 'Псих, особенность - удваивает урон после каждой атаки']
    if lv < 24:
        if seed < 3000:
            return [False, crazy.copy(), 'Псих, особенность - удваивает урон после каждой атаки']
        if seed < 6000:
            return [False, wizard.copy(), 'Маг, особенность - с малым шансом может оглушить']
        return [False, ghost.copy(), 'Призрак, особенность - уменшает урон каждой атакой']
    if lv < 33:
        if seed < 1000:
            return [False, pro_wizard.copy(), 'Жрец, особенности - запрещает магию на себе, отражает часть урона']
        if seed < 6000:
            return [False, wizard.copy(), 'Маг, особенность - с малым шансом может оглушить']
        if seed < 8000:
            return [False, electro_wizard.copy(), 'Электический маг, особенность - с БОЛЬШИМ шансом оглушает']
        return [False, ghost.copy(), 'Призрак, особенность - уменшает урон каждой атакой']
    if lv == 33:
        return [False, Boss.copy(),
                'Первый босс, особенности - ослабляет, может оглушить, возвращает часть урона, ослабляет атаку']
    if lv < 40:
        if seed < 1500:
            return [False, pro_wizard.copy(), 'Жрец, особенности - запрещает магию на себе, отражает часть урона']
        if seed < 3500:
            return [False, electro_wizard2.copy(), 'Электический маг, особенность - с БОЛЬШИМ шансом оглушает']
        if seed < 6500:
            return [False, wizard2.copy(), 'Маг, особенность - с малым шансом может оглушить']
        return [False, ghost2.copy(), 'Призрак, особенность - уменшает урон каждой атакой']
    if lv == 40:
        return [False, Boss2.copy(),
                'Второй босс, особенности - ослабляет, может оглушить, возвращает часть урона, ослабляет атаку']
    if lv < 50:
        if seed < 1500:
            return [False, pro_wizard.copy(), 'Жрец, особенности - запрещает магию на себе, отражает часть урона']
        if seed < 3500:
            return [False, electro_wizard2.copy(), 'Электический маг, особенность - с БОЛЬШИМ шансом оглушает']
        if seed < 6500:
            return [False, wizard3.copy(), 'Маг, особенность - с малым шансом может оглушить']
        return [False, ghost3.copy(), 'Призрак, особенность - уменшает урон каждой атакой']
    if lv == 50:
        return [False, Boss3.copy(),
                'Третий босс, особенности - ослабляет, может оглушить, возвращает часть урона, ослабляет атаку']
    if lv < 60:
        if seed < 1500:
            return [False, pro_wizard2.copy(), 'Жрец, особенности - запрещает магию на себе, отражает часть урона']
        if seed < 3500:
            return [False, electro_wizard2.copy(), 'Электический маг, особенность - с БОЛЬШИМ шансом оглушает']
        if seed < 6500:
            return [False, wizard3.copy(), 'Маг, особенность - с малым шансом может оглушить']
        return [False, ghost3.copy(), 'Призрак, особенность - уменшает урон каждой атакой']
    if lv == 60:
        return [False, Boss4.copy(), 'Четвертый босс, особенности - запрещает магию на себе. Удачи!']


def present(i):
    if i == 0:
        return 'лист шалфея'
    if i == 1:
        return 'магическая эссенция'
    if i == 2:
        return 'костяная мука'
    if i == 3:
        return 'прах сумасшествия'
    if i == 4:
        return 'пепел ярости'


def visualize(maxx, current, val1=-1, val2=-1):
    s = ''
    if val1 == -1:
        s = '🟢' * int(current * 49 / maxx)
    else:
        if current - val1 < 0:
            s = '🔴' * int(current * 49 / maxx)
        else:
            if current - val2 < 0:
                s = ('🟢' * max(int(((current - val1) * 49 / maxx) - 1), 1) + '🟡' + '🔴' * max(int(current * 49 / maxx), 1))
            else:
                s = ('🟢' * int((max((current - val2), 0) * 49 / maxx) - 1) + '🟡' + '🟡' * int((val2 - val1) * 49 / maxx) + '🟡' + '🔴' * int((val1) * 49 / maxx))
    res = s + '⚫' * int(abs(48 - len(s)))
    res += res[-1]
    ans = ''
    for i in range(0, 49):
        ans+=res[i]
        if i % 7 == 6:
            ans+='\n'
    return ans


'''
def playlv(id, player):

        while player.hp > 0 and enemy.hp > 0:
            print('Его характеристики: здоровье =', enemy.hp, 'урон =', enemy.damage)
            print('Ваши: здоровье =', player.hp, '/', player.maxhp, 'урон =',
                  player.damage * max(0.1, 1 - player.weakness) * (1 + player.rage), 'мана =', player.mana, '/',
                  player.maxmana, 'инвентарь =', player.potion, 'Ингредиенты =', player.ingredients)
            print('Визуализация здоровья врага после вашего удара:')
            visualize(maxhp, enemy.hp, player.damage * max(0.1, 1 - player.weakness) * (1 + player.rage) * 0.9,
                      player.damage * max(0.1, 1 - player.weakness) * (1 + player.rage) * 1.1)
            print('Вы ударили врага')
            print('Визуализация вашего здоровья после удара врага:')
            visualize(player.maxhp, player.hp, enemy.damage * 0.9, enemy.damage * 1.1)
            if random.randint(1, 10000) > enemy.stun_chance * 10000 or enemy.stun > 0:
                player.attack(enemy)
                if player.hp * 7.5 < player.maxhp:
                    print('ВНИМАНИЕ! НИЗКИЙ УРОВЕНЬ ЗДОРОВЬЯ!')
                print('Опции: 1. Пасс  2. Заклинание 3. Зелье 4. Варка зелья')
                if enemy.no_magic:
                    print('Враг запрещает использовать заклинания на себе')
                print('Внимание! Введение чисел, отличных от 2, 3, 4 означает пасс!')
                d = input()
                if d == '3':
                    print(player.potion)
                    print(
                        'Какое зелье?  1. здоровье +50 2. здоровье +150 3. мана +10 4. мана +30 5. +50% к урону на 12 ходов')
                    i = input()
                    if i not in ['1', '2', '3', '4', '5']:
                        print('Неправильно введено название зелья!')
                    else:
                        player.drink(int(i))
                if d == '2':
                    print(player.mana)
                    print(
                        'Какое заклинание? 1. Молния (10м) 2. Лечение(10м) 3. Оглушение(15м) 4. Поглощение врага(15м) 5. Магический щит(20м)' if enemy.hp < 300 else 'Какое заклинание? 1. Молния (10м) 2. Лечение(10м) 3. Оглушение(15м) 4. Магический щит(20м)')
                    i = input()
                    if i not in ['2', '4' if enemy.hp > 300 else '5'] and enemy.no_magic:
                        print('Некорректный ввод / Заклинание запрещено')
                    elif i not in ['1', '2', '3', '4', '5']:
                        print('Некорректный ввод')
                    else:
                        if enemy.hp > 300 and int(i) > 3:
                            i = int(i)
                            i += 1
                        player.magic(enemy, int(i), maxhp)
                if d == '4':
                    player.make_potion()
                player.rage_time = max(0, player.rage_time - 1)
                if player.rage_time == 0:
                    player.rage = 0
            else:
                print('Вас оглушили на 1 ход!')
            if enemy.stun < 1 and enemy.hp > 0:
                enemy.attack(player)
            enemy.damage += enemy.damage * enemy.damage_multiply if enemy.stun < 1 else 0
            enemy.stun -= 1
            player.shield_time -= 1
            player.weakness += enemy.weakness if enemy.stun < 1 else 0
            player.return_time -= 1
            player.hp = round(player.hp, 5)
            enemy.hp = round(enemy.hp, 5)
            print('\n \n \n \n \n \n')
            if player.shield_time > 0:
                print('Щит будет действовать еще', player.shield_time, 'раундов')
            if player.shield_time == 0:
                print('Щит кончился!')

        if player.hp < 1:
            print('Вы мертвы.')
            print(player.lv)
            input()
            sys.exit()
        else:
            print('Враг повержен!')
            for i in range(5):
                if enemy.drop[i] * 10000 > random.randint(0, 10000):
                    player.ingredients[i] += 1
                    print('Ингредиент', present(i), 'получен')
            print('Нажмите 0 для сохранения игры')
            if input() == '0':
                player.save()

    player.lv += 1
    player.maxhp += 5
    player.damage += 5
    player.mana = min(player.mana + 1 + player.lv // 20, player.maxmana)
    player.maxmana += 1
    player.mana = min(player.maxmana, player.mana + 3)
    player.hp = min(player.maxhp, player.hp + 15)
    player.shield_time -= 2
    player.return_time -= 2
    player.weakness = 0
    print('\n \n \n \n \n \n')
    print()
    return player
'''

def savedata(data):
    GlobalData = open("DATA.json", 'w')
    jsonable = dict()
    for key in data.keys():
        arr = []
        for elem in data[key]:
            self = elem[1]
            arr.append([elem[0], self.hp, self.mana, self.maxmana, self.maxhp, self.damage, *self.potion, *self.ingredients, self.stunned, self.shield, self.shield_time, self.damage_return, self.return_time, self.weakness, self.rage, self.rage_time, self.lv])
        jsonable[key] = arr
    print(jsonable)
    GlobalData.write(json.dumps(jsonable))
    GlobalData.close()


GlobalData = open('DATA.json', 'r')
pre = json.loads(GlobalData.read())
data = dict()
waiting = dict()
for key in pre.keys():
    arr = []
    waiting[key] = -1
    for elem in pre[key]:
        self = hero()
        self.hp, self.mana, self.maxmana, self.maxhp, self.damage, self.potion[0], self.potion[1], self.potion[2], self.potion[3], self.potion[4], self.ingredients[0], self.ingredients[1], self.ingredients[2], self.ingredients[3], self.ingredients[4], self.stunned, self.shield, self.shield_time, self.damage_return, self.return_time, self.weakness, self.rage, self.rage_time, self.lv = elem[1:]
        arr.append([elem[0], self])
    data[int(key)] = arr
GlobalData.close()
print(data)
playinggames = dict()
enemies = dict()
skeleton = mob(340, 10)
skeleton.drop = [0, 0.2, 0.6, 0.2, 0]
zombie = mob(750, 5)
zombie.drop = [0.1, 0.1, 0.1, 0.1, 0.1]
crazy = mob(900, 5, 1)
crazy.drop = [0.3, 0, 0.3, 0.3, 0.5]
wizard = mob(1000, 30, False, 0.2)
wizard.drop = [0.03, 0.3, 0.3, 0.03, 0.2]
pro_wizard = mob(2000, 30)
pro_wizard.damage_return = 0.15
pro_wizard.no_magic = True
pro_wizard.drop = [1, 1, 1, 1, 1]
ghost = mob(900, 20)
ghost.weakness = 0.18
ghost.drop = [0.25, 0.25, 0.25, 0.25, 0.25]
electro_wizard = mob(700, 10)
electro_wizard.stun_chance = 0.7
electro_wizard.drop = [0.1, 0.5, 0, 0.2, 0.2]
wizard2 = mob(1500, 30, False, 0.25)
wizard2.drop = [0.03, 0.3, 0.3, 0.03, 0.03]
pro_wizard2 = mob(4000, 40)
pro_wizard2.damage_return = 0.2
pro_wizard2.no_magic = True
pro_wizard2.drop = [1, 1, 1, 1, 1]
ghost2 = mob(1200, 20)
ghost2.weakness = 0.3
ghost2.drop = [0.25, 0.25, 0.25, 0.25, 0.25]
electro_wizard2 = mob(900, 10)
electro_wizard2.stun_chance = 0.75
electro_wizard2.drop = [0.1, 0.5, 0, 0.2, 0.2]
wizard3 = mob(2000, 30, False, 0.3)
wizard3.drop = [0.03, 0.3, 0.3, 0.03, 0.03]
ghost3 = mob(1500, 30)
ghost3.weakness = 0.45
ghost3.drop = [0.25, 0.25, 0.25, 0.25, 0.25]
Boss = mob(3000, 40)
Boss.weakness = 0.02
Boss.stun_chance = 0.1
Boss.damage_return = 0.03
Boss.drop = [1, 1, 1, 1, 1]
Boss2 = mob(5000, 60)
Boss2.weakness = 0.04
Boss2.stun_chance = 0.15
Boss2.damage_return = 0.06
Boss2.drop = [1, 1, 1, 1, 1]
Boss3 = mob(8000, 90)
Boss3.weakness = 0.06
Boss3.stun_chance = 0.2
Boss3.damage_return = 0.1
Boss3.drop = [1, 1, 1, 1, 1]
Boss4 = mob(20000, 120)
Boss4.no_magic = True
Boss4.drop = [1, 1, 1, 1, 1]

TOKEN = '6075009729:AAELCItgPMQ5FfNkHbTnxx7ETxBkwcWaSPI'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.json['text'])
    if message.from_user.id not in data.keys():
        keyboard = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text="Погнали!", callback_data="newgame")
        keyboard.row(button)
        bot.send_message(message.from_user.id, "Привет! Я вижу ты новый пользователь. Я зарегистрировал тебя в базе. Приятной игры! Прочти правила /help. Для взаимодействия используй кнопки. Напиши /mm для мгновенного перехода в главное меню (если ты в игре прогресс сбросится!)", reply_markup=keyboard)
        data[message.from_user.id] = [['Пусто', hero()], ['Пусто', hero()], ['Пусто', hero()]]
        savedata(data)
    elif message.json['text'][0] == '!' and waiting[message.from_user.id] != -1 and message.json['text'] != '!':
        keyboard = telebot.types.InlineKeyboardMarkup()
        data[message.from_user.id][waiting[message.from_user.id]] = [message.json['text'][1:], hero()]
        waiting[message.from_user.id] = -1
        savedata(data)
        button4 = telebot.types.InlineKeyboardButton(text="Главное меню", callback_data="mainmenu")
        keyboard.row(button4)
        bot.send_message(message.from_user.id, "Готово!", reply_markup=keyboard)
    elif message.json['text'] == '/mm':
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text="Перейти", callback_data="mainmenu")
        keyboard.row(button1)
        bot.send_message(message.from_user.id, "Перейти в главное меню", reply_markup=keyboard)
    elif message.json['text'] == '/help':
        bot.send_message(message.from_user.id, "Привет!\nЭто справочное сообщение, в нем рассказывается о главных моментах игры\nДля начала новых игр или загрузки старых используй \"mm\". Когда выводится здоровье, черные кружки показывают утерянное здоровье, красное - то здоровье, которое ТОЧНО будет потеряно, зеленое - то, которое ТОЧНО останется, желтое - которое возможно будт утеряно (если повезет, могут быть потеряны лишь часть кружочков). Возможна погрешность +- 1 кружочек.\nПри переименовывании не забудье указать восклицательный знак перед словом.\nПожалуйста, не нажмайте кнопки под предыдущими сообщениями бота. Это, скорее всего, не нарушит работу бота, но может привести к сбоям и некорректной работе. Если вы думаете, что сломали бота - загрузите сохранение из главного меню. Особенно опасно нажимать много раз на кнопку варки зелий. Единственное - можно нажимать кнопку из прошлых сообщений если вы хотите изменить действие (нет маны на нужное заклинание и вы хотите сварить зелье в таком случае).\nСохранения работают раз в несколько уровней - будьте внмательны.\nВраг не бьет в ответ, если убит в этот ход.\n/mm - в главное меню.\nВолшебный щит не меняет отображение - пусть низкий урон будет для вас сюрпризом =) (если вы конечно не прочитали справку)")
    else:
        bot.send_message(message.from_user.id, "Бот почти не реагирует на текст. Справка - /help.")

@bot.callback_query_handler(func=lambda call: call.data == "newgame")
def callback_function1(callback_obj):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][0][0], callback_data="newgame1")
    button2 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][1][0], callback_data="newgame2")
    button3 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][2][0], callback_data="newgame3")
    keyboard.row(button1, button2, button3)
    button4 = telebot.types.InlineKeyboardButton(text="Главное меню", callback_data="mainmenu")
    keyboard.row(button4)
    bot.send_message(callback_obj.from_user.id, "Выберите ячейку сохранения для перезаписи. Затем напишите в чат любое сообщение с префиксом ! для того чтобы дать сохранению название", reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data == "newgame1")
def callback_function2(callback_obj):
    waiting[callback_obj.from_user.id] = 0
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data == "newgame2")
def callback_function3(callback_obj):
    waiting[callback_obj.from_user.id] = 1
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data == "newgame3")
def callback_function4(callback_obj):
    waiting[callback_obj.from_user.id] = 2
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data == "mainmenu")
def callback_function5(callback_obj):
    keyboard = telebot.types.InlineKeyboardMarkup()
    savedata(data)
    button1 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][0][0], callback_data="startrun0")
    keyboard.row(button1)
    button2 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][1][0], callback_data="startrun1")
    keyboard.row(button2)
    button3 = telebot.types.InlineKeyboardButton(text=data[callback_obj.from_user.id][2][0], callback_data="startrun2")
    keyboard.row(button3)
    button4 = telebot.types.InlineKeyboardButton(text="Новая игра", callback_data="newgame")
    keyboard.row(button4)
    bot.send_message(callback_obj.from_user.id, "Выберите игру, которую хотите продолжить (Если у игры имя пусто, то рекомендуется пересоздать эту игру с более понятным именем)", reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "startrun")
def callback_function6(callback_obj):
    print(callback_obj.data[-1])
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='Продолжить игру', callback_data="playslot" + callback_obj.data[-1])
    keyboard.row(button1)
    bot.send_message(callback_obj.from_user.id, "Погнали! Ты играешь в сохранение с названием | " + str(data[callback_obj.from_user.id][int(callback_obj.data[-1])][0]), reply_markup=keyboard)
    playinggames[callback_obj.from_user.id] = hero(data[callback_obj.from_user.id][int(callback_obj.data[-1])][1])
    player = data[callback_obj.from_user.id][int(callback_obj.data[-1])][1]
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "playslot")
def callback_function7(callback_obj):
    player = playinggames[callback_obj.from_user.id]
    id = callback_obj.from_user.id
    if player.lv in [5, 12, 24]:
        bot.send_message(id, 'Стадия пройдена. Враги стали сложнее! Игра сохранена.')
        data[id][int(callback_obj.data[-1])][1] = hero(player)
    if player.lv in [33, 40, 50, 60]:
        bot.send_message(id, 'Следующий противник - босс! Игра сохранена.')
        data[id][int(callback_obj.data[-1])][1] = hero(player)
    if player.lv - 1 in [33, 40, 50, 60]:
        bot.send_message(id, 'Босс пройден! Игра сохранена.')
        data[id][int(callback_obj.data[-1])][1] = hero(player)
    bot.send_message(id, 'Уровень ' + str(player.lv))
    level = generate(player.lv)
    if level[0]:
        if level[1] < 6:
            player.potion[level[1] - 1] += 1
            translator = dict()
            translator[1] = 'здоровья'
            translator[2] = 'здоровья (бол.)'
            translator[3] = 'маны'
            translator[4] = 'маны (бол.)'
            translator[5] = 'ярости'
            bot.send_message(id, 'Вы спустились ниже, и нашли зелье ' + translator[level[1]])
        elif level[1] == 6:
            player.damage += 15
            bot.send_message(id, 'Вы выпили зелье силы, и получили +15 к урону!')
        else:
            player.damage += 10
            player.maxhp += 10
            bot.send_message(id, 'Вы выпили зелье могущества и получили +10 к максимальному здоровью и урону')
        keyboard = telebot.types.InlineKeyboardMarkup()
        player.lv += 1
        button1 = telebot.types.InlineKeyboardButton(text='Следующий уровень', callback_data="playslot" + str(callback_obj.data[-1]))
        playinggames[callback_obj.from_user.id] = player
        keyboard.row(button1)
        bot.send_message(callback_obj.from_user.id, "Ты нашел зелье. Тебе повезло, что не попался враг. Спускайся ниже!", reply_markup=keyboard)
    else:
        enemy = level[1]
        bot.send_message(id, 'ВРАГ!!')
        enemies[id] = enemy
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='Начать битву', callback_data="battle" + callback_obj.data[-1])
        playinggames[callback_obj.from_user.id] = player
        keyboard.row(button1)
        bot.send_message(id, 'Досье: Имя - ' + level[2], reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "battle")
def callback_function7(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    if random.randint(1, 10000) > enemy.stun_chance * 10000 or enemy.stun > 0:
        bot.send_message(id, 'Вы бьете врага. Визулизация его здоровья после вышего удара:')
        bot.send_message(id, visualize(enemy.maxhp, enemy.hp, player.damage * max(0.1, 1 - player.weakness) * (1 + player.rage) * 0.9, player.damage * max(0.1, 1 - player.weakness) * (1 + player.rage) * 1.1))
        player.attack(enemy)
        bot.send_message(id, 'Ваше здоровье после удара врага')
        bot.send_message(id, visualize(player.maxhp, player.hp, enemy.damage * 0.9, enemy.damage * 1.1))
        bot.send_message(id, 'Вы можете использовать зелье, заклинание, и сварить зелье.')
        one = False
        if player.ingredients[0] > 0 and player.ingredients[2] > 0:
            one = True
        if player.ingredients[1] > 0 and player.ingredients[3] > 0:
            one = True
        if player.ingredients[3] > 1 and player.ingredients[4] > 1:
            one = True
        if one:
            button1 = telebot.types.InlineKeyboardButton(text='Сварить зелье', callback_data="potion" + callback_obj.data[-1])
            keyboard.row(button1)
        if player.mana > 9 and not enemy.no_magic:
            button2 = telebot.types.InlineKeyboardButton(text='Использовать заклинание', callback_data="magic" + callback_obj.data[-1])
            keyboard.row(button2)
        if sum(player.potion) > 0:
            button3 = telebot.types.InlineKeyboardButton(text='Выпить зелье', callback_data="drink" + callback_obj.data[-1])
            keyboard.row(button3)
        button4 = telebot.types.InlineKeyboardButton(text='Ничего не делать', callback_data="check" + callback_obj.data[-1])
        keyboard.row(button4)
        bot.send_message(id, 'Выберите действие', reply_markup=keyboard)
        playinggames[id] = player
        enemies[id] = enemy
    else:
        callback_function14(callback_obj)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "magic")
def callback_function8(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    if player.mana > 9:
        button1 = telebot.types.InlineKeyboardButton(text='Молния', callback_data="zap" + callback_obj.data[-1])
        keyboard.row(button1)
        button2 = telebot.types.InlineKeyboardButton(text='Лечение', callback_data="heal" + callback_obj.data[-1])
        keyboard.row(button2)
    if player.mana > 14:
        button3 = telebot.types.InlineKeyboardButton(text='Оглушение', callback_data="stun" + callback_obj.data[-1])
        keyboard.row(button3)
        if enemy.hp < 300:
            button4 = telebot.types.InlineKeyboardButton(text='Поглотить врага', callback_data="destroy" + callback_obj.data[-1])
            keyboard.row(button4)
    if player.mana > 19:
        button5 = telebot.types.InlineKeyboardButton(text='Волшебный щит', callback_data="shield" + callback_obj.data[-1])
        keyboard.row(button5)
    bot.send_message(id, "Выберите заклинание из перечисленных", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "zap")
def callback_function9(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    button5 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)
    player.mana -= 10
    damag = 500 * random.randint(80, 120) / 100
    enemy.hp -= damag
    player.hp -= damag * enemy.damage_return
    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Визуализация здоровья врага после удара молнии (Урон нанесен):')
    bot.send_message(id, visualize(enemy.maxhp, enemy.hp), reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "heal")
def callback_function10(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    button5 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)
    player.mana -= 10
    player.hp = player.maxhp
    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Отлично, вы полностью здоровы!', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "stun")
def callback_function11(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    button5 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    player.mana -= 15
    enemy.stun = 6

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Враг оглушен на 6 ходов', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "destroy")
def callback_function12(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    button5 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    enemy.hp = -1000
    player.mana -= 15
    player.hp = max(self.maxhp, self.hp + 30)
    player.damage += 5
    player.rage_time += 3
    player.rage = 0.5

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Враг поглощен. Вы стали сильнее.', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "shield")
def callback_function13(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()
    button5 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    player.mana -= 20
    player.shield = 0.9
    player.damage_return = 0.3
    player.shield_time = 8
    player.return_time = 8

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Щит активирован.', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "drink")
def callback_function14(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    if player.potion[0] > 0:
        button1 = telebot.types.InlineKeyboardButton(text='Малое зелье здоровья', callback_data="smallheal" + callback_obj.data[-1])
        keyboard.row(button1)
    if player.potion[1] > 0:
        button2 = telebot.types.InlineKeyboardButton(text='Большое зелье здоровья', callback_data="bigheal" + callback_obj.data[-1])
        keyboard.row(button2)
    if player.potion[2] > 0:
        button3 = telebot.types.InlineKeyboardButton(text='Малое зелье маны', callback_data="smallmana" + callback_obj.data[-1])
        keyboard.row(button3)
    if player.potion[3] > 0:
        button4 = telebot.types.InlineKeyboardButton(text='Большое зелье маны', callback_data="bigmana" + callback_obj.data[-1])
        keyboard.row(button4)
    if player.potion[4] > 0:
        button5 = telebot.types.InlineKeyboardButton(text='Зелье ярости', callback_data="rage" + callback_obj.data[-1])
        keyboard.row(button5)

    bot.send_message(id, "Выберите зелье из перечисленных", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "smallheal")
def callback_function15(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[0] -= 1
    player.hp = min(player.hp + 50, player.maxhp)
    button5 = telebot.types.InlineKeyboardButton(text='Вернемся к битве тратить только что полученное здоровье', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    bot.send_message(id, "Вы пьете зелье здоровья, и вам становится очень хорошо...", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "bigheal")
def callback_function16(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[1] -= 1
    player.hp = min(player.hp + 150, player.maxhp)
    button5 = telebot.types.InlineKeyboardButton(text='Вернемся к битве тратить только что полученное здоровье', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    bot.send_message(id, "Вы пьете зелье здоровья, и вам становится очень хорошо...", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "smallmana")
def callback_function17(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[2] -= 1
    player.mana = min(player.hp + 10, player.maxmana)
    button5 = telebot.types.InlineKeyboardButton(text='Вернемся к битве - колдовать!', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    bot.send_message(id, "Вы пьете зелье маны, и чувствуете прилив маны.", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "bigmana")
def callback_function18(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[3] -= 1
    player.mana = min(player.mana + 30, player.maxmana)
    button5 = telebot.types.InlineKeyboardButton(text='Вернемся к битве - колдовать!', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    bot.send_message(id, "Вы пьете зелье маны, и чувствуете сильный прилив маны.", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "rage")
def callback_function19(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.rage = 0.5
    player.rage_time += 12
    player.potion[4] -= 1
    button5 = telebot.types.InlineKeyboardButton(text='АРГХ!', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button5)

    bot.send_message(id, "Вы пьете зелье ярости, и готовы раскрошить на атомы любого", reply_markup=keyboard)
    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "check")
def callback_function14(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    if enemy.hp < 0:
        player.lv += 1
        player.maxhp += 5
        player.damage += 5
        player.mana = min(player.mana + 1 + player.lv // 20, player.maxmana)
        player.maxmana += 1
        player.mana = min(player.maxmana, player.mana + 3)
        player.hp = min(player.maxhp, player.hp + 15)
        player.shield_time -= 2
        player.return_time -= 2
        player.weakness = 0
        for i in range(5):
            if enemy.drop[i] * 10000 > random.randint(0, 10000):
                player.ingredients[i] += 1
                bot.send_message(id, 'Ингредиент ' + present(i) + ' получен')
        button5 = telebot.types.InlineKeyboardButton(text='Следующий уровень', callback_data="playslot" + callback_obj.data[-1])
        keyboard.row(button5)
        bot.send_message(id, 'Враг повержен! Характеристики увеличены. Здоровье - ' + str(player.maxhp) + ', урон - ' + str(player.damage) + ', макс. мана - ' + str(player.maxmana), reply_markup=keyboard)
    else:
        if enemy.stun < 1:
            enemy.attack(player)
        if player.hp < 0:
            button5 = telebot.types.InlineKeyboardButton(text='Пойду загружу сейв из главного меню', callback_data="mainmenu")
            keyboard.row(button5)
            bot.send_message(id, 'Вы сами не знаете, как умерли.', reply_markup=keyboard)
            playinggames[id] = player
            enemies[id] = enemy
        else:
            player.rage_time = max(0, player.rage_time - 1)
            if player.rage_time == 0:
                player.rage = 0
            enemy.damage += enemy.damage * enemy.damage_multiply if enemy.stun < 1 else 0
            enemy.stun -= 1
            player.shield_time -= 1
            player.weakness += enemy.weakness if enemy.stun < 1 else 0
            player.return_time -= 1
            player.hp = round(player.hp, 5)
            enemy.hp = round(enemy.hp, 5)
            callback_function7(callback_obj)

    playinggames[id] = player
    enemies[id] = enemy
    bot.answer_callback_query(callback_query_id=callback_obj.id)


@bot.callback_query_handler(func=lambda call: call.data[:-1] == "potion")
def callback_function100(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    if player.ingredients[0] > 0 and player.ingredients[2] > 0:
        button1 = telebot.types.InlineKeyboardButton(text='Малое зелье здоровья', callback_data="craftsmallheal" + callback_obj.data[-1])
        keyboard.row(button1)
    if player.ingredients[0] > 3 and player.ingredients[2] > 3:
        button2 = telebot.types.InlineKeyboardButton(text='Большое зелье здоровья',
                                                     callback_data="craftbigheal" + callback_obj.data[-1])
        keyboard.row(button2)
    if player.ingredients[1] > 0 and player.ingredients[3] > 0:
        button3 = telebot.types.InlineKeyboardButton(text='Малое зелье маны',
                                                     callback_data="craftsmallmana" + callback_obj.data[-1])
        keyboard.row(button3)
    if player.ingredients[1] > 2 and player.ingredients[3] > 2:
        button4 = telebot.types.InlineKeyboardButton(text='Большое зелье маны', callback_data="craftbigmana" + callback_obj.data[-1])
        keyboard.row(button4)
    if player.ingredients[3] > 1 and player.ingredients[4] > 1:
        button5 = telebot.types.InlineKeyboardButton(text='Зелье ярости',
                                                     callback_data="craftrage" + callback_obj.data[-1])
        keyboard.row(button5)


    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Выберите зелье для варки', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "craftsmallheal")
def callback_function101(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[0] += 1
    player.ingredients[0] -= 1
    player.ingredients[2] -= 1
    button1 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button1)

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Зелье сварено', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "craftbigheal")
def callback_function102(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[1] += 1
    player.ingredients[0] -= 3
    player.ingredients[2] -= 3
    button1 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button1)

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Зелье сварено', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "craftsmallmana")
def callback_function103(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[2] += 1
    player.ingredients[1] -= 1
    player.ingredients[3] -= 1
    button1 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button1)

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Зелье сварено', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "craftbigmana")
def callback_function104(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[3] += 1
    player.ingredients[1] -= 3
    player.ingredients[3] -= 3
    button1 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button1)

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Зелье сварено', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)

@bot.callback_query_handler(func=lambda call: call.data[:-1] == "craftrage")
def callback_function105(callback_obj):
    id = callback_obj.from_user.id
    player = playinggames[id]
    enemy = enemies[id]
    keyboard = telebot.types.InlineKeyboardMarkup()

    player.potion[4] += 1
    player.ingredients[3] -= 2
    player.ingredients[4] -= 2
    button1 = telebot.types.InlineKeyboardButton(text='Продолжим', callback_data="check" + callback_obj.data[-1])
    keyboard.row(button1)

    playinggames[id] = player
    enemies[id] = enemy
    bot.send_message(id, 'Зелье сварено', reply_markup=keyboard)
    bot.answer_callback_query(callback_query_id=callback_obj.id)





bot.infinity_polling()
