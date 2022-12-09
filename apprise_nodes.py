import logging
import apprise
import knime_extension as knext
import pandas as pd
LOGGER = logging.getLogger(__name__)

paradigmchange_nodes = knext.category(
        path="/community",
        level_id="paradigmchange_nodes",
        name="ParadigmChange Nodes",
        description="ParadigmChange Nodes for KNIME",
        icon="icons/exchange-64-freepik.png",
)

apprise_nodes = knext.category(
        path="/community/paradigmchange_nodes/",
        level_id="apprise_nodes",
        name="Apprise Nodes",
        description="Apprise Notifications for KNIME",
        icon="icons/megaphone-64-freepik.png",
)

@knext.node(name="Notify Single URL", node_type=knext.NodeType.OTHER, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
class AppriseNotifierSingle:
    """
# Send notification to a single service.

This is the most simple Node in the collection of the *Apprise Nodes*.
It can be used to send a simple notification to a single service URL. The connection to a workflow occurs through the (hidden) variable ports.

See [Apprise documentation](https://github.com/caronc/apprise#supported-notifications) for more details regarding supported notification URLs.

Icons for ParadigmChange Nodes and Apprise Nodes are taken from [Freepik](https://www.freepik.com)!
    """

    apprise_url = knext.StringParameter("Apprise URL", "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs", "pover://user@token/DEVICE")
    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")

    def configure(self, config_context):
        pass 

    def execute(self, exec_context):

        apobj = apprise.Apprise()

        LOGGER.info("Adding url \"" + self.apprise_url + "\" to Apprise...")

        config_result = apobj.add(self.apprise_url)

        if not config_result:
            raise ValueError("URL \"" + self.apprise_url + "\" could not be added to Apprise!")

        push_result = apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        match push_result:
            case None:
                raise RuntimeError("Notification could not be sent!")
            case False:
                LOGGER.error("Notification could not be sent!")
                exec_context.set_warning("Notification could not be sent!")

        apobj.clear()

        return

@knext.node(name="Notify Multiple URLs", node_type=knext.NodeType.OTHER, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
class AppriseNotifierMultiple:
    """
# Send notification to a up to five services.

This is another rather simple Node in the collection of the *Apprise Nodes*.
It can be used to send a simple notification to *up to five* service URLs. The connection to a workflow occurs through the (hidden) variable ports.
**Unused services should stay at "empty:", otherwise it is tried to add the content to Apprise and may raise errors!**

See [Apprise documentation](https://github.com/caronc/apprise#supported-notifications) for more details regarding supported notification URLs.

Icons for ParadigmChange Nodes and Apprise Nodes are taken from [Freepik](https://www.freepik.com)!
    """

    apprise_url1 = knext.StringParameter(
        label = "Apprise URL 1",
        description = "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs",
        default_value= "pover://user@token/DEVICE"
        )
    apprise_url2 = knext.StringParameter(
        label = "Apprise URL 2",
        description = "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs",
        default_value= "empty:"
        )
    apprise_url3 = knext.StringParameter(
        label = "Apprise URL 3",
        description = "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs",
        default_value= "empty:"
        )
    apprise_url4 = knext.StringParameter(
        label = "Apprise URL 4",
        description = "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs",
        default_value= "empty:"
        )
    apprise_url5 = knext.StringParameter(
        label = "Apprise URL 5",
        description = "See the [Apprise wiki](https://github.com/caronc/apprise/wiki) for a list of supported URLs",
        default_value= "empty:"
        )
    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")


    def configure(self, config_context):
        pass 

    def execute(self, exec_context):

        apobj = apprise.Apprise()

        urls = [self.apprise_url1, self.apprise_url2, self.apprise_url3, self.apprise_url4, self.apprise_url5]
        LOGGER.info(urls)
        all_ok = True
        for url in urls:
            if not (url.startswith("empty:")):
                LOGGER.info("Adding url \"" + url + "\" to Apprise...")

                config_result = apobj.add(url)

                if not config_result:
                    LOGGER.warn("URL \"" + url + "\" could not be added to Apprise!")
                    all_ok = False

        if not(all_ok):
            exec_context.set_warning("At least one URL could not bee added to Apprise")

        push_result = apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        match push_result:
            case None:
                raise RuntimeError("Notifications could not be sent at all!")
            case False:
                LOGGER.error("At least one notification could not be sent!")
                exec_context.set_warning("At least one notification could not be sent!")

        apobj.clear()

        return

@knext.node(name="Notify Table Rows", node_type=knext.NodeType.OTHER, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes)
@knext.input_table(name="Input", description="The table containing the Apprise configuration data")
class AppriseNotifierTable1:
    """
# Send notification to services defined in a KNIME table

This node can be used to send out a series of notifications defined in a table. It expects a table with at least three columns, one containing the notification URL and the other two with the message titles and message bodies.
A typical application could be to notify the whole team about an issue with everyone receiving the notification on his or her preferred service.

See [Apprise documentation](https://github.com/caronc/apprise#supported-notifications) for more details regarding supported notification URLs.

Icons for ParadigmChange Nodes and Apprise Nodes are taken from [Freepik](https://www.freepik.com)!
    """

    apprise_configs = knext.ColumnParameter(
        label="Configurations",
        description="Select the column containing the Apprise configuration",
    )
    apprise_titles = knext.ColumnParameter(
        label="Titles",
        description="Select the column containing the titles of the messages to be sent",
    )
    apprise_bodies = knext.ColumnParameter(
        label="Body",
        description="Select the column containing the body of the messages to be sent",
    )

    def configure(self, config_context, input_schema_1):
        pass 

    def execute(self, exec_context, input_1):

        input_1_pandas = input_1.to_pandas()

        configs_name = self.apprise_configs
        titles_name = self.apprise_titles
        bodies_name = self.apprise_bodies

        apobj = apprise.Apprise()

        all_config_ok = True
        all_push_ok = True
        for index, row in input_1_pandas.iterrows():
            if not (row[configs_name].startswith("empty:")):
                LOGGER.info("Sending notification to " + row[configs_name])

                config_result = apobj.add(row[configs_name])

                if not config_result:
                    LOGGER.warn("Error in row " + index + " - URL \"" + row[configs_name] + "\" could not be added to Apprise!")
                    all_config_ok = False

                push_result = apobj.notify(
                    title=row[titles_name],
                    body=row[bodies_name]
                )

                match push_result:
                    case None:
                        all_push_ok = False
                        LOGGER.warn("Error in row " + index + " Notification could not be sent!")
                        exec_context.set_warning("Error in row " + index + " Notification could not be sent!")
                    case False:
                        all_push_ok = False
                        LOGGER.error("Error in row " + index + " Notification could not be sent!")
                        exec_context.set_warning("Error in row " + index + " Notification could not be sent!")

                apobj.clear()

        if not(all_config_ok & all_push_ok):
            exec_context.set_warning("At least one row produced an error - see log for details!")

        return

@knext.node(name="Notify Variable Config", node_type=knext.NodeType.OTHER, icon_path="icons/megaphone-64-freepik.png", category=apprise_nodes, is_deprecated=True)
class AppriseNotifierVariable:
    """
# Send single notification to serivices configured in a flow variable

This node allows to send a simple single notification to services configured in a flow variable.
See [Apprise documentation](https://github.com/caronc/apprise#supported-notifications) for more details regarding supported notification URLs.

**This node is deprecated as all of it's functionality can be achieved with one of the other nodes as well!**

Icons for ParadigmChange Nodes and Apprise Nodes are taken from [Freepik](https://www.freepik.com)!
    """

    apprise_title = knext.StringParameter("Apprise Title", "The title of the message to be sent", "FooBar")
    apprise_body = knext.StringParameter("Apprise Message", "The message to be sent", "FooBar")

    def configure(self, config_context):
        try:
            config = config_context.flow_variables["apprise_config"]
        except:
            raise ValueError("FlowVariable 'apprise_config' could not be found")

    def execute(self, exec_context):

        apobj = apprise.Apprise()

        try:
            config = exec_context.flow_variables["apprise_config"]
        except:
            raise ValueError("FlowVariable 'apprise_config' could not be found")

        all_config_ok = True
        for line in config.split("\n"):
            LOGGER.info("Adding url \"" + line + "\" to Apprise...")
            config_result = apobj.add(line)

            if not config_result:
                LOGGER.warn("URL \"" + line + "\" could not be added to Apprise!")
                all_config_ok = False

        all_push_ok = True
        push_result = apobj.notify(
            title=self.apprise_title,
            body=self.apprise_body
        )

        match push_result:
            case None:
                raise RuntimeError("Notifications could not be sent at all!")
            case False:
                LOGGER.error("At least one notification could not be sent!")
                exec_context.set_warning("At least one notification could not be sent!")

        if not(all_config_ok & all_push_ok):
            exec_context.set_warning("At least one service produced an error - see log for more details!")

        apobj.clear()

        return
