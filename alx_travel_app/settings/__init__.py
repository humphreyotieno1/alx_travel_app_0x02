from .base import *

# Import development settings if DEBUG is True
if DEBUG:
    try:
        from .local import *
    except ImportError:
        pass
else:
    try:
        from .production import *
    except ImportError:
        pass
