import csv
from random import randint as R
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

with open('kura_menu.csv') as fp:
    item_list = list(csv.reader(fp))

item_list = sorted(item_list, key=lambda x: int(x[1]))

def binary_search(items, num):
    length = len(items)
    mid = int(length / 2)
    right = length - 1
    left = 0

    while(right - left > 1):
        tmp = int(items[mid][1])
        if tmp <= num:
            left = mid
            mid = left + int((right - left)/2)
        elif tmp > num:
            right = mid
            mid = left + int((right - left)/2)
    return left


def main_function(event, context):
    if event['money'] != "":
        money = int(event['money'])
        locate = int(event['locate'])
    else:
        money = 1000
        locate = 1
    html = generate_html(item_list, money, locate)
    return html


def generate_html(item_list, money, locate):
    all_money = money
    sum_cal = 0
    suggest_list = []
    tweet_text = ""
    over = False
    while(all_money >= 110):
        list_range = binary_search(item_list, all_money)
        tmp = item_list[R(0, list_range)]
        if int(tmp[4]) != 0:
            if str(locate) not in tmp[4]:
                continue
        if all_money < int(tmp[1])*1.1:
            continue
        if len(tweet_text) + len(tmp[0]) < 100:
            tweet_text += tmp[0] + " "
        else:
            over=True
        suggest_list.append(tmp)
        sum_cal += int(tmp[3])
        all_money -= int(tmp[1]) * 1.1
    if over:
        tweet_text += "…"
    tmpl = env.get_template('output.tmpl')
    html = tmpl.render(items=suggest_list, money=money, sum=money-int(all_money), cal=sum_cal, locate=locate, tweet_text=tweet_text,)
    return html

html = generate_html(item_list, 1000, 1)

for _ in range(1000):
    html = generate_html(item_list, 1000, 1)

with open('jinja2_test.html',mode='w') as f:
    f.write(str(html))