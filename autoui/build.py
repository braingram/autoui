#!/usr/bin/env python

import copy
import logging
import Tkinter


logger = logging.getLogger(__name__)


def spin_changed(ui_element):
    ui_element['control'].config(bg='red')


def spin_key_press(event, ui_element):
    # print("pressed: %s" % event.keycode)
    if event.keycode & 0xFF in (13, 36):
        val = ui_element['variable'].get()
        if (val >= ui_element['spec']['min']) and \
                (val <= ui_element['spec']['max']):
            logger.info("{} : {}".format(ui_element['spec']['name'], val))
            ui_element['spec']['setter'](val)
            ui_element['control'].config(bg='green')


def check_toggled(ui_element):
    val = ui_element['variable'].get()
    logger.info("{} : {}".format(ui_element['spec']['name'], val))
    ui_element['spec']['setter'](val)


def create_control(control_type, frame, k, name, s, ui, v):
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


def build_ui(spec, root=None, update_interval=100, on_update=None):
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
            control, ui, v = create_control(s['control'], frame, k, name,
                                            s, ui, v)
            control.pack(side=Tkinter.LEFT)
        frame.pack(fill=Tkinter.BOTH, side=Tkinter.TOP)
    ui['_root'] = root
    if update_interval is not None:
        if on_update is None:
            on_update = lambda: None

        def update():
            on_update()
            for k in ui:
                if k[0] == '_':
                    continue
                if ui[k]['spec'].get('update', False):
                    ui[k]['variable'].set(ui[k]['spec']['getter']())
            root.after(update_interval, update)

        root.after(update_interval, update)

    return ui


def build_split_ui(spec, root=None, update_interval=100,
                   on_update=None):
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
    """
    When setting up the split ui, some number of the widgets will go on the
    left, while the other number will go on the right. Each set of widgets will
    utilize two column spaces to accomodate their labels. This is most simple
    with a half split."""
    total_widgets = len(spec)
    half = int(total_widgets / 2)
    counter = 0
    left_counter = 0
    right_counter = 0
    if root is None:
        root = Tkinter.Tk()
    frame = Tkinter.Frame(root)
    if half + half < total_widgets:
        half += 1
    print half, total_widgets
    for r in range(half):
        frame.rowconfigure(r, pad=3)
    frame.columnconfigure(0, pad=3)
    frame.columnconfigure(1, pad=3)
    frame.columnconfigure(2, pad=3)
    frame.columnconfigure(3, pad=3)
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
        ui[k]['frame'] = frame
        if 'text' in s:
            label = Tkinter.Label(frame, text=s['text'], fg="black",
                                  justify=Tkinter.LEFT, relief=Tkinter.RIDGE,
                                  wraplength=400)
        else:
            label = Tkinter.Label(frame, text=name, fg='blue')
        ui[k]['label'] = label
        if (counter % 2) == 0:
            label.grid(row=left_counter, column=1, sticky=Tkinter.W+Tkinter.E)
        else:
            label.grid(row=right_counter, column=3,
                       sticky=Tkinter.W+Tkinter.E)
        if 'text' not in s:
            control, ui, v = create_control(s['control'], frame, k, name,
                                            s, ui, v)
            if (counter % 2) == 0:
                control.grid(row=left_counter, column=0,
                             sticky=Tkinter.W+Tkinter.E)
            else:
                control.grid(row=right_counter, column=2,
                             sticky=Tkinter.W+Tkinter.E)
        if (counter % 2) == 0:
            left_counter += 1
        else:
            right_counter += 1
        counter += 1
        frame.pack(fill=Tkinter.BOTH, side=Tkinter.LEFT)
    ui['_root'] = root
    if update_interval is not None:
        if on_update is None:
            on_update = lambda: None

        def update():
            on_update()
            for k in ui:
                if k[0] == '_':
                    continue
                if ui[k]['spec'].get('update', False):
                    ui[k]['variable'].set(ui[k]['spec']['getter']())
            root.after(update_interval, update)

        root.after(update_interval, update)

    return ui


def run():
    Tkinter.mainloop()
