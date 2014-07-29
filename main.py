from kivy.app import App
from kivy.properties import StringProperty
import fonts_ja

from os.path import join, dirname
import gettext
import os

# To set the language you need to set
#export CHILD_FIRST_LANG='fr'
__file__='/Users/jerome/Downloads/kivy-gettext-example-master-2/main.py'
class _(str):
    observers = []
    lang = None
    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            try:
                _.switch_lang(os.environ['CHILD_FIRST_LANG'])
            except KeyError:
                _.switch_lang('en')
        print("s is", s)
        s = _.translate(s, *args, **kwargs)
        print(s)
        return s
        return super(_, cls).__new__(cls, s)

    @staticmethod
    def translate(s, *args, **kwargs):
        print(s, args, kwargs)
        a = _.lang(s).format(args, kwargs)
        print("a is fine")
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

_(u"Hello World")

class LangApp(App):

    lang = StringProperty('en')

    def on_lang(self, instance, lang):
        os.environ['CHILD_FIRST_LANG'] = lang
        _.switch_lang(lang)
        


LangApp().run()
