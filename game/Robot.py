# Robots are actors which accept commands to perform actions.
# They can also record and run scripts.
class Robot(Actor):
  def __init__(self, name):
    #super(Robot, self).__init__(name )
    Actor.__init__(self, name)
    self.name = name
    self.scripts = {}
    self.current_script = None
    self.script_think_time = 0
    self.add_verb(BaseVerb(self.act_start_recording, 'record'))
    self.add_verb(BaseVerb(self.act_run_script, 'run'))
    self.add_verb(BaseVerb(self.act_check_script, 'check'))
    self.add_verb(BaseVerb(self.act_print_script, 'print'))
    self.add_verb(BaseVerb(self.act_save_file, 'save'))
    self.add_verb(BaseVerb(self.act_load_file, 'load'))
    self.add_verb(BaseVerb(self.set_think_time, 'think'))
    self.add_verb(BaseVerb(self.toggle_verbosity, 'verbose'))
    self.leader = None
    self.add_verb(BaseVerb(self.act_follow, 'heel'))
    self.add_verb(BaseVerb(self.act_follow, 'follow'))
    self.add_verb(BaseVerb(self.act_stay, 'stay'))

  def act_follow(self, actor, noun, words=None):
    if noun == None or noun == "" or noun == "me":
      self.leader = self.game.player
    elif noun in self.game.robots:
      self.leader = self.game.robots[noun]
    elif noun in self.game.animals:
      self.leader = self.game.animals[noun]
    self.output("%s obediently begins following %s" % \
                (self.name, self.leader.name) , FEEDBACK)
    return True

  def act_stay(self, actor, noun, words=None):
    if self.leader:
      self.output("%s obediently stops following %s" % \
                  (self.name, self.leader.name) , FEEDBACK)
    self.leader = None
    return True

  def toggle_verbosity(self, actor, noun, words):
    if self.flag('verbose'):
      self.unset_flag('verbose')
      self.output("minimal verbosity")
    else:
      self.set_flag('verbose')
      self.output("maximum verbosity")
    return True

  def parse_script_name(self, noun):
    if not noun:
        script_name = "default"
    else:
        script_name = noun
    return script_name

  def act_start_recording(self, actor, noun, words):
    script_name = self.parse_script_name(noun)
    self.set_flag('verbose')
    self.game.devtools.debug_output("start recording %s" % script_name, 2)
    script = Script(script_name, None, self.game)
    self.scripts[script_name] = script
    script.start_recording()
    self.current_script = script
    return True

  def act_run_script(self, actor, noun, words):
    if self.current_script:
      print "You must stop \"%s\" first." % (self.current_script.name)
    script_name = self.parse_script_name(noun)
    if not script_name in self.scripts:
      print "%s can't find script \"%s\" in its memory." % (self.name,
                                                            script_name)

      return True;
    
    self.game.devtools.debug_output("start running %s" % script_name, 2)
    script = self.scripts[script_name]
    self.current_script = script
    script.start_running()
    return True

  def act_check_script(self, actor, noun, words):
    if self.act_run_script(actor, noun, words):
      self.set_flag('verbose')
      self.current_script.start_checking()
      self.game.devtools.debug_output("start checking", 2)
      return True
    return False
  
  def act_print_script(self, actor, noun, words):
    script_name = self.parse_script_name(noun)
    if not script_name in self.scripts:
      print "%s can't find script \"%s\" in its memory." % (self.name,
                                                              script_name)
      return True

    print "----------------------8<-------------------------\n"
    print "# Paste the following into your game code in order"
    print "# to be able to run this script in the game:"
    print "%s_script = Script(\"%s\"," % (script_name, script_name)
    print "\"\"\""
    self.scripts[script_name].print_script()
    print "\"\"\")"
    print "\n# Then add the script to a player, or a robot"
    print "# with code like the following:"
    print "player.add_script(%s_script)" % script_name
    print "\n# Now you can run the script from within the game"
    print "# by typing \"run %s\"" % script_name
    print "\n---------------------->8-------------------------"
    return True

  def act_save_file(self, actor, noun, words):
    script_name = self.parse_script_name(noun)
    if not script_name in self.scripts:
      print "%s can't find script \"%s\" in its memory." % (self.name,
                                                            script_name)
      return True
    self.scripts[script_name].save_file()
    return True

  def act_load_file(self, actor, noun, words):
    script_name = self.parse_script_name(noun)
    self.scripts[script_name] = Script(script_name, None, self.game)
    self.scripts[script_name].load_file()
    return True

  def add_script(self, script):
    script.game = self.game
    self.scripts[script.name] = script    
  
  def set_think_time(self, actor, noun, words):
    if noun:
      t = float(noun)
      if t >= 0 and t <= 60:
          self.script_think_time = t
          return True

    print "\"think\" requires a number of seconds (0.0000-60.0000) as an argument"
    return True

  def get_next_script_command(self):
    if not self.current_script or not self.current_script.running:
      return None
    line = self.current_script.get_next_command()
    if not line:
      print "%s %s done running script \"%s\"." % (self.name,
                                                   self.isare,
                                                   self.current_script.name)
      self.current_script = None
      return None
    if self.script_think_time > 0:
      time.sleep(self.script_think_time)
    line = self.name + ": " + line
    print "> %s" % line
    return line

  def set_next_script_command(self, command):
    if not self.current_script:
      return True
    if not self.current_script.set_next_command(command):
      print "%s finished recording script \"%s\"." % (self.name,
                                                      self.current_script.name)
      self.current_script = None
      return False
    return True

  def set_next_script_response(self, response):
    if not self.current_script:
      return True
    self.current_script.set_next_response(response)
    return True