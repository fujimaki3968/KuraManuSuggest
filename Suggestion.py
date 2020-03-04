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
    while(all_money >= 100):
        list_range = binary_search(item_list, all_money)
        tmp = item_list[R(0, list_range)]
        if int(tmp[4]) != 0:
            if str(locate) not in tmp[4]:
                continue
        suggest_list.append(tmp)
        sum_cal += int(tmp[3])
        all_money -= int(tmp[1])

    tmpl = env.get_template('output.tmpl')
    html = tmpl.render(items=suggest_list, money=money, sum=money-all_money, cal=sum_cal, locate=locate,)
    return html

html = generate_html(item_list, 5000, 1)

with open('jinja2_test.html',mode='w') as f:
    f.write(str(html))