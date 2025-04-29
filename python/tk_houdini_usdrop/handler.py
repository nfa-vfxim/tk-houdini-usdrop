import sgtk
import hou
import os
import re


class TkUSDRopNodeHandler(object):
    def __init__(self, app):
        self.app = app

    def execute_export(self, node, is_background_export):
        inputs = node.inputs()
        if len(inputs) > 0:
            file_path = self.calculate_path(node)
            self.execute_usd_export(node, file_path, is_background_export)
        else:
            message = "ShotGrid USD ROP node not connected to any input."
            self.app.logger.debug(message)
            hou.ui.displayMessage(message, severity=hou.severityType.Error)

    def calculate_path(self, node):
        # Get all necessary data
        current_filepath = hou.hipFile.path()
        work_template = self.app.get_template("work_file_template")
        usd_template = self.app.get_template("output_publish_template")

        # Set fields
        fields = work_template.get_fields(current_filepath)
        fields["name"] = node.parm("name").eval()

        # Validate name parm is alphanumeric
        regex = re.compile("^[a-zA-Z0-9_-]*$")
        match = regex.match(fields["name"])
        if not match:
            hou.ui.displayMessage(
                "You may only use letters and numbers for the publish name!",
                severity=hou.severityType.Error,
            )
            return

        # Apply fields
        file_path = usd_template.apply_fields(fields).replace(os.sep, "/")

        return file_path

    def populate_configure_layers(self, nodes, file_path):
        for node in nodes:
            name = node.parm("name").eval()
            layer_type = self.get_layer_type(node)

            file_path = os.path.dirname(file_path)
            file_path = os.path.join(file_path, layer_type, name + ".usd").replace(
                os.sep, "/"
            )

            node.parm("filepath").set(file_path)

    @staticmethod
    def check_layer_nodes(nodes):
        # This function will validate if the SGTK Configure Layer node has a valid name
        for node in nodes:
            name = node.parm("name").eval()
            regex = re.compile("^[a-zA-Z0-9_-]*$")
            match = regex.match(name)

            # Check if name is specified on all nodes
            if len(name) <= 0:
                # Create error message
                node_name = str(node)
                hou.ui.displayMessage(
                    "Name is not specified on configure layer node %s" % node_name,
                    severity=hou.severityType.Error,
                )
                return False

            # Check for illegal characters defined by the regex
            elif not match:
                node_name = str(node)
                hou.ui.displayMessage(
                    "Configure layer node %s contains illegal characters, only letters, numbers and underscores "
                    "are allowed." % node_name,
                    severity=hou.severityType.Error,
                )
                return False

        return True

    @staticmethod
    def get_layer_type(node):
        # This will translate the values from the ordered menu to string values
        layer_value = node.parm("type").eval()
        if layer_value == 0:
            layer = "geo"
        elif layer_value == 1:
            layer = "light"
        else:
            layer = "material"

        return layer

    def execute_usd_export(self, node, file_path, is_background_export):
        # Set all SGTK Configure Layers node to the correct path
        layer_nodes = (
            hou.lopNodeTypeCategory().nodeType("sgtk_configurelayer").instances()
        )
        if self.check_layer_nodes(layer_nodes):
            self.populate_configure_layers(layer_nodes, file_path)

            # Set filepath on SGTK USD ROP node to the publish path
            if file_path is None:
                self.app.logger.error(
                    "File path is None. An invalid publish name was probably used."
                )
                return

            node.parm("path").set(file_path)

            try:
                # Execute the USD Export
                if is_background_export:
                    hou.hipFile.save()
                    node.node("usd_rop").parm("executebackground").pressButton()
                else:
                    node.node("usd_rop").parm("execute").pressButton()
                self.app.logger.debug("Exported USD %s." % file_path)

            except Exception as e:
                # Let the user know what went wrong when exporting
                hou.ui.displayMessage(str(e), severity=hou.severityType.Error)

    @staticmethod
    def get_all_usdrop_nodes():
        # Get all nodes from node type sgtk_usd_rop
        nodes = hou.lopNodeTypeCategory().nodeType("sgtk_usd_rop").instances()

        return nodes
