import logging
import apprise
import knime_extension as knext
import pandas as pd
LOGGER = logging.getLogger(__name__)

paradigmchange_nodes = knext.category(
        path="/",
        level_id="paradigmchange_nodes",
        name="ParadigmChange Nodes",
        description="ParadigmChange Nodes for KNIME",
        icon="icons/exchange-64-freepik.png",
)

apprise_nodes = knext.category(
        path="/paradigmchange_nodes/",
        level_id="apprise_nodes",
        name="Apprise Nodes",
        description="Apprise Notifications for KNIME",
        icon="icons/megaphone-64-freepik.png",
)

@knext.node(name="Notify Single URL", node_type=knext.NodeType.SINK, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
@knext.input_table(name="Input Data", description="Just a stub for connecting the node to a workflow")
class AppriseNotifierSingle:
    """
    This is the most simple Node in the collection of the *Apprise Nodes*.
    It can be used to send a simple notification to a single service URL.

    See Apprise documentation for more details regarding supported notification URLs: https://github.com/caronc/apprise#supported-notifications

    Icons for ParadigmChange Nodes and Apprise Nodes are taken from Freepik: https://www.freepik.com
    """

    apprise_url = knext.StringParameter("Apprise URL", "See here https://github.com/caronc/apprise/wiki", "pover://user@token/DEVICE")
    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")

    def configure(self, configure_context, input_schema_1):
        pass 

    def execute(self, exec_context, input_1):

        apobj = apprise.Apprise()

        LOGGER.info("Adding url" + self.apprise_url + "to Apprise...")
        apobj.add(self.apprise_url)

        apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        apobj.clear()

        return

@knext.node(name="Notify Multiple URLs", node_type=knext.NodeType.SINK, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
@knext.input_table(name="Input Data", description="Just a stub for connecting the node to a workflow")
class AppriseNotifierMultiple:
    """
    This is another rather simple Node in the collection of the *Apprise Nodes*.
    It can be used to send a simple notification to *up to five* service URLs.

    See Apprise documentation for more details regarding supported notification URLs: https://github.com/caronc/apprise#supported-notifications

    Icons for ParadigmChange Nodes and Apprise Nodes are taken from Freepik: https://www.freepik.com
    """

    apprise_url1 = knext.StringParameter(
        label = "Apprise URL 1",
        description = "See here for details: https://github.com/caronc/apprise/wiki",
        default_value= "pover://user@token/DEVICE"
        )
    apprise_url2 = knext.StringParameter(
        label = "Apprise URL 2",
        description = "See here for details: https://github.com/caronc/apprise/wiki",
        default_value= "empty:"
        )
    apprise_url3 = knext.StringParameter(
        label = "Apprise URL 3",
        description = "See here for details: https://github.com/caronc/apprise/wiki",
        default_value= "empty:"
        )
    apprise_url4 = knext.StringParameter(
        label = "Apprise URL 4",
        description = "See here for details: https://github.com/caronc/apprise/wiki",
        default_value= "empty:"
        )
    apprise_url5 = knext.StringParameter(
        label = "Apprise URL 5",
        description = "See here for details: https://github.com/caronc/apprise/wiki",
        default_value= "empty:"
        )
    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")


    def configure(self, configure_context, input_schema_1):
        pass 

    def execute(self, exec_context, input_1):

        apobj = apprise.Apprise()

        urls = [self.apprise_url1, self.apprise_url2, self.apprise_url3, self.apprise_url4, self.apprise_url5]
        LOGGER.info(urls)
        for url in urls:
            if not (url.startswith("empty:")):
                LOGGER.info("Adding url " + url + " to Apprise...")
                apobj.add(url)

        apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        apobj.clear()

        return

@knext.node(name="Notify Table Rows", node_type=knext.NodeType.SINK, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
@knext.input_table(name="Input", description="The table containing the Apprise configuration data")
class AppriseNotifierTable1:
    """
    This node can be used to send out a series of notifications defined in a table. It expects a table with at least three columns, one containing the notification URL and the other two with the message titles and message bodies.
    This node can e.g. be used to notify the whole team about an issue with everyone receiving the notification on his or her preferred service.

    See Apprise documentation for more details regarding supported notification URLs: https://github.com/caronc/apprise#supported-notifications

    Icons for ParadigmChange Nodes and Apprise Nodes are taken from Freepik: https://www.freepik.com
    """

    apprise_configs = knext.ColumnParameter(
        label="Configurations",
        description="Select the column containing the Apprise configuration",
        port_index=0, # the port from which to source the input table
        include_row_key=False, # whether to include the table Row ID column in the list of selectable columns
        include_none_column=False # whether to enable None as a selectable option, which returns "<none>"
    )
    apprise_titles = knext.ColumnParameter(
        label="Titles",
        description="Select the column containing the titles of the messages to be sent",
        port_index=0, # the port from which to source the input table
        include_row_key=False, # whether to include the table Row ID column in the list of selectable columns
        include_none_column=False # whether to enable None as a selectable option, which returns "<none>"
    )
    apprise_bodies = knext.ColumnParameter(
        label="Body",
        description="Select the column containing the body of the messages to be sent",
        port_index=0, # the port from which to source the input table
        include_row_key=False, # whether to include the table Row ID column in the list of selectable columns
        include_none_column=False # whether to enable None as a selectable option, which returns "<none>"
    )

    def configure(self, configure_context, input_schema_1):
        pass 

    def execute(self, exec_context, input_1):

        input_1_pandas = input_1.to_pandas()

        configs_name = self.apprise_configs
        titles_name = self.apprise_titles
        bodies_name = self.apprise_bodies

        apobj = apprise.Apprise()

        for index, row in input_1_pandas.iterrows():
            if not (row[configs_name].startswith("empty:")):
                LOGGER.info("Sending notification to " + row[configs_name])
                apobj.add(row[configs_name])

                apobj.notify(
                    title=row[titles_name],
                    body=row[bodies_name]
                )

                apobj.clear()

        return

@knext.node(name="Notify Variable Config", node_type=knext.NodeType.SINK, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
@knext.input_table(name="Input Data", description="Input port from which the 'apprise_config' flow variable is read")
class AppriseNotifierVariable:
    """
    This node allows to send a simple single notification to services configured in a flow variable.
    See Apprise documentation for more details regarding supported notification URLs: https://github.com/caronc/apprise#supported-notifications

    Icons for ParadigmChange Nodes and Apprise Nodes are taken from Freepik: https://www.freepik.com
    """

    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")

    def configure(self, configure_context, input_schema_1):
        pass 

    def execute(self, exec_context, input_1):

        apobj = apprise.Apprise()

        try:
            config = exec_context.flow_variables["apprise_config"]
        except:
            raise ValueError("FlowVariable 'apprise_config' could not be found")

        if not (config.find("\n")):
            raise ValueError("Configuration FlowVariable should contain at least one newline (\n) character.")
        
        for line in config.split("\n"):
            LOGGER.info("Adding url" + line + "to Apprise...")
            apobj.add(line)

        apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        apobj.clear()

        return