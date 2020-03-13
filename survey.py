"""Hemlock-CRT demonstration"""

from hemlock_crt import CRT
from hemlock_crt.items import ball_bat, machines, lily_pads

from hemlock import *

@route('/survey')
def Start(origin=None):
    b = Branch()
    CRT(b, ball_bat, machines, lily_pads)
    p = Page(b, terminal=True)
    Label(p, label='<p>End.</p>')
    return b