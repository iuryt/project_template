"""Example science module.

Name your real modules for *what they are* (``geostrophy.py``, ``mixing.py``,
``spectra.py``) -- not generic ``dataset.py`` / ``features.py``. This one is a
placeholder holding a single trivial function used by the toy pipeline and tests.
"""

import numpy as np


def rms(x):
    """Root-mean-square of an array-like."""
    return float(np.sqrt(np.mean(np.asarray(x) ** 2)))
