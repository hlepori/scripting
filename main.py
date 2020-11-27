import xmi_importer

def main():
  choice = '0'
  while choice == '0':
      print('\n')
      print("Menu: ")
      print("1. [XMI to EXCEL] Generating Excel file from xmi...")

      choice = input ("Please make a choice: ")

      if choice == "1":
        print('\n')
        print("[XMI to EXCEL] Generating Excel file from xmi...")
        xmiFileName = input ("Name of the xmi file to import? ")
        xmi_importer.import_xmi(xmiFileName)
        main()
      else:
        print("I don't understand your choice.")
        main()

main()

