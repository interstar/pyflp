from FLChunk import FLChunk

# FL project class
class FLProject:

  # Constructor
  def __init__(self, chunks):
    self.chunks = chunks
    
  # Read a project from a file
  @classmethod
  def read(cls, file):
    # Create a list to store the chunks
    chunks = []
  
    # Get the size of the file
    file.seek(0,2)
    file_size = file.tell()
      
    # Read chunks as long as there are bytes available
    file.seek(0,0)
    while file.tell() < file_size:
      # Read a new chunk
      chunk = FLChunk.read(file)
      
      # Add it to the list
      chunks.append(chunk)
    
    # Create a new project instance
    return FLProject(chunks)
