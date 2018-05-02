"""
Useage:

1. load config to a dict object
2. following these codes:

```
dct = {
    'aaa':{
        'bbb':{
            'x': 1,
            'y': 2,
        }
        'z' : 3,
    }
}
c = create_config_tree()
v = create_view(c, 'aaa/bbb')
v['x']
>>> 1
v['y']
>>> 2
v['z']
>>> 3
```

"""
"""
Config module make it easy for config intens projects.

Config module consists of following classes:
ConfigsViewer:
    Configs viewer class.

ConfigsMaker:
    

"""
"""
New design:
    This package should consisted of the following classes:

    1.  Viewer (R)
        A Viewer is a object with 
        Provide facility for querying config via:
            normal key/name: `'key'`
            path-like: `'aaa/bbb/ccc'` and `'aaa.bbb.ccc'` (configurable)
    
    2.  Loader (C)
        Construct config tree from files/scripts
    
    3.  Updator (U)
        Update config tree
    
    4.  CNode / CTree (Model)
        Data structure of storing configs in memory
        Support serilization to .json/.yaml

        To deal with multiple config tree combination (multiple default):
            CNodeAnonymous
    
    Also provide the following helper functions:
    default() -> default config tree
"""

# from .base import Configs
# from .module_config import ModuleConfigs
# from ._viewer import ConfigsView
# from ._configurable import configurable

from .cnode import from_dict as create_config_tree
from .view import create_view