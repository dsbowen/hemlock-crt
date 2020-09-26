"""Cognitive reflection test for hemlock"""

from hemlock_crt import crt

from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
    return Branch(
        *crt(page=True),
        Page(
            Label('<p>The End!</p>'),
            terminal=True
        )
    )