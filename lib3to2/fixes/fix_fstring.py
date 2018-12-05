"""
Fixer for:
f"spam {len(range(10)}" -> u"spam " + unicode((len(range(10))))
"""

import re
from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

_literal_re = re.compile(r"[fF]?[\'\"]")


def parse_fstring(s):
    pos = 0
    length = len(s)
    while pos < length:
        found = s.find("{", pos)
        if found == -1:
            break
        level = 0
        while pos < length - 1:
            pos += 1
            char = s[pos]
            if char == "{":
                level += 1
            elif char == "}":
                if level > 1:
                    level -= 1
                else:
                    pos += 1
                    yield (found, pos)
                    break

def detect_quotation(s):
    for qm in ("'''", '"""', "'", '"'):
        if s.startswith(qm) and s.endswith(qm):
            return qm

def unquote(s):
    qm = detect_quotation(s)
    if s.startswith(qm) and s.endswith(qm):
        ql = len(qm)
        return s[ql:-ql]
    return s


def quote(s, qm):
    # XXX: inner string should be escaped correctly 
    return qm + s + qm


def replace_fstring(s, qm):
    pos = 0
    length = len(s)
    result = []
    for (begin, end) in parse_fstring(s):
        if begin > pos:
            result.append("u" + quote(s[pos:begin], qm))
        result.append("unicode(" + s[begin + 1:end - 1] + ")")
        pos = end
    if pos < length:
        result.append("u" + quote(s[pos:], qm))
    return " + ".join(result)



class FixFstring(fixer_base.BaseFix):

    PATTERN = "STRING"

    def transform(self, node, results):
        new = node.clone()
        assert node.type == token.STRING
        if _literal_re.match(new.value):
            qs = new.value[1:]
            # TODO: support raw formatted strings
            qm = detect_quotation(qs)
            new.value = replace_fstring(unquote(qs), qm)
            return new


