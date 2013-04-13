import os
import platform

__all__ = [
    'SKYPE_ROOT',
]

OS_PLATFORM = platform.system()

if OS_PLATFORM == 'Darwin':
    HOME = os.path.expanduser('~')
    SKYPE_ROOT = os.path.join(
        HOME, 'Library', 'Application Support', 'Skype'
    )
    OUTPUT = os.path.join(HOME, 'Documents', 'Converted Chats')
