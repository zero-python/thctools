#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-19
"""


class Event(object):
    def __init__(self):
        self.__handlers = []

    def register(self, handler):
        if handler not in self.__handlers:
            self.__handlers.append(handler)

    def append(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def unregister(self, handler):
        if handler in self.__handlers:
            self.__handlers.remove(handler)


class DataSeries(object):
    def __init__(self):
        self.event = Event()
        self.__values = []
        self.__dateTimes = []
        self.data = {}

    def append(self, value):
        self.__values.append(value)
        self.event.append(value)

    def appendWithDateTime(self, dateTime, value):
        if dateTime is not None and len(self.__dateTimes) != 0 and self.__dateTimes[-1] >= dateTime:
            raise Exception("Invalid datetime. It must be bigger than that last one")
        assert (len(self.__values) == len(self.__dateTimes))
        self.__dateTimes.append(dateTime)
        self.__values.append(value)
        self.event.append(self, dateTime, value)

    def getData(self):
        return self.data

    def addData(self, data):
        self.data = data
