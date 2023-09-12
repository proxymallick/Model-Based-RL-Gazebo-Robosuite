from .mount_model import MountModel
from .mount_factory import mount_factory

from .rethink_mount import RethinkMount
from .rethink_minimal_mount import RethinkMinimalMount
from .e_lab_mount import ELabMount
from .null_mount import NullMount


MOUNT_MAPPING = {
    "RethinkMount": RethinkMount,
    "RethinkMinimalMount": RethinkMinimalMount,
    "ELabMount": ELabMount,
    None: NullMount,
}

ALL_MOUNTS = MOUNT_MAPPING.keys()
