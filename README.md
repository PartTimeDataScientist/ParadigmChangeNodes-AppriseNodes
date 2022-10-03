This repository contains the *Apprise Nodes for KNIME* which are part of the *ParadigmChange Nodes for KNIME*

Did you ever wanted to get notified when certain things are happening in your KNIME workflow? Receive a high priority pushover notification when errors are occuring in a try-catch-block? Get notified via Telegram when your workflow is done? Automatically tweet about your latest results? **We've got you covered: Take a look at the Apprise Nodes** 

[Apprise](https://github.com/caronc/apprise) is one of the most versatile if not *the* most versatile notification tool / library as of today. Here's the self description from the repository:

> Apprise allows you to send a notification to almost all of the most popular notification services available to us today such as: Telegram, Discord, Slack, Amazon SNS, Gotify, etc.
>
>    * One notification library to rule them all.
>    * A common and intuitive notification syntax.
>    * Supports the handling of images and attachments (to >the notification services that will accept them).
>    * It's incredibly lightweight.
>    * Amazing response times because all messages sent asynchronously.
>
> Developers who wish to provide a notification service no longer need to research each and every one out there. They no longer need to try to adapt to the new ones that comeout thereafter. They just need to include this one library and then they can immediately gain access to almost all of the notifications services available to us today.
>
>System Administrators and DevOps who wish to send a notification now no longer need to find the right tool for the job. Everything is already wrapped and supported within the apprise command line tool (CLI) that ships with this product.

When I first discovered Apprise as notification library for the selfhosted [changedetection.io website monitor](https://github.com/dgtlmoon/changedetection.io) I immediatly thought about the possibilities that KNIME nodes using this library would bring but being a Python library they were not straightforward to integrate. With the ability to [develop Python based KNIME Nodes](https://docs.knime.com/latest/pure_python_node_extensions_guide/#introduction) introduced in KNIME 4.6 the situation changed and now here they are: The *Apprise Nodes*