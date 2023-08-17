import json

################################################################Edit Here!!!

InputPath=r"C:\path\to\the\JSON_file\from\megadetector\results"
OutputPath=r"C:\Select\the\output\filepath\for\the\program"

################################################################

#filter the images with highest conf or conf >10%
new_images_list=[]
with open(InputPath, "r") as f:
	data=json.load(f)
images=data["images"]
count=1
try:
    for i in images:
        CurrentImages=[]
        highest_conf=0
        highest_cof_image={}
        
        try:
            if i["detections"]!=[]:
                for j in i["detections"]:
                    if(j["conf"]>0.1):
                        CurrentImages.append(j)
                    elif(j["conf"]>highest_conf):
                        highest_conf=j["conf"]
                        highest_cof_image=j
                if CurrentImages==[]:
                    CurrentImages.append(highest_cof_image)
                new_images_list.append({"file":i["file"],"detections":CurrentImages})
                count+=1
            else: new_images_list.append({"file":i["file"],"detections":[]})
        except: continue
except: (print(images[count]))

Output={"images":new_images_list, "detection_categories": data["detection_categories"],
 "info": data["info"]
}

#write output file
with open(OutputPath, "w") as f:
     json.dump(Output, f, indent=1)