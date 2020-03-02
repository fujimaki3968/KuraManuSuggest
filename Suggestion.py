import csv
import random
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))

with open('kura_menu.csv') as fp:
    item_list = list(csv.reader(fp))

print(len(item_list))


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

# html = generate_html(item_list, money)
#
# with open('jinja2_test.html',mode='w') as f:
#     f.write(str(html))
