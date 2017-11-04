from enum import Enum
import struct

# Read the size of an array
def read_array_size(stream):
  # Create a counter
  count = 1

  # Read the first byte
  size_bytes = stream.read(1)
  size = struct.unpack("<B",size_bytes)[0]
  
  # Create the total size
  total_size = size
  
  # While there are more bytes to read
  while size >> 7 == 1:
    # Increase the counter
    count += 1
  
    # Read the next byte
    size_bytes = stream.read(1)
    size = struct.unpack("<B",size_bytes)[0]

    # Add it to the total size
    total_size += (size & 0x7F) << (7 * count)
    
  # Return the total size
  return total_size


# FL event class
class FLEvent:

  # Constructor
  def __init__(self, type, content):
    self.type = type
    self.content = content
    
  # Convert to string
  def __str__(self):
    return str.format("{} of type {}",self.__class__.__name__,FLEventType(self.type).name)
    
  # Read an event from a stream
  @classmethod
  def read(cls, stream):
    # Read the event type
    type_bytes = stream.read(1)
    type = struct.unpack("<B",type_bytes)[0]
    
    # Get the base type
    basetype = type >> 6
    
    # Is it a BYTE event?
    if basetype == 0:
      # Read the next BYTE
      byte_bytes = stream.read(1)
      byte = struct.unpack("<B",byte_bytes)[0]
      
      # Return a new byte event instance
      return FLByteEvent(type,byte)
      
    # Is it a WORD event?
    elif basetype == 1:
      # Read the next WORD
      word_bytes = stream.read(2)
      word = struct.unpack("<H",word_bytes)[0]
      
      # Return a new word event instance
      return FLWordEvent(type,word)
      
    # Is it a DWORD event?
    elif basetype == 2:
      # Read the next DWORD
      dword_bytes = stream.read(4)
      dword = struct.unpack("<I",dword_bytes)[0]
      
      # Return a new dword event instance
      return FLDWordEvent(type,dword)
      
    # Is it an ARRAY event?
    elif basetype == 3:
      # Read the array size
      array_size = read_array_size(stream)
      
      # Read the array
      array = stream.read(array_size)
      
      # Return a new array event instance
      return FLArrayEvent(type,array)
      
    # If we execute the next line, someting went terriby wrong
    else:
      raise RuntimeError("Should not come here")
  
  
# FL BYTE event class
class FLByteEvent(FLEvent):

  # Constructor
  def __init__(self, type, content):
    FLEvent.__init__(self,type,content)
    
    
# FL WORD event class
class FLWordEvent(FLEvent):

  # Constructor
  def __init__(self, type, content):
    FLEvent.__init__(self,type,content)
    
    
# FL DWORD event class
class FLDWordEvent(FLEvent):

  # Constructor
  def __init__(self, type, content):
    FLEvent.__init__(self,type,content)

    
# FL ARRAY event class
class FLArrayEvent(FLEvent):

  # Constructor
  def __init__(self, type, content):
    FLEvent.__init__(self,type,content)
    
  # Return the content as a string
  def get_content_as_string(self):
    return self.content.decode()
    

# FL Event type enum
BYTE = 0 << 6
WORD = 1 << 6
DWORD = 2 << 6
ARRAY = 3 << 6

class FLEventType(Enum):
  # Byte events
  BYTE_CHAN_ENABLED = BYTE + 0
  BYTE_NOTE_ON = BYTE + 1 # +position
  BYTE_CHAN_VOL = BYTE + 2
  BYTE_CHAN_PAN = BYTE + 3
  BYTE_MIDI_CHAN = BYTE + 4
  BYTE_MIDI_NOTE = BYTE + 5
  BYTE_MIDI_PATCH = BYTE + 6
  BYTE_MIDI_BANK = BYTE + 7
  BYTE_LOOP_ACTIVE = BYTE + 9
  BYTE_SHOW_INFO = BYTE + 10
  BYTE_SHUFFLE = BYTE + 11
  BYTE_MAIN_VOL = BYTE + 12
  BYTE_FIT_TO_STEPS = BYTE + 13
  BYTE_PITCHABLE = BYTE + 14
  BYTE_ZIPPED = BYTE + 15
  BYTE_DELAY_FLAGS = BYTE + 16
  BYTE_TIME_SIG_NUM = BYTE + 17
  BYTE_TIME_SIG_BEAT = BYTE + 18
  BYTE_USE_LOOP_POBYTES = BYTE + 19
  BYTE_LOOP_TYPE = BYTE + 20
  BYTE_CHAN_TYPE = BYTE + 21
  BYTE_TARGET_FX_TRACK = BYTE + 22
  BYTE_PAN_VOL_TAB = BYTE + 23
  BYTE_N_STEPS_SHOWN = BYTE + 24
  BYTE_SS_LENGTH = BYTE + 25
  BYTE_SS_LOOP = BYTE + 26
  BYTE_FX_PROPS = BYTE + 27
  BYTE_REGISTERED = BYTE + 28
  BYTE_APDC = BYTE + 29
  BYTE_TRUNCATE_CLIP_NOTES = BYTE + 30
  BYTE_EE_AUTO_MODE = BYTE + 31
  
  # Word events
  WORD_NEW_CHAN = WORD + 0
  WORD_NEW_PAT = WORD + 1
  WORD_TEMPO = WORD + 2
  WORD_CURRENT_PAT_NUM = WORD + 3
  WORD_PAT_DATA = WORD + 4
  WORD_FX = WORD + 5
  WORD_FX_FLAGS = WORD + 6
  WORD_FX_CUT = WORD + 7
  WORD_DOT_VOL = WORD + 8
  WORD_DOT_PAN = WORD + 9
  WORD_FX_PREAMP = WORD + 10
  WORD_FX_DECAY = WORD + 11
  WORD_FX_ATTACK = WORD + 12
  WORD_DOT_NOTE = WORD + 13
  WORD_DOT_PITCH = WORD + 14
  WORD_DOT_MIX = WORD + 15
  WORD_MAIN_PITCH = WORD + 16
  WORD_RAND_CHAN = WORD + 17
  WORD_MIX_CHAN = WORD + 18
  WORD_FX_RES = WORD + 19
  WORD_OLD_SONG_LOOP_POS = WORD + 20
  WORD_FX_ST_DEL = WORD + 21
  WORD_FX3 = WORD + 22
  WORD_DOT_F_RES = WORD + 23
  WORD_DOT_F_CUT = WORD + 24
  WORD_SHIFT_TIME = WORD + 25
  WORD_LOOP_END_BAR = WORD + 26
  WORD_DOT = WORD + 27
  WORD_DOT_SHIFT = WORD + 28
  WORD_TEMPO_FINE = WORD + 29
  WORD_LAYER_CHAN = WORD + 30
  WORD_FX_ICON = WORD + 31
  WORD_DOT_REL = WORD + 32
  WORD_SWING_MIX = WORD + 33
  
  # Double word events
  DWORD_PLUGIN_COLOR = DWORD + 0
  DWORD_PL_ITEM = DWORD + 1 # Pos (word) +PatNum (word)
  DWORD_ECHO = DWORD + 2
  DWORD_FX_SINE = DWORD + 3
  DWORD_CUT_CUT_BY = DWORD + 4
  DWORD_WINDOW_H = DWORD + 5
  DWORD_MIDDLE_NOTE = DWORD + 7 
  DWORD_RESERVED = DWORD + 8
  DWORD_MAIN_RES_CUT = DWORD + 9
  DWORD_DELAY_F_RES = DWORD + 10
  DWORD_REVERB = DWORD + 11
  DWORD_STRETCH_TIME = DWORD + 12
  DWORD_SYMSYNTH_NOTE = DWORD + 13
  DWORD_FINE_TUNE = DWORD + 14
  DWORD_SAMPLE_FLAGS = DWORD + 15
  DWORD_LAYER_FLAGS = DWORD + 16
  DWORD_CHAN_FILTER_NUM = DWORD + 17
  DWORD_CURRENT_FILTER_NUM = DWORD + 18
  DWORD_FX_OUT_CHAN_NUM = DWORD + 19
  DWORD_NEW_TIME_MARKER = DWORD + 20
  DWORD_FX_COLOR = DWORD + 21
  DWORD_PAT_COLOR = DWORD + 22
  DWORD_PAT_AUTO_MODE = DWORD + 23
  DWORD_SONG_LOOP_POS = DWORD + 24
  DWORD_AU_SAMPLE_RATE = DWORD + 25
  DWORD_FX_IN_CHAN_NUM = DWORD + 26
  DWORD_PLUGIN_ICON = DWORD + 27
  DWORD_FINE_TEMPO = DWORD + 28
  
  # Array events
  ARRAY_CHAN_NAME = ARRAY + 0
  ARRAY_PAT_NAME = ARRAY + 1
  ARRAY_TITLE = ARRAY + 2
  ARRAY_COMMENT = ARRAY + 3
  ARRAY_SMP_FILE_NAME = ARRAY + 4
  ARRAY_URL = ARRAY + 5
  ARRAY_COMMENT_RTF = ARRAY + 6
  ARRAY_VERSION = ARRAY + 7
  ARRAY_REG_NAME = ARRAY + 8
  ARRAY_DEF_PLUGIN_NAME = ARRAY + 9
  ARRAY_PROJ_DATA_PATH = ARRAY + 10
  ARRAY_PLUGIN_NAME = ARRAY + 11 
  ARRAY_FX_NAME = ARRAY + 12
  ARRAY_TIME_MARKER = ARRAY + 13
  ARRAY_GENRE = ARRAY + 14
  ARRAY_AUTHOR = ARRAY + 15
  ARRAY_MIDI_CTRLS = ARRAY + 16
  ARRAY_DELAY = ARRAY + 17
  ARRAY_TS404_PARAMS = ARRAY + 18
  ARRAY_DELAY_LINE = ARRAY + 19
  ARRAY_NEW_PLUGIN = ARRAY + 20
  ARRAY_PLUGIN_PARAMS = ARRAY + 21
  ARRAY_RESERVED2 = ARRAY + 22
  ARRAY_CHAN_PARAMS = ARRAY + 23
  ARRAY_CTRL_REC_CHAN = ARRAY + 24
  ARRAY_PL_SEL = ARRAY + 25
  ARRAY_ENVELOPE = ARRAY + 26
  ARRAY_CHAN_LEVELS = ARRAY + 27
  ARRAY_CHAN_FILTER = ARRAY + 28
  ARRAY_CHAN_POLY = ARRAY + 29
  ARRAY_NOTE_REC_CHAN = ARRAY + 30
  ARRAY_PAT_CTRL_REC_CHAN = ARRAY + 31
  ARRAY_PAT_NOTE_REC_CHAN = ARRAY + 32
  ARRAY_INIT_CTRL_REC_CHAN = ARRAY + 33
  ARRAY_REMOTE_CTRL_MIDI = ARRAY + 34
  ARRAY_REMOTE_CTRL_INTERNAL = ARRAY + 35
  ARRAY_TRACKING = ARRAY + 36
  ARRAY_CHAN_OFS_LEVELS = ARRAY + 37
  ARRAY_ARRAY_REMOTE_CTRL_FORMULA = ARRAY + 38
  ARRAY_ARRAY_CHAN_FILTER = ARRAY + 39
  ARRAY_REG_BLACK_LIST = ARRAY + 40
  ARRAY_PL_REC_CHAN = ARRAY + 41
  ARRAY_CHAN_AC = ARRAY + 42
  ARRAY_FX_ROUTING = ARRAY + 43
  ARRAY_FX_PARAMS = ARRAY + 44
  ARRAY_PROJECT_TIME = ARRAY + 45
  ARRAY_PL_TRACK_INFO = ARRAY + 46
  ARRAY_ARRAY_PL_TRACK_NAME = ARRAY + 47
