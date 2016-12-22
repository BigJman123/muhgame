# A class to hold utility methods useful during game development, but
# not needed for normal game play.  Import the advent_devtools module
# to get the full version of the tools.
class DevToolsBase(object):
  def __init__(self):
    self.game = None

  def set_game(self, game):
    self.game = game
    
  def debug_output(self, text, level):
    return

  def start(self):
    return

global _devtools
_devtools = DevToolsBase()
  
def register_devtools(devtools):
  global _devtools
  _devtools = devtools