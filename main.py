from project import FLProject
from event import FLEvent

# Main function
def main():
  # Open an FLP
  project = FLProject.open("examples/empty.flp")
  
  # Print some basic info
  for event in project.get_data_chunk().events:
    if type(event) != FLEvent:
      print(event)
  
  print("Version:",project.version)
  print("Title:",project.title)
  print("Author:",project.author)
  print("Genre:",project.genre)
  print("Comment:",project.comment)
  
# Execute the main function if not imported
if __name__ == "__main__":
  main()