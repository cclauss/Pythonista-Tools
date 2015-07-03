
# @Phuket2
# beware, i am a beginner programmer, if you are also a beginner programmer,
# dont try to learn from me. i think i have some ok ideas, put my code is not
# even close to being smart or refined.

# CodeHelper applet :)
# what:
# is a popover view that presents buttons you have described in data below
# that basically copies text to the clipboard. a gloried copy routine. but
# before you decide, look at the examples below. a lot can be done.

# settings:
#   1. _btns_per_line, number of btns you want displayed on a single row/line
#   2. _btn_w, _btn_h. the width and height of the buttons. The popup view,
#      will determine its frame from these vars.
#   3. _btns, is a dict. {btn title:varible}
# so an entry in _btns like 'email':'me@gmail.com' will add a button called
# 'email', when clicked will copy me@gmail.com, to the clipboard. if you write
# a varible that is the result str of a function, you get the expected results
# on the clipboard. only cavet is in the order you do this. ..... can go on
# and on....

# usage:
# To use this code, you should put in a .py file and then add the .py to
# 'Actions Menu' in Pythonista.

# Notes:
# by the virtue of pythons flexibility, this simple applet can do a lot. i did
# some simple and stupid examples. only to give an idea to what is possible

# Excuses:
# sorry, the file is a bit of a mess. but is because the data is in the same
# file as the code. The data and the data functions, should be put into
# another .py file and imported into this file.

import ui
import clipboard
import console
import datetime
import calendar
import platform

# if _debug_mode, then as well as copying to the clipboad, prints to the
# console. just for debugging and testing your output.
_debug_mode = False

_btns_per_line  = 3
_btn_h = 48
_btn_w = 120

# only examples of what you can do that makes sense to you
def make_week_day_header(width = 3):
    return str(calendar.weekheader(width))

def zen_text():
    import StringIO, sys
    prev_out = sys.stdout
    sys.stdout = StringIO.StringIO()
    import this
    reload(this)
    the_text = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = prev_out
    return the_text

_text_weekday_header = make_week_day_header()

_code_div = '# {} section {}'.format('/' * 25, '\\' * 25)

_text_comment = '{0}\nYour comment\n{0}'.format("'''")

_text_platform = platform.platform()

_text_date_stamp = str(datetime.datetime.today())

_text_zen = zen_text()

_text_init = '''
    def __init__(self):
        pass
'''

_text_main = '''
if __name__ == '__main__':
    pass
'''

_text_class = '''
class MyClass(object):
    def __init__(self):
        pass
'''

_text_forum = '''
#Comments here

```python
#your code here
```
'''

_text_sig = '''
# @Phuket2
# beware i am a beginner programmer, if you are also a beginner programmer,
# dont try to learn from me. i think i have some ok ideas, put my code is not
# even close to being smart or refined.
'''
# key = name of button, value = text, can be a literal, from a var defined
# above of result of a funtion that returns a string, losely speaking... you
# can see the examples above.

_btns ={'init': _text_init,
     'main': _text_main,
     'class': _text_class,
     'forum': _text_forum,
     'sig': _text_sig,
     'email': 'my_email@google.com',
     'Zen': _text_zen,
     'datestamp': _text_date_stamp,
     'platform': _text_platform,
     'comment': _text_comment,
     'weekday head': _text_weekday_header,
     'code div': _code_div }

#////////////code starts here\\\\\\\\\\\\\\\

def make_button(index, the_title):
    btn = ui.Button(name=str(index), title=the_title)
    #btn.name = str(index)
    btn.background_color = 'purple'
    btn.border_width = .5
    btn.tint_color = 'white'
    btn.font = ('<system-bold>', 16)
    # a little crappy to do like this, but just a quick tool
    btn.width = _btn_w
    btn.height = _btn_h
    return  btn

def action(sender):
    clipboard.set(_btns[sender.title])
    sender.superview.close()
    console.hud_alert('Copied', duration = .4)

    # print to the console, if in debug mode
    if _debug_mode:
        print _btns[sender.title]

def rows_to_write(num_btn, btn_per_row):
    ln, p_ln = divmod( num_btn, btn_per_row )
    if p_ln:
        ln +=1
    return(ln)

def add_btns(view, rows):

    for k, v in enumerate(_btns):
        btn = make_button(k, v)
        btn.action = action
        w,h = btn.width , btn.height
        btn.frame = (k % _btns_per_line * w,
                     k / _btns_per_line * h, w, h)
        view.add_subview(btn)

if __name__ == '__main__':
    view = ui.View()
    view.name = 'Code Helper'
    rows = rows_to_write(len(_btns), _btns_per_line )
    view.frame = (0,0,_btn_w * _btns_per_line ,_btn_h * rows)
    add_btns(view, rows)
    view.present('popover')
