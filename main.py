from FLProject import FLProject

# Main function
def main():
  # Open an FLP
  with open("examples/tetris.flp","rb") as file:
    project = FLProject.read(file)
    for chunk in project.chunks:
      print("- ",chunk)
  
# Execute the main function if not imported
if __name__ == "__main__":
  main()