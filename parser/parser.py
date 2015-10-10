# coding: utf-8
from lxml import html
from regulars import regulars

HTML = '''
<html>
<body>
<div title="buyer-name">Carson Busses</div>
<span class="item-price">$29.95</span>
<span class="item-price">$14.95</span>
<span id="item-price">
    <span class="item-company">ООО Рога и копыта</span>
</span>
</body>
</html>
'''

page1 = HTML


def get_html_elements(page, regulars):
    tree = html.fromstring(str(page))
    elements = {}
    for param in regulars.keys():
        elements[param] = tree.xpath(regulars[param])
    return elements

p = get_html_elements(page1, regulars)

print p