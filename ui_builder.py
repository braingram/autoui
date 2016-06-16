#!/usr/bin/env python


import copy
import Tkinter


def spin_changed(ui_element):
    ui_element['control'].config(bg='red')


def spin_key_press(event, ui_element):
    print("pressed: %s" % event.keycode)
    if event.keycode & 0xFF in (13, 36):
        val = ui_element['variable'].get()
        if (val >= ui_element['spec']['min']) and \
                (val <= ui_element['spec']['max']):
            # logger.info("{} : {}".format(ui_element['spec']['name'], val))
            ui_element['spec']['setter'](val)
            ui_element['control'].config(bg='green')


def check_toggled(ui_element):
    val = ui_element['variable'].get()
    # logger.info("{} : {}".format(ui_element['spec']['name'], val))
    ui_element['spec']['setter'](val)


def create_widget_control(control_type, frame, k, name, s, ui, v):
    if control_type == Tkinter.Spinbox:
        kwargs = dict(textvariable=v)
        if 'increment' in s:
            kwargs['increment'] = s['increment']
        if 'min' in s:
            kwargs['from_'] = s['min']
        if 'max' in s:
            kwargs['to'] = s['max']
        control = Tkinter.Spinbox(frame, **kwargs)
        ui[k]['control'] = control
        ui[k]['spec']['min'] = s.get('min', float('-inf'))
        ui[k]['spec']['max'] = s.get('max', float('inf'))
        # 6) define keybinding function [for spinbox]

        v.trace("w", lambda a, b, c, ui_e=ui[k]: spin_changed(ui_e))
        control.bind("<Key>",
                     lambda e, ui_e=ui[k]: spin_key_press(e, ui_e))
        return control, ui, v
    elif control_type == Tkinter.Checkbutton:
        control = Tkinter.Checkbutton(frame, variable=v)
        ui[k]['control'] = control
        # control = Tkinter.Checkbutton(frame, text=name, variable=v)
        # 7) attach functions
        v.trace("w", lambda a, b, c, ui_e=ui[k]: check_toggled(ui_e))
        return control, ui, v
    elif control_type == Tkinter.Label:
        control = Tkinter.Label(frame, textvariable=v)
        ui[k]['control'] = control
        return control, ui, v
    elif control_type == Tkinter.Button:
        if 'value' not in s:
            v.set(name)
        control = Tkinter.Button(
            frame, textvariable=v, command=s['command'])
        ui[k]['control'] = control
        return control, ui, v
    else:
        raise Exception("Unknown Control: {}".format(s['control']))


def build_ui(spec, root=None):
    """Auto-magically construct a tkinter ui
    spec = dictionary with
        keys = attribute names
        values = attribute spec = dictionary with
            key : value
            type : tkinter variable type
            value : optional default value
            control : tkinter control type
            min : optional min value
            max : optional max value
            increment : optional increment (for spin boxes)
            setter : setter function
            getter : getter function

    for each item in the spec a variable will be created
    """
    if root is None:
        root = Tkinter.Tk()
    ui = {}
    for (k, s) in spec:
        ui[k] = {}
        ui[k]['spec'] = copy.deepcopy(s)
        name = s.get('name', k)
        ui[k]['spec']['name'] = name
        # 1) create variable for attribute
        v = s['type']()
        ui[k]['variable'] = v
        # 2) (optional) set default value
        if 'value' in s:
            v.set(s['value'])
        # 3) create control
        # 5) define callback function
        frame = Tkinter.Frame(root)
        ui[k]['frame'] = frame
        if 'text' in s:
            label = Tkinter.Label(frame, text=s['text'], fg="black",
                                  justify=Tkinter.LEFT, relief=Tkinter.RIDGE,
                                  wraplength=400)
        else:
            label = Tkinter.Label(frame, text=name, fg='blue')
        ui[k]['label'] = label
        label.pack(side=Tkinter.LEFT)
        if 'text' not in s:
            control, ui, v = create_widget_control(s['control'], frame, k,
                                                   name, s, ui, v)
            control.pack(side=Tkinter.LEFT)
        frame.pack(fill=Tkinter.BOTH, side=Tkinter.TOP)
    ui['_root'] = root
    return ui
