# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from ._constants import Constants
from .secret import Secret

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def sign(message: str) -> str:
    import hmac, hashlib

    return hmac.new(Secret.KEY.encode(), message.encode(), hashlib.sha512).hexdigest()

def verify_hash(message: str, hash_: str) -> bool:
    return sign(message) == hash_

def get_temp_path(extension: str) -> str:
    from kcu import kpath
    import os, uuid

    temp_dir = kpath.new_tempdir(
        use_system_tmp_folder_for_macos=True,
        create_folder_if_not_exists=True,
        appending_subpath=Constants.TTS_TEMP_FOLDER_NAME,
        append_random_subfolder_path=False
    )

    print('temp_dir', temp_dir)

    os.makedirs(temp_dir, exist_ok=True)
    return os.path.join(temp_dir, '{}.{}'.format(uuid.uuid4(), extension.lstrip('.')))


# ---------------------------------------------------------------------------------------------------------------------------------------- #