import csv
from random import randint as R
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

with open('kura_menu.csv') as fp:
    item_list = list(csv.reader(fp))

item_list = sorted(item_list, key=lambda x: x[1])



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
    else:
        money = 1000
    html = generate_html(item_list, money)
    return html


def generate_html(item_list, money):
    all_money = money
    suggest_list = []
    while(all_money>=100):
        list_range = binary_search(item_list, money)
        tmp = item_list[R(0, list_range)]
        suggest_list.append(tmp)
        all_money -= int(tmp[1])
    tmpl = env.get_template('output.tmpl')
    html = tmpl.render(items=suggest_list, money=money, )
    return html
#
# money = 1000
#
# html = generate_html(item_list, money)
#
# with open('jinja2_test.html',mode='w') as f:
#     f.write(str(html))



