# Read the size of a text event
def read_text_size(stream):
  # Create a counter
  count = 1

  # Read the first byte
  size_bytes = stream.read(1)
  size = int.from_bytes(size_bytes,byteorder="little")
  
  # Create the total size
  total_size = size
  
  # While there are more bytes to read
  while size >> 7 == 1:
    # Increase the counter
    count += 1
  
    # Read the next byte
    size_bytes = stream.read(1)
    size = int.from_bytes(size_bytes,byteorder="little")

    # Add it to the total size
    total_size += (size & 0x7F) << (7 * count)
    
  # Return the total size
  return total_size
