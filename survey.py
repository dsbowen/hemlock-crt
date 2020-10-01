"""Cognitive reflection test for hemlock"""

from hemlock_crt import crt

from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
    from hemlock_crt import crt_items
    return Branch(
        *crt(*list(crt_items.keys()), require=True, page=True),
        Page(
            Label('<p>The End!</p>'),
            terminal=True
        )
    )