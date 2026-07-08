"""Shared plotting helpers (house style, annotations, savers)."""

import matplotlib.pyplot as plt


def savefig(fig, path, *, dpi=150, **kwargs):
    """Save ``fig`` to ``path`` (creating parent dirs) and close it."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", **kwargs)
    plt.close(fig)
