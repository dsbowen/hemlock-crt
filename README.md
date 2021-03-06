Hemlock-CRT is a <a href="https://dsbowen.github.io/hemlock" target="_blank">hemlock</a> extension for adding a cognitive reflection test to hemlock projects.

## Installation

With hemlock-CLI (recommended):

```
$ hlk install hemlock-crt
```

With pip:

```
$ pip install hemlock-crt
```

## Quickstart

In this example, we add a CRT with the bat and ball, lily pads, widgets,
and students problem. Then we display the results to the participant.

In `survey.py`:

```python
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
```

`app.py` is standard from the hemlock template.

Run with:

```bash
hlk serve
```

or

```bash
python app.py
```

## Citations

```
@software{bowen2020hemlock-crt,
  author = {Dillon Bowen},
  title = {Hemlock-CRT},
  url = {https://dsbowen.github.io/hemlock-crt/},
  date = {2020-10-05},
}

@article{frederick2005cognitive,
  title={Cognitive reflection and decision making},
  author={Frederick, Shane},
  journal={Journal of Economic perspectives},
  volume={19},
  number={4},
  pages={25--42},
  year={2005}
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/hemlock-crt/blob/master/LICENSE).