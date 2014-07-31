from kivy.app import App
from kivy.properties import StringProperty
import fonts_ja

from os.path import join, dirname
import gettext
import os

'''
To set the language you need to set one of:
export CHILD_FIRST_LANG='fr'
export CHILD_FIRST_LANG='ja'
export CHILD_FIRST_LANG='en'
'''

class _(str):
    observers = []
    lang = None
    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            try:
                _.switch_lang(os.environ['CHILD_FIRST_LANG'])
            except KeyError:
                _.switch_lang('en')
        s = _.translate(s, *args, **kwargs)
        return s
        # The original call, which somehow broke things
        return super(_, cls).__new__(cls, s)

    @staticmethod
    def translate(s, *args, **kwargs):
        a = _.lang(s).format(args, kwargs)
        return a
    @staticmethod
    def bind(**kwargs):
        _.observers.append(kwargs['_'])
    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir,
            languages=[lang])
        _.lang = locales.ugettext
        # update all the kv rules attached to this text
        for callback in _.observers:
            callback()

class LangApp(App):

    lang = StringProperty('en')

    def on_lang(self, instance, lang):
        os.environ['CHILD_FIRST_LANG'] = lang
        _.switch_lang(lang)
        


LangApp().run()
