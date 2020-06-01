#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shelve
import db_config

ROOT = os.getcwd()


class Shelf:

    def __init__(self):
        self.db = shelve.open('db')

    def set(self, key, value):
        self.db[key] = value

    def add_elem(self, key, value):
        try:
            self.db[key].add(value)
        except KeyError:
            pass

    def get(self, key):
        return self.db[key]

    def close(self):
        self.db.close()


# d = Shelf()
# # appointment = db_config.appointment
# # problem = db_config.problem
# # advice = db_config.advice
# d.set('other', set([]))
# # print(type(d.get('advice')))
# d.close()
