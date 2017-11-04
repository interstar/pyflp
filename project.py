from io import FileIO
from chunk import FLChunk
from event import FLEventType

# FL project class
class FLProject:

  # Constructor
  def __init__(self, chunks):
    self.chunks = chunks
    
  # Return a chunk with a given type
  def get_chunk_by_type(self, type):
    # Iterate over the chunks
    for chunk in self.chunks:
      # If the types match, return it
      if chunk.type == type:
        return chunk
    else:
      raise Exception(str.format("No chunk with type {} was found",type))
    
  # Return the header chunk
  def get_header_chunk(self):
    return self.get_chunk_by_type("FLhd")
    
  # Return the data chunk
  def get_data_chunk(self):
    return self.get_chunk_by_type("FLdt")
    
  # Return the project format
  def get_format(self):
    return self.get_header_chunk().format
    
  # Return the project channel count
  def get_channel_count(self):
    return self.get_header_chunk().channel_count
    
  # Return the project beat division
  def get_beat_division(self):
    return self.get_header_chunk().beat_division
    
  # Return the version
  def get_version(self):
    return self.get_data_chunk().get_event_by_type(FLEventType.ARRAY_VERSION).get_content_as_string()
    
  # Return the title
  def get_title(self):
    return self.get_data_chunk().get_event_by_type(FLEventType.ARRAY_TITLE).get_content_as_string()
    
  # Return the author
  def get_author(self):
    return self.get_data_chunk().get_event_by_type(FLEventType.ARRAY_AUTHOR).get_content_as_string()
    
  # Return the genre
  def get_genre(self):
    return self.get_data_chunk().get_event_by_type(FLEventType.ARRAY_GENRE).get_content_as_string()
    
  # Return the comment
  def get_comment(self):
    return self.get_data_chunk().get_event_by_type(FLEventType.ARRAY_COMMENT).get_content_as_string()
    
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
    with FileIO(file_name,"r") as stream:
      # Read the project from the file stream
      return cls.read(stream)
