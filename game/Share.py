class Share(object):
  def __init__(self):
    self.hostname = None
    self.port = None
    self.username = None
    self.password = None
    self.GLOBAL = 1
    self.ADVENTURE = 2
    self.PLAYER = 3
    self.SESSION = 4
    self.game = ""
    self.player = ""
    self.session = ""
    self.key_fns = {
        self.GLOBAL: self.global_key,
        self.ADVENTURE: self.adventure_key,
        self.PLAYER: self.player_key,
        self.SESSION: self.session_key,
    }
    try:
      f = open("share.info", "r")
      self.hostname = f.readline().strip()
      self.port = f.readline().strip()
      self.username = f.readline().strip()
      self.password = f.readline().strip()
    except IOError:
      pass

  def set_host(self, hostname, port, username, password):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password

  def set_adventure(self, adventure):
    self.adventure = adventure

  def set_player(self, player):
    self.player = player

  def set_session(self, session):
    self.session = session

  def is_available(self):
    return self.hostname != None

  def start(self):
    if not self.is_available():
      return
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    webdis_url = "http://%s:%s/" % (self.hostname, self.port)
    password_mgr.add_password(None, webdis_url, self.username, self.password)
    self.opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(password_mgr))

  def global_key(self, key):
    return 'g.' + key

  def adventure_key(self, key):
    return 'a.' + self.adventure + '.' + key

  def player_key(self, key):
    return 'p.' + self.adventure + '.' + self.player + '.' + key

  def session_key(self, key):
    return 's.' + self.adventure + '.' + self.player + '.' + self.session + key

  def _do(self, domain, cmd, key):
    assert(domain in self.key_fns)
    if not self.is_available():
      return None
    k = self.key_fns[domain](key)
    net_f = self.opener.open('http://%s:%s/%s/%s.raw' % (self.hostname, self.port, cmd, k))
    v = net_f.read().split('\n')
    if len(v) > 1:
       return v[1].strip()
    return None

  def _do1(self, domain, cmd, key, arg1):
    assert(domain in self.key_fns)
    if not self.is_available():
      return None
    k = self.key_fns[domain](key)
    net_f = self.opener.open('http://%s:%s/%s/%s/%s.raw' % (self.hostname, self.port, cmd, k, arg1))
    v = net_f.read().split('\n')
    if len(v) > 1:
       return v[1]  # should be ""
    return None

  def _do2(self, domain, cmd, key, arg1, arg2):
    assert(domain in self.key_fns)
    if not self.is_available():
      return None
    k = self.key_fns[domain](key)
    net_f = self.opener.open('http://%s:%s/%s/%s/%s/%s.raw' % (self.hostname, self.port, cmd, k, arg1, arg2))
    v = net_f.read().split('\n')
    if len(v) > 1:
       return v[1]  # should be ""
    return None

  # return a list
  def _do2l(self, domain, cmd, key, arg1, arg2):
    assert(domain in self.key_fns)
    if not self.is_available():
      return []
    k = self.key_fns[domain](key)
    net_f = self.opener.open('http://%s:%s/%s/%s/%s/%s.raw' % (self.hostname, self.port, cmd, k, arg1, arg2))
    v = net_f.read().split('\n')
    return v

  # return a list
  def _do3l(self, domain, cmd, key, arg1, arg2, arg3):
    assert(domain in self.key_fns)
    if not self.is_available():
      return []
    k = self.key_fns[domain](key)
    net_f = self.opener.open('http://%s:%s/%s/%s/%s/%s/%s.raw' % (self.hostname, self.port, cmd, k, arg1, arg2, arg3))
    v = net_f.read().split('\n')
    return v

  def delete(self, domain, key):
    return self._do(domain, "DEL", key)

  def get(self, domain, key):
    return self._do(domain, "GET", key)

  def put(self, domain, key, value):
    return self._do1(domain, "SET", key, value)

  def increment(self, domain, key):
    return self._do(domain, "INCR", key)

  def decrement(self, domain, key):
    return self._do(domain, "DECR", key)

  def push(self, domain, key, value):
    return self._do1(domain, "LPUSH", key, value)

  def pop(self, domain, key):
    return self._do(domain, "LPOP", key)

  def zadd(self, domain, key, value, score):
    return self._do2(domain, "ZADD", key, score, value)

  def zscore(self, domain, key):
    return self._do(domain, "ZSCORE", key, value)

  def zdelete_over_rank(self, domain, key, rank):
    return self._do2(domain, "ZREMRANGEBYRANK", key, rank, "-1")

  def ztop(self, domain, key, rank):
    v = self._do2l(domain, "ZREVRANGE", key, "0", rank)
    v = [x.strip() for x in v[1:]]
    result = []
    for x in xrange(0, len(v)):
      if x % 2 == 1:
        result.append(v[x])
    return result

  def ztop_with_scores(self, domain, key, rank):
    v = self._do3l(domain, "ZREVRANGE", key, "0", rank, "WITHSCORES")
    v = [x.strip() for x in v[1:]]
    result = []
    for x in xrange(0, len(v)):
      if x % 4 == 1:
        p = [v[x]]
      elif x % 4 == 3:
        p.append(v[x])
        result.append(p)
    return result

  def zdelete(self, domain, key, value):
    return self._do(domain, "ZREM", key, value)