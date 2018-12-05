from lib3to2.tests.support import lib3to2FixerTestCase

class Test_fstring(lib3to2FixerTestCase):
    fixer = "fstring"

    def test_fstring(self):
        b = """f'test: {a}'"""
        a = """u'test: ' + unicode(a)"""
        self.check(b, a)
