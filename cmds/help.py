import updateabot
import glob

HELP = "I display available cmds and any 'HELP' variables that are defined by the cmd. "


def run(query):
    message = ""
    cmds = [cmd[:-3].split('/')[-1] for cmd in glob.glob(updateabot.CMDS_DIR + '/*.py') if cmd[-11:] != '__init__.py']
    if query:
        cmds = [cmd for cmd in cmds if cmd == query]
    if cmds == []:
        message = "No commands found! :("
        if query:
            message += " (for filter '%s')" % (query)
        return message
    cmds.sort()
    for cmdstr in cmds:
        cmd = __import__('cmds.%s' % (cmdstr), fromlist=[''])
        message += "?%s" % (cmdstr)
        if hasattr(cmd, 'HELP'):
            message += " - %s" % (cmd.HELP)
        else:
            message += " - No HELP for you!"
        message += "\n"
    return message
