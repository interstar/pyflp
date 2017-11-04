from chunk import FLChunk
from event import FLEventType
import io

# FL project class
class FLProject:

  # Constructor
  def __init__(self, chunks):
    self.version = ""
    self.title = ""
    self.author = ""
    self.genre = ""
    self.comment = ""
  
    self.chunks = chunks
    
    # Handle all events
    for event in self.get_data_chunk().events:
      event.handle(self)
    
  # Return a chunk with a given type
  def get_chunk(self, type):
    # Iterate over the chunks
    for chunk in self.chunks:
      # If the types match, return it
      if chunk.type == type:
        return chunk
    else:
      raise Exception(str.format("No chunk with type {} was found",type))
    
  # Return the header chunk
  def get_header_chunk(self):
    return self.get_chunk("FLhd")
    
  # Return the data chunk
  def get_data_chunk(self):
    return self.get_chunk("FLdt")
    
  # Read a project from a stream
  @classmethod
  def read(cls, stream):
    # Create a list to store the chunks
    chunks = []
  
    # Get the size of the stream
    stream.seek(0,2)
    stream_size = stream.tell()
      
    # Read chunks as long as there are bytes available
    stream.seek(0,0)
    while stream.tell() < stream_size:
      # Read a new chunk
      chunk = FLChunk.read(stream)
      
      # Add it to the list
      chunks.append(chunk)
    
    # Return a new project instance
    return FLProject(chunks)

  # Open a file and read the project in it
  @classmethod
  def open(cls, file_name):
    # Open the file
    with io.BufferedReader(io.FileIO(file_name,"r")) as stream:
      # Read the project from the file stream
      return cls.read(stream)
