import csv
import json
import os

def CSV_JSON():
   list=[]
   jsonlist=[]
   path = os.path.abspath(os.path.dirname(__file__))
   input=os.path.join(path, "Animal Detections\Animal Labels.csv")
   output=os.path.join(path, "Animal Detections\Animal_Labels.json")
   print (input)
   with open(input, mode ='r')as file:
      csvFile = csv.reader(file)
      # displaying the contents of the CSV file
      for lines in csvFile:
         list.append(lines)
   for i in range(1, len(list)):
      jsonlist.append({"file":list[i][1], "species":list[i][3], "confidence":list[i][2]})


   jsonfile={"images":jsonlist}
   with open(output, 'w')as f:
      json.dump(jsonfile, f)

CSV_JSON()