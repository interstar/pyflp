import struct

# FL chunk class
class FLChunk:

  # Constructor
  def __init__(self, type):
    self.type = type
    
  # Convert to string
  def __str__(self):
    return self.__class__.__name__
    
  # Read a chunk from a file
  @classmethod
  def read(cls, file):
    # Read the chunk type
    type_bytes = file.read(4)
    type = type_bytes.decode()
    
    # Read the chunk length
    size_bytes = file.read(4)
    size = struct.unpack("<I",size_bytes)[0]
    
    # Read the content
    content = file.read(size)
    
    # Parse the chunk if applicable
    if type == "FLhd":
      return FLHeaderChunk.parse(content)
    elif type == "FLdt":
      return FLDataChunk.parse(content)
    else:
      return FLChunk(type)
      
 # FL header chunk class
class FLHeaderChunk(FLChunk):

  # Constructor
  def __init__(self, format, channel_count, beat_division):
    FLChunk.__init__(self,"FLhd")
    self.format = format
    self.channel_count = channel_count
    self.beat_division = beat_division
    
  # Convert to string
  def __str__(self):
    return str.format("{} with format = {}, channel count = {}, beat division = {}",self.__class__.__name__,self.format,self.channel_count,self.beat_division)

  # Parse the content of the chunk
  @classmethod
  def parse(cls, bytes):
    # Apply the header information
    header = struct.unpack("<HHH",bytes)
    format = header[0]
    channel_count = header[1]
    beat_division = header[2]
    
    # Return a new instance
    return FLHeaderChunk(format,channel_count,beat_division)
    
# FL data chunk class
class FLDataChunk(FLChunk):

  # Constructor
  def __init__(self, events):
    FLChunk.__init__(self,"FLdt")
    self.events = events
    
  # Convert to string
  def __str__(self):
    return str.format("{} with {} events",self.__class__.__name__,len(self.events))

  # Parse the content of the chunk
  @classmethod
  def parse(cls, bytes):
    return FLDataChunk([])

