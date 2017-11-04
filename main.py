from project import FLProject

# Main function
def main():
  # Open an FLP
  project = FLProject.open("examples/tetris.flp")
  
  # Print some basic info
  print("Format:",project.get_format())
  print("Channel count:",project.get_channel_count())
  print("Beat division:",project.get_beat_division())
  print("Version:",project.get_version())
  print("Title:",project.get_title())
  print("Author:",project.get_author())
  print("Genre:",project.get_genre())
  print("Comment:",project.get_comment())
  
# Execute the main function if not imported
if __name__ == "__main__":
  main()