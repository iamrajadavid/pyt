from .base_cfg import AssignmentNode
from .constraint_table import constraint_table
from .reaching_definitions_base import ReachingDefinitionsAnalysisBase
from pyt.utils.log import enable_logger, logger
enable_logger(to_file='./pyt.log')


class ReachingDefinitionsTaintAnalysis(ReachingDefinitionsAnalysisBase):
    """Reaching definitions analysis rules implemented."""

    def fixpointmethod(self, cfg_node):
        logger.debug("[FIDI] cfg_node is %s", cfg_node)
        JOIN = self.join(cfg_node)
        # Assignment check
        if isinstance(cfg_node, AssignmentNode):
            arrow_result = JOIN

            # Reassignment check:
            if cfg_node.left_hand_side not in\
               cfg_node.right_hand_side_variables:
                arrow_result = self.arrow(JOIN, cfg_node)

            logger.debug("[FIDI] cfg_node.right_hand_side_variables is %s", cfg_node.right_hand_side_variables)
            arrow_result = arrow_result | self.lattice.el2bv[cfg_node]
            constraint_table[cfg_node] = arrow_result
        # Default case:
        else:
            if cfg_node.label.startswith("subp"):
                logger.debug("SPECIAL, not assignment is %s", cfg_node)
                logger.debug("SPECIAL, JOIN is %s", bin(JOIN))
            constraint_table[cfg_node] = JOIN
