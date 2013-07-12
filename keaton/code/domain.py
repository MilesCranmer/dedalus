

import numpy as np

from fields import Field


class Domain(object):
    """Problem domain."""

    def __init__(self, bases):

        # Inputs
        self.bases = bases

        # Build shape
        self.shape = tuple([b.size for b in bases])
        self.dim = len(self.shape)

        # Grid
        self.grid = bases[-1].grid

        # Pencil slices
        self.slices = [slice(None)]

    def create_field(self):

        return Field(self)

