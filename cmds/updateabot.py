import os
import git

CMDS_DIR = os.path.dirname(os.path.abspath(__file__))
ABOT_DIR = os.path.dirname(CMDS_DIR)


def run(query):
    os.system('pip install -r %s/requirements.txt' % ABOT_DIR)
    repo = git.Repo(ABOT_DIR)
    repo.remotes.origin.pull()
    return "I have updated myself!"
