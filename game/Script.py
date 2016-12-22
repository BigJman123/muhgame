# Scripts are sequences of instructions for Robots to execute
class Script(Base):
  def __init__(self, name, lines=None, game=None):
    Base.__init__(self, name)
    self.game = game
    self.commands = list()
    self.responses = list()
    self.current_response = None
    self.check_responses = False
    self.mismatched_responses = -1
    self.current_command = -1
    self.recording = False
    self.running = False
    self.start_time = None
    self.finish_time = None
    self.response_errors = 0
    self.parse_lines(lines)

  def parse_lines(self, lines):
    if lines != None:
      self.start_recording()
      for line in lines.split("\n"):
        if line.startswith("> "):
          # save the new command, and any accumulated response from previous
          self.set_next_command(line.strip("> \n"))
        elif self.current_response != None:
          # accumulate response lines until the next command
          self.current_response += line + "\n"
        else:
          self.current_response = line + "\n"
      # if we didn't manage to get "end" go ahead and stop things brute force
      if self.recording:
        self.stop_recording()
    
  def start_recording(self):
    assert not self.running
    assert not self.recording
    self.current_response = None
    self.responses = list()
    self.commands = list()
    self.recording = True

  def stop_recording(self):
    assert self.recording
    assert not self.running
    self.current_response = None
    self.recording = False

  def start_running(self):
    assert not self.running
    assert not self.recording
    self.current_response = None
    self.check_responses = False
    self.running = True
    self.current_command = 0
    self.mismatched_responses = 0
    self.start_time = time.time()

  def start_checking(self):
    assert self.running
    assert not self.recording
    print "check_responses on"
    self.check_responses = True
    self.current_response = ""

  def stop_running(self):
    assert self.running
    assert not self.recording
    self.stop_time = time.time()
    self.game.devtools.debug_output(
      "script \"%s\":\n\tcommands: %d\n\tmismatched responses: %d\n\truntime: %f %s\n" % (
        self.name, self.current_command, self.mismatched_responses,
        (self.stop_time - self.start_time) * 1000, "milliseconds"), 0)
    self.current_response = None
    self.check_responses = False
    self.running = False
    self.current_command = -1
    if self.mismatched_responses != 0:
      assert(not self.game.flag('fail_on_mismatch'))

  def get_next_command(self):
    # if we're running a checker, examine the current response vs what's expected
    if self.current_command >= 1:
      self.check_response_match(self.current_response,
                                self.responses[self.current_command - 1])
      self.current_response = ""

    if not self.commands:
      return None
      
    while True:
      line = self.commands[self.current_command].strip()
      self.current_command += 1
      # support comments and/or blank lines within the script
      line = line.split("#")[0]
      if line != "":
        break 
    if line == "end":
      self.stop_running()
      return None
    return line

  def check_response_match(self, response, expected_response):
    if self.check_responses:
      match = "match"
      level = 2
      if response != expected_response:
        match = "mismatch"
        level = 0
        self.mismatched_responses += 1

      self.game.devtools.debug_output(
        "response %s:\n>>>\n%s\n===\n%s\n<<<\n" % (match,
                                                   response,
                                                   expected_response),
        level)
      
  
  def set_next_command(self, command):
    if not self.recording:
      return True
    
    # save the accumulated response from the previous command
    if self.current_response != None:
      # append the response, trimming the final newline that preceded this command
      self.responses.append(self.current_response[:-1])
    self.current_response = ""

    # save the current command
    self.commands.append(command)
    if command.strip() == "end":
      self.stop_recording()
      return False
    self.current_command += 1
      
    return True

  def set_next_response(self, response):
    if self.current_response != None:
      # strip out color changing chars which may be in there
      control_chars = False
      for c in response:
        if c == '\33':
          control_chars = True
        if control_chars:
          if c == 'm':
            control_chars = False
          continue
        self.current_response += c
      self.current_response += "\n"
      
  def print_script(self):
    i = 0
    for command in self.commands:
      print "> " + command
      if command == "end":
        break
      print self.responses[i]
      i = i + 1

  def save_file(self):
    f = open(self.name + ".script", "w")
    i = 0
    for command in self.commands:
      f.write('> ' + command + '\n')
      if command != "end":
        response_lines = self.responses[i].split('\n')
        for line in response_lines:
          f.write(line + '\n')
      i = i + 1
    f.close()

  def load_file(self):
    f = open(self.name + ".script", "r")
    self.parse_lines(f.read())
    f.close()