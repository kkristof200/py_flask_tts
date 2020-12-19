# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# Local
from .constants import SECRET_KEY

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def sign(message: str) -> str:
    import hmac, hashlib

    return hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha512).hexdigest()

def verify_hash(message: str, hash_: str) -> bool:
    return sign(message) == hash_


# ---------------------------------------------------------------------------------------------------------------------------------------- #