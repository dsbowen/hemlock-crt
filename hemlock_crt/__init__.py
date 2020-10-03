"""Cognitive Reflection Test (CRT)

Frederick, Shane (2005). "Cognitive Reflection and Decision Making". Journal of Economic Perspectives. 19 (4): 25–42. https://www.aeaweb.org/articles?id=10.1257/089533005775196732.

Examples
--------

```python
from hemlock import Page, push_app_context
from hemlock_crt import crt

app = push_app_context()

Page(*crt()).preview()
```
"""

from hemlock import Binary, Check, Choice, Debug as D, Embedded, Input, Page, Validate as V, Submit as S

import random

def crt(*items, page=False, require=False, shuffle=False):
    """
    Parameters
    ----------
    \*items : str
        The names of CRT items.

    page : bool, default=False
        Indicates that items should be in separate pages.

    require : bool, default=False
        Indicates that responses are required.

    shuffle : bool, default=False
        Indicates that items should be shuffled.

    Returns
    -------
    CRT items : list
        List of `hemlock.Question` if not `page`, otherwise list of 
        `hemlock.Page`.
    """
    items = items if items else ['bat_ball', 'widgets', 'lily_pads']
    items = [crt_items[item]() for item in items]
    if require:
        for item in items:
            item.validate.append(V.require())
    if page:
        items = [
            Page(
                item, 
                name=item.var, 
                timer=(item.var+'Time', -1), 
                debug=[D.debug_questions(), D.forward()]
            )
            for item in items
        ]
    if shuffle:
        random.shuffle(items)
    return items

crt_items = {}

def register(correct, intuitive, key=None):
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
        crt_items[key or func.__name__] = gen_question
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
    data = question.data
    data_null = data in (None, '')
    page.embedded += [
        Embedded(
            question.var+'Correct', 
            None if data_null else int(correct==type(correct)(data)),
            data_rows=-1
        ),
        Embedded(
            question.var+'Intuitive',
            None if data_null else int(intuitive==type(intuitive)(data)),
            data_rows=-1
        )
    ]

def _debug_functions(correct, intuitive):
    return [
        D.send_keys(),
        D.send_keys(str(intuitive), p_exec=.7),
        D.send_keys(str(correct), p_exec=.3)
    ]

# https://www.aeaweb.org/articles?id=10.1257/089533005775196732
@register(correct=5., intuitive=10.)
def bat_ball():
    return Input(
        '''
        <p>A bat and a ball cost $1.10 in total. The bat costs $1 more than 
        the ball.</p>
        <p>How many cents does the ball cost?</p>
        ''',
        var='CRT_BatBall', append='cents', 
        extra_attrs=dict(type='number', min=0, max=110, step='any'),
        debug=_debug_functions(5, 10)
    )

@register(correct=5., intuitive=100.)
def widgets():
    return Input(
        '''
        <p>If it takes 5 machines 5 minutes to make 5 widgets, how many 
        minutes would it take 100 machines to make 100 widgets?</p>
        ''',
        var='CRT_Widgets', append='minutes',
        extra_attrs=dict(type='number', min=0, step='any'),
        debug=_debug_functions(5, 100)
    )

@register(correct=47., intuitive=24.)
def lily_pads():
    return Input(
        '''
        <p>In a lake, there is a patch of lily pads. Every day, the patch 
        doubles in size. If it takes 48 days for the patch to cover the 
        entire lake, how many days would it take for the patch to cover half 
        of the lake?</p>
        ''',
        var='CRT_LilyPads', append='days', 
        extra_attrs=dict(type='number', min=0, max=48, step='any'),
        debug=_debug_functions(47, 24)
    )

# https://dataverse.harvard.edu/file.xhtml?persistentId=doi:10.7910/DVN/BPCDH5/X7UQGX
@register(correct=0, intuitive=1)
def flowers():
    return Binary(
        '''
        <p>All flowers have petals. Roses have petals. If these two statements are true can we conclude that roses are flowers?</p>
        ''',
        var='CRT_Flowers'
    )

@register(correct=5., intuitive=3.)
def sun_tea():
    return Input(
        '''
        <p>Sally is making sun tea. Every hour, the concentration of the tea 
        doubles. If it takes 6 hours for the tea to be ready, how many hours 
        would it take for the tea to reach half of the final 
        concentration?</p>
        ''',
        var='CRT_SunTea', append='hours', 
        extra_attrs=dict(type='number', min=0, max=6, step='any'),
        debug=_debug_functions(5, 3)
    )

@register(correct=-1, intuitive=1)
def green_round():
    return Check(
        '''
        <p>In a box, no green things are round, and all round things are large. What can we conclude?</p>
        ''',
        [
            ('No green things are large', 1),
            ('Some green things are not large', 0),
            ('Neither of the above', -1)
        ],
        var='CRT_GreenRound'
    )

@register(correct=0, intuitive=1)
def auto():
    return Binary(
        '''
        <p>All things that have a motor need oil. Automobiles need oil. If 
        these two statements are true, can we conclude from them that 
        automobiles have a motor?</p>
        ''',
        var='CRT_Auto'
    )

@register(correct=0, intuitive=1)
def rabbits():
    return Binary(
        '''
        <p>All cats are furry. Rabbits are furry. If these two statements are 
        true, can we conclude from them that rabbits are cats?</p>
        ''',
        var='CRT_Rabbits'
    )

@register(correct=1, intuitive=0)
def whales():
    return Binary(
        '''
        <p>All mammals walk. Whales are mammals. If these two statements are 
        true, can we conclude from them that whales walk?</p>
        ''',
        var='CRT_Whales'
    )

@register(correct=0, intuitive=1)
def athletes():
    return Binary(
        '''
        <p>All fish are swimmers. Some Olympic athletes are swimmers. If 
        these two statements are true, can we conclude from them that some 
        Olympic athletes are fish?</p>
        ''',
        var='CRT_Athletes'
    )

@register(correct=0, intuitive=1)
def roses():
    return Binary(
        '''
        <p>All living things need water. Roses need water. If these two 
        statements are true, can we conclude from them that roses are living 
        things?</p>
        ''',
        var='CRT_Roses'
    )

@register(correct=1, intuitive=0)
def boats():
    return Binary(
        '''
        <p>All vehicles have wheels. Boats are vehicles. If these two 
        statements are true, can we conclude from them that boats have 
        wheels?</p>
        ''',
        var='CRT_Boats'
    )

@register(correct=1, intuitive=0)
def cigarettes():
    return Binary(
        '''
        <p>All things that are smoked are good for the health. Cigarettes are 
        smoked. If these two statements are true, can we conclude from them 
        that cigarettes are good for the health?</p>
        ''',
        var='CRT_Cigarettes'
    )

@register(correct=1, intuitive=0)
def bears():
    return Binary(
        '''
        <p>All bears are ferocious. Some stuffed animals are bears. If these 
        two statements are true, can we conclude from them that some stuffed 
        animals are ferocious?</p>
        ''',
        var='CRT_Bears'
    )

@register(correct=0, intuitive=1)
def wives():
    return Binary(
        '''
        <p>All wives are married. Some women are married. If these two 
        statements are true, can we conclude from them that some women are 
        wives?</p>
        ''',
        var='CRT_Wives'
    )

@register(correct=1, intuitive=0)
def oysters():
    return Binary(
        '''
        <p>If animals need vitamin Q, can we conclude that oysters need 
        vitamin Q?</p>
        ''',
        var='CRT_Oysters'
    )

@register(correct=1, intuitive=0)
def dogs():
    return Binary(
        '''
        <p>If oxygen in the air is poisonous to animals, can we conclude that 
        oxygen in the air is poisonous to dogs?</p>
        ''',
        var='CRT_Dogs'
    )

@register(correct=2., intuitive=200.)
def nurses():
    return Input(
        '''
        <p>If it takes 2 nurses 2 minutes to measure the blood of 2 patients, 
        how many minutes would it take 200 nurses to measure the blood of 200 
        patients?</p>
        ''',
        var='CRT_Nurses', append='minutes', 
        extra_attrs=dict(type='number', min=0, step='any'),
        debug=_debug_functions(2, 200)
    )

@register(correct=2.25, intuitive=2.5)
def soup_salad():
    return Input(
        '''
        <p>Soup and salad cost $5.50 in total. The soup costs a dollar more 
        than the salad. How much does the salad cost?</p>
        ''',
        var='CRT_SoupSalad', prepend='$', 
        extra_attrs=dict(type='number', min=0, max=5.5, step=.01),
        debug=_debug_functions(2.25, 2.5)
    )

# http://www.keithstanovich.com/Site/Research_on_Reasoning_files/Toplak_West_Stanovich_14.pdf
@register(correct=4., intuitive=9.)
def drinking_water():
    return Input(
        '''
        <p>If John can drink one barrel of water in 6 days, and Mary can 
        drink one barrel of water in 12 days, how many days would it take 
        them to drink one barrel of water together?</p>
        ''',
        var='CRT_DrinkingWater', append='days', 
        extra_attrs=dict(type='number', min=0, step='any'),
        debug=_debug_functions(4, 9)
    )

@register(correct=29., intuitive=30.)
def students():
    return Input(
        '''
        <p> Jerry received both the 15th highest and the 15th lowest mark in 
        the class. How many students are in the class?</p>
        ''',
        var='CRT_Students', append='students', 
        extra_attrs=dict(type='number', min=1),
        debug=_debug_functions(29, 30)
    )

@register(correct=20., intuitive=10.)
def pig():
    return Input(
        '''
        <p>A man buys a pig for $60, sells it for $70, buys it back for $80, 
        and sells it finally for $90. How much has he made?</p>
        ''',
        var='CRT_Pig', prepend='$', extra_attrs=dict(type='number'),
        debug=_debug_functions(20, 10)
    )

@register(correct='loss', intuitive='gain')
def stock():
    return Check(
        '''
        <p> Simon decided to invest $8,000 in the stock market one day early 
        in 2008. Six months after he invested, on July 17, the stocks he had 
        purchased were down 50%. Fortunately for Simon, from July 17 to 
        October 17, the stocks he had purchased went up 75%. At this point, 
        Simon has:</p>
        ''',
        [
            Choice('broken even in the stock market', value='even'),
            Choice('is ahead of where he began', value='gain'),
            Choice('has lost money', value='loss')
        ],
        var='CRT_Stock'
    )