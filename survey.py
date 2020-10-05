"""Cognitive reflection test for hemlock"""

from flask_login import current_user
from hemlock import Branch, Page, Label, route
from hemlock_crt import crt

@route('/survey')
def start():
    return Branch(
        *crt('bat_ball', 'lily_pads', 'widgets', 'students', page=True),
        Page(
            Label(compile=display_score),
            terminal=True
        )
    )

def display_score(label):
    label.label = '''
    <p>You gave {} correct and {} intuitive answers out of {} CRT questions.
    </p>
    '''.format(
        current_user.g['CRT_Correct'], 
        current_user.g['CRT_Intuitive'], 
        current_user.g['CRT_Total']
    )