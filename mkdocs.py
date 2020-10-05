from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/hemlock-crt/blob/master')

path = 'hemlock_crt/__init__.py'
soup = PySoup(path=path, src_href=src_href)
soup.keep_objects('crt', 'register')
compile_md(soup, outfile='docs_md/api.md')