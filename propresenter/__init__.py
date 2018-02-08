__NAME__ = "propresenter"
__VERSION__ = "1.0.0"

import os
if os.name != 'nt': raise Exception("ProPresenter 6 Python library not compatible on non-Windows environments")

appDataLocation = None

import propresenter.registry
