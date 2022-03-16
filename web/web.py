from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *


def main():
    text = textarea('Text Area', rows=3, placeholder='Some text')
    put_text('text = %r' % text)
    text = textarea('Text Area', rows=3, placeholder='Some text')
    put_text('text = %r' % text)
    text = textarea('Text Area', rows=3, placeholder='Some text')
    put_text('text = %r' % text)



start_server(main, port=8080, debug=True)