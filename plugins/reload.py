import importlib
import sys
import logging

from command import command

log = logging.getLogger(__name__)


@command("reload", owner_only=True)
async def reload_plugin(bot, sender_jid, nick, args, msg, is_room):
    """
    Reload a plugin without restarting the bot.

    Usage:
        reload <plugin>
        reload all

    Arguments:
        plugin   Name of the plugin module in the plugins directory.
        all      Reload all currently loaded plugins.

    Examples:
        ,reload help
        ,reload all
    """

    if not args:
        bot.reply(msg, "Usage: reload <plugin|all>")
        return

    target = args[0]

    # Reload all plugins
    if target == "all":
        count = 0
        for module_name in list(sys.modules):
            if not module_name.startswith("plugins."):
                continue
            try:
                module = sys.modules[module_name]
                # remove commands belonging to this module
                to_remove = [
                    name for name, func in bot.commands.items()
                    if func.__module__ == module_name
                ]
                for name in to_remove:
                    del bot.commands[name]
                importlib.reload(module)
                # re-register commands
                for attr in vars(module).values():
                    if callable(attr) and hasattr(attr, "_command_names"):
                        for name in attr._command_names:
                            bot.commands[name] = attr
                count += 1
            except Exception:
                log.exception(f"Failed to reload {module_name}")

        bot.reply(msg, f"🔄 Reloaded {count} plugins.")
        log.info(f"🔄 Reload all: {count} plugins.")
        return

    module_path = f"plugins.{target}"

    if module_path not in sys.modules:
        bot.reply(msg, f"❌ Plugin '{target}' is not loaded.")
        return

    try:
        module = sys.modules[module_path]
        # remove existing commands from this plugin
        to_remove = [
            name for name, func in bot.commands.items()
            if func.__module__ == module_path
        ]
        for name in to_remove:
            del bot.commands[name]
        # reload module
        importlib.reload(module)
        # re-register commands
        for attr in vars(module).values():
            if callable(attr) and hasattr(attr, "_command_names"):
                for name in attr._command_names:
                    bot.commands[name] = attr
        bot.reply(msg, f"🔄 Plugin '{target}' reloaded.")
        log.info(f"🔄 Plugin '{target}' reloaded.")
    except Exception:
        log.exception(f"Failed to reload plugin {target}")
        bot.reply(msg, f"❌ Failed to reload '{target}'. Check logs.")
