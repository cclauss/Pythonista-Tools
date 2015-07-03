# coding: utf-8

from __future__ import print_function  # a bit of Python 3 compatibility ;-)

# not: thinking out Aloud ;-)

import console, sys, ui

'''
    UIClassAttrInfo
    this is a test class, collecting attribute information about ui elements.
    not meant for runtime, more a tool, not necessarily useful.
'''
_nl = "\n"
_sp = ' '

# list of the standard ui elements
_ui_objects = [ui.View, ui.Button, ui.ButtonItem, ui.ImageView, ui.Label,
    ui.NavigationView, ui.ScrollView, ui.SegmentedControl, ui.Slider,
    ui.Switch, ui.TableView, ui.TableViewCell, ui.TextField, ui.TextView,
    ui.WebView,  ui.DatePicker]

# a list of attributes that can not filtered out automatically, but should not
# be exposed in this class. well, thats my opion, maybe wrong
# if you dont ignore subviews, a error will occur
# if you dont ignore, transform, content_view and text_label you will get an
# object reference in memory for the attr. seems like better to leave these
# out.
# seems to be no references to autoresizing in the documentation.
# i am guessing bg_color is in for backward compatibility.

_attr_ignore = '''superview subviews transform content_view image_view
    text_label on_screen autoresizing bg_color'''.split()

# a entry of attribute:value will replace the default attribute.
_attr_override = { 'font' : ('<system>', 18),
                   'tint_color' : "'white'",
                   'date' : None }

def big_fail_hard_exit(func_name, param, exception):
    fmt = '{}\nwe should not get here: {}({})\n{}: {}'
    sys.exit(fmt.format('*' * 100, func_name, param,
        type(exception), exception))

class UIClassAttrInfo(object):
    def __init__(self, ui_element):
        # this needs to be done for ui.NavigationView otherwise, big fail
        is_nav = ui_element == ui.NavigationView
        self.obj = obj = ui_element(ui.View()) if is_nav else ui_element()

        # mangle a class name from obj
        self.class_name = obj.__doc__.split()[0]

        # get the settable attr names from a normal ui.View
        self.uiView_attrs = self.get_attr_names(ui.View())

        # get the settable attr from the passed obj
        self.attrs = self.get_attr_names(obj)

        #get the settable attr of obj that are not in ui.View
        self.u_attrs = self.get_u_attrs(self.uiView_attrs, self.attrs)

        self.attr_values = self.get_attr_values(obj, self.attrs)


    def get_attr_names(self, obj):
        '''
            get the settable attrs from the obj passed in.
            _attr_ignore, is looked up before adding the attr
        '''
        attr_list=[]
        attributes = dir(obj)
        for attr in attributes:
            if attr in _attr_ignore:
                # _attr_ignore, a list of attrs to ignore
                continue
            try:
                if not callable(getattr(obj,attr)) and attr[:2] != '__':
                    attr_list.append(attr)
            except Exception as e:
                big_fail_hard_exit('get_attr_names', attr, e)
        return attr_list

    def get_u_attrs( self, view_attr, obj_attr):
        # uses sets to get the attrs that are in obj but not in the ui.View
        # could be useful
        return list(set.difference(set(obj_attr), set(view_attr)))

    def get_u_attrs( self, view_attrs, obj_attrs):
        # uses sets to get the attrs that are in obj but not in the ui.View
        # could be useful
        return (attr for attr in obj_attrs if attr not in view_attrs)

    def get_attr_values(self, obj, attrs):
        '''
            make and return a dict of attr with the default values
        '''
        lst = []

        for attr in attrs:
            if attr in _attr_override:
                lst.append((attr, _attr_override[attr] ))
            else:
                try:
                    x = eval('obj.' + attr)
                    lst.append((attr, x))
                except Exception as e:
                    big_fail_hard_exit('get_attr_values', attr, e)

        return lst

    def a_write_method(self):
        # an example of how this class could write out attribute classes.

        print('class ' + self.class_name + 'AttrInfo(' + 'object' + '):')

        print(_sp * 2 + 'def __init__(' + 'self ):')

        print(_sp * 4 + 'self.attr_list =' + str(self.attrs))

        print(_nl)

        print(_sp * 4 + 'self.attr_list_u =' + str(self.u_attrs))
        print(_nl)

        #write of the attr names with default values
        for t in self.attr_values:
            attr , val = t
            print(_sp * 4 + 'self.' + attr + ' = ' + str( str(val) if len(str(val)) > 0 else "''"))

        print(_nl)

    def __str__(self):
        # you can remove <__str__()> and </__str__()> after comparison testing
        fmt = '''<__str__()>
class {}AttrInfo(object):
  def __init__(self):

    self.attr_list = {}

    self.attr_list_u = {}

{}
</__str__()>
'''
        return fmt.format(self.class_name, self.attrs, self.u_attrs,
            '\n'.join('    self.{} = {}'.format(key,
                value if len(str(value)) else "''")
                for key, value in self.attr_values))

if __name__== '__main__':
    for obj in _ui_objects:
        # only collect the attribute
        cls_info  = UIClassAttrInfo(obj)
        #write to the console
        cls_info.a_write_method()
        print(cls_info)
    console.hud_alert('completed')
