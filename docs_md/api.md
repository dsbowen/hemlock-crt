<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Cognitive Reflection Test (CRT)

Frederick, Shane (2005). "Cognitive Reflection and Decision Making". Journal of Economic Perspectives. 19 (4): 25–42. https://www.aeaweb.org/articles?id=10.1257/089533005775196732.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock_crt.**crt**

<p class="func-header">
    <i>def</i> hemlock_crt.<b>crt</b>(<i>*items, page=False, require=False, shuffle=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock-crt/blob/master/hemlock_crt/__init__.py#L11">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*items : <i>str</i></b>
<p class="attr">
    The names of CRT items. If no items are given, the standard 3-item CRT is used. <a href="items.md">See the full list of available items.</a>.
</p>
<b>page : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that items should be in separate pages.
</p>
<b>require : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that responses are required.
</p>
<b>shuffle : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that items should be shuffled.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>CRT items : <i>list</i></b>
<p class="attr">
    List of <code>hemlock.Question</code> if not <code>page</code>, otherwise list of <code>hemlock.Page</code>.
</p></td>
</tr>
    </tbody>
</table>



##hemlock_crt.**register**

<p class="func-header">
    <i>def</i> hemlock_crt.<b>register</b>(<i>correct, intuitive, key=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock-crt/blob/master/hemlock_crt/__init__.py#L59">[source]</a>
</p>

Register a new CRT item.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>correct : <i></i></b>
<p class="attr">
    The correct answer.
</p>
<b>intuitive : <i></i></b>
<p class="attr">
    The intuitive answer.
</p>
<b>key : <i>str</i></b>
<p class="attr">
    Name of the CRT item.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock_crt import register

@register(correct=5., intuitive=10.)
def bat_ball():
    return Input(
        '''
        <p>A bat and a ball cost $1.10 in total. The bat costs $1 more
        than the ball.</p>
        <p>How many cents does the ball cost?</p>
        ''',
        var='CRT_BatBall', append='cents',
        type='number', min=0, max=110
    )
```