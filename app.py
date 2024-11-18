"""
File Cache node App for use with Toolkit's Houdini engine.
"""

import sgtk


class TkHoudiniUSDRopNode(sgtk.platform.Application):
    def init_app(self):
        """Initialize the app."""
        tk_houdini_usdrop = self.import_module("tk_houdini_usdrop")
        self.handler = tk_houdini_usdrop.TkUSDRopNodeHandler(self)

    def execute_export(self, node, is_background_export):
        self.handler.execute_export(node, is_background_export)

    def get_nodes(self):
        # Get all nodes from this session
        nodes = self.handler.get_all_usdrop_nodes()
        return nodes

    def get_output_path(self, node):
        # Calculate output path
        output_path = self.handler.calculate_path(node)
        return output_path

    def get_work_file_template(self):
        template = self.get_template("output_usd_template")
        return template

    def get_publish_file_template(self):
        template = self.get_template("output_publish_template")
        return template
