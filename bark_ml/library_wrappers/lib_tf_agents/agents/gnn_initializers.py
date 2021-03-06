from bark_ml.library_wrappers.lib_tf_agents.networks.gnns.graph_network import GraphNetwork
from bark_ml.library_wrappers.lib_tf_agents.networks.gnns.interaction_wrapper import InteractionWrapper


def init_interaction_network(name, params):
  return InteractionWrapper(
    params=params, 
    name=name + "_InteractionNetwork")
  
def init_gnn_edge_cond(name, params):
  return GEdgeCondWrapper(
    params=params, 
    name=name + "_GEdgeCond")