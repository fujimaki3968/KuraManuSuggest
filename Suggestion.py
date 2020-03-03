import csv
import random
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
        print(right, left, mid, tmp)
    print(right)
    return right


ans = binary_search(item_list, 300)


def main_function(event, context):
    try:
        cost = event["money"]
    except:
        cost = 1000
    html = generate_html(item_list, cost)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html;charset=UTF-8"},
        "body": html
    }


def generate_html(item_list, money):
    tmpl = env.get_template('output.tmpl')
    html = tmpl.render(items=item_list, money=money, )
    return html

money = 1000

html = generate_html(item_list, money)

with open('jinja2_test.html',mode='w') as f:
    f.write(str(html))
