"""
Warn about features that are not present in Python 2.5, giving a message that
points to the earliest version of Python 2.x (or 3.x, if none) that supports it
"""

from feature_base import Feature, Features
from lib2to3 import fixer_base

FEATURES = [
   #(FeatureName,
   #    FeaturePattern,
   # FeatureMinVersion,
   #),
    ("memoryview",
        "power < 'memoryview' trailer < '(' any* ')' > any* >",
     "2.7",
    ),
    ("numbers",
        """import_from< 'from' 'numbers' 'import' any* > |
           import_name< 'import' ('numbers' dotted_as_names< any* 'numbers' any* >) >""",
     "2.6",
    ),
    ("abc",
        """import_name< 'import' ('abc' dotted_as_names< any* 'abc' any* >) > |
           import_from< 'from' 'abc' 'import' any* >""",
     "2.6",
    ),
    ("io",
        """import_name< 'import' ('io' dotted_as_names< any* 'io' any* >) > |
           import_from< 'from' 'io' 'import' any* >""",
     "2.6",
    ),
    ("bin",
        "power< 'bin' trailer< '(' any* ')' > any* >",
     "2.6",
    ),
    ("formatting",
        "power< any trailer< '.' 'format' > trailer< '(' any* ')' > >",
     "2.6",
    ),
    ("nonlocal",
        "global_stmt< 'nonlocal' any* >",
     "3.0",
    ),
]

class FixFeatures(fixer_base.BaseFix):

    # To avoid spamming, we only want to warn for each feature once.
    features_warned = set()

    # Build features from the list above
    features = Features(Feature(name, pattern, version) for \
                                name, pattern, version in FEATURES)

    PATTERN = features.PATTERN

    def match(self, node):
        to_ret = super(FixFeatures, self).match(node)
        # We want the mapping only to tell us the node's specific information.
        try:
            del to_ret['node']
        except Exception:
            # We want it to delete the 'node' from the results
            # if it's there, so we don't care if it fails for normal reasons.
            pass
        return to_ret
    
    def transform(self, node, results):
        for feature_name in results:
            if feature_name in self.features_warned:
                continue
            else:
                curr_feature = self.features[feature_name]
                if curr_feature.version >= "3":
                    fail = self.cannot_convert
                else:
                    fail = self.warning
                fail(node, reason=curr_feature.message_text())
                self.features_warned.add(feature_name)
