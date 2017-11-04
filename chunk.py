from io import BytesIO, BufferedReader
from event import FLEvent, FLEventType
import struct

# FL chunk class
class FLChunk:

  # Constructor
  def __init__(self, type):
    self.type = type
    
  # Convert to string
  def __str__(self):
    return self.__class__.__name__
    
  # Read a chunk from a stream
  @classmethod
  def read(cls, stream):
    # Read the chunk type
    type_bytes = stream.read(4)
    type = type_bytes.decode()
    
    # Read the chunk length
    size_bytes = stream.read(4)
    size = struct.unpack("<I",size_bytes)[0]
    
    # Read the content
    content = stream.read(size)
    
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

  # Parse the content of the chunk
  @classmethod
  def parse(cls, bytes):
    # Apply the header information
    header = struct.unpack("<HHH",bytes)
    format = header[0]
    channel_count = header[1]
    beat_division = header[2]
    
    # Return a new header chunk instance
    return FLHeaderChunk(format,channel_count,beat_division)
    
    
# FL data chunk class
class FLDataChunk(FLChunk):

  # Constructor
  def __init__(self, events):
    FLChunk.__init__(self,"FLdt")
    self.events = events
    
  # Return an event of a given type
  def get_event_by_type(self, type):
    # Check if it is the enum
    if isinstance(type,FLEventType):
      type = type.value

    # Iterate over the events
    for event in self.events:
      # If the types match, return it
      if event.type == type:
        return event
    else:
      raise Exception(str.format("No event with type {} was found",type))

  # Parse the content of the chunk
  @classmethod
  def parse(cls, bytes):
    # Create a list to store the events
    events = []
    
    # Create a new stream from the chunk contents
    stream = BufferedReader(BytesIO(bytes))
    
    # Get the size of the stream
    stream.seek(0,2)
    stream_size = stream.tell()
      
    # Read events as long as there are bytes available
    stream.seek(0,0)
    while stream.tell() < stream_size:
      # Read a new event
      event = FLEvent.read(stream)
      
      # Add it to the list
      events.append(event)
  
    # Return a new data chunk instance
    return FLDataChunk(events)

