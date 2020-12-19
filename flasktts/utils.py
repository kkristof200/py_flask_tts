# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .constants import Constants

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def sign(message: str) -> str:
    import hmac, hashlib

    return hmac.new(Constants.SECRET_KEY.encode(), message.encode(), hashlib.sha512).hexdigest()

def verify_hash(message: str, hash_: str) -> bool:
    return sign(message) == hash_


# ---------------------------------------------------------------------------------------------------------------------------------------- #