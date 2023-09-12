"""
ELabmount's Mount
"""
import numpy as np
from robosuite.utils.mjcf_utils import xml_path_completion
from robosuite.models.mounts.mount_model import MountModel


class ELabMount(MountModel):
    """
    Mount officially used for Rethink's Sawyer Robot. Includes a controller box and wheeled pedestal.

    Args:
        idn (int or str): Number or some other unique identification string for this mount instance
    """

    def __init__(self, idn=0):
        super().__init__(xml_path_completion("mounts/e_lab_mount.xml"), idn=idn)

    @property
    def top_offset(self):
        return np.array((0.43, 0.175, 0.92))

    @property
    def horizontal_radius(self):
        # TODO: This may be inaccurate; just a placeholder for now
        return 0.25
