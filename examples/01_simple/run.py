#!/usr/bin/env python

import Tkinter

import autoui


class Thingy(object):
    def __init__(self):
        self.some_number = 1.
        self.some_other_number = 2.
        self.string = "hello world"
        self.result = None

    def add(self):
        print("Add: %s, %s" % (self.some_number, self.some_other_number))
        self.result = self.some_number + self.some_other_number

    def multiply(self):
        print("Multiply: %s, %s" % (self.some_number, self.some_other_number))
        self.result = self.some_number * self.some_other_number

    def subtract(self):
        print("Subtract: %s, %s" % (self.some_number, self.some_other_number))
        self.result = self.some_number - self.some_other_number

    def divide(self):
        print("Divide: %s, %s" % (self.some_number, self.some_other_number))
        self.result = self.some_number / self.some_other_number


obj = Thingy()

spec = [
    ('Helpful Tip #1', {
        'control': Tkinter.Label,
        'type': Tkinter.StringVar,
        'text': "This is helpful text",
    }),
    ('some_number', {
        'name': 'Some Number',
        'control': Tkinter.Spinbox,
        'increment': 0.01,
        'type': Tkinter.DoubleVar,
        'value': obj.some_number,
        'getter': lambda: getattr(obj, 'some_number'),
        'setter': lambda v: setattr(obj, 'some_number', v),
    }),
    ('some_other_number', {
        'name': 'Some Other Number',
        'control': Tkinter.Spinbox,
        'increment': 0.01,
        'type': Tkinter.DoubleVar,
        'value': obj.some_other_number,
        'getter': lambda: getattr(obj, 'some_other_number'),
        'setter': lambda v: setattr(obj, 'some_other_number', v),
    }),
    ('result', {
        'name': 'Result',
        'control': Tkinter.Label,
        'type': Tkinter.DoubleVar,
        'getter': lambda: getattr(obj, 'result'),
        'update': True,
    }),
    ('multiply', {
        'name': 'Multiply',
        'control': Tkinter.Button,
        'type': Tkinter.StringVar,
        'command': obj.multiply,
    }),
]

r = autoui.build_ui(spec)
autoui.run()
