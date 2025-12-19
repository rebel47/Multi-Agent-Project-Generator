"""
Backward compatibility bridge for legacy imports.
This allows old code to continue working while users migrate to the new system.
"""

import warnings
from agent.graph_enhanced import agent as enhanced_agent

warnings.warn(
    "Importing from agent.graph is deprecated. "
    "Please use 'from agent.graph_enhanced import agent' instead. "
    "The old import will be removed in v3.0.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export for backward compatibility
agent = enhanced_agent

__all__ = ['agent']
