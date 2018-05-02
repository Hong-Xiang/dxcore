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
