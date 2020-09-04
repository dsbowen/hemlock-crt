"""Cognitive Reflection Test (CRT)

Frederick, Shane (2005). "Cognitive Reflection and Decision Making". Journal of Economic Perspectives. 19 (4): 25–42. https://www.aeaweb.org/articles?id=10.1257/089533005775196732.

Examples
--------

```python
from hemlock_crt import crt

from hemlock import Page, push_app_context

app = push_app_context()

Page(*crt('batball', 'lilypads', 'widgets')).preview()
```
"""

from hemlock import Embedded, Input, Submit as S

def crt(*items):
    """
    Parameters
    ----------
    \*items : str
        The names of CRT items.

    Returns
    -------
    CRT questions : list of `hemlock.Question`
    """
    return [crt_items[item]() for item in items]

crt_items = {}

def register_crt_item(key, correct, intuitive):
    """
    Register a new CRT item.

    Parameters
    ----------
    key : str
        Name of the CRT item.

    correct : 
        The correct answer.

    intuitive :
        The intuitive answer.
    """
    def inner(func):
        def gen_question():
            question = func()
            question.data_rows = -1
            question.submit.append(S(_assess_response, correct, intuitive))
            return question
        crt_items[key] = gen_question
        return gen_question
    
    return inner

def _assess_response(question, correct, intuitive):
    """
    Add embedded data to the CRT question's page indicating if the answer was 
    1) correct, 2) intuitive.
    """
    page = question.page
    prev_assessment = [
        e for e in page.embedded 
        if e.var in [question.var+'Correct', question.var+'Intuitive']
    ]
    [page.embedded.remove(e) for e in prev_assessment]
    page.embedded += [
        Embedded(
            question.var+'Correct', 
            int(correct==type(correct)(question.data)),
            data_rows=-1
        ),
        Embedded(
            question.var+'Intuitive',
            int(intuitive==type(intuitive)(question.data)),
            data_rows=-1
        )
    ]

@register_crt_item('batball', correct=.05, intuitive=.10)
def bat_ball():
    return Input(
        '''
        <p>A bat and a ball cost $1.10 in total. The bat costs $1 more than 
        the ball.</p>
        <p>How much does the ball cost?</p>
        ''',
        var='CRT.Batball',
        append='cents',
        input_type='number'
    )