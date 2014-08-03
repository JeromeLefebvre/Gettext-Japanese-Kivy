from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from os.path import join, dirname
from os import environ
import gettext

import fonts_ja

'''
To set the language you need to set one of one enviroment variables:
export CHILD_FIRST_LANG='fr' 
export CHILD_FIRST_LANG='ja'
export CHILD_FIRST_LANG='en'
'''


class _(str):
    lang = None

    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            try:
                _.switch_lang(environ['CHILD_FIRST_LANG'])
            except KeyError:
                _.switch_lang('en')
        return _.translate(s, *args, **kwargs)

    @staticmethod
    def translate(s, *args, **kwargs):
        return _.lang(s).format(args, kwargs)

    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir,
                                      languages=[lang])
        _.lang = locales.ugettext


class LangApp(App):

    lang = StringProperty('en')

    def on_lang(self, instance, lang):
        environ['CHILD_FIRST_LANG'] = lang
        _.switch_lang(lang)


LangApp().run()
