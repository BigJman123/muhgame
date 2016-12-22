# A "connection" connects point A to point B. Connections are
# always described from the point of view of point A.
class Connection(Lockable):
  # name
  # point_a
  # point_b

  def __init__(self, name, pa, pb, way_ab, way_ba=None):
    Lockable.__init__(self, name)
    # way_ba defaults to the opposite of way_ab
    if way_ba is None:
        way_ba = ([opposite_direction(way) for way in way_ab]
                  if isinstance(way_ab, (list, tuple))
                  else opposite_direction(way_ab))
    self.point_a = pa
    self.point_b = pb
    self.way_ab = way_ab
    self.way_ba = way_ba