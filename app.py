import os
import re
import csv

to_find = "FourKitesCommon::Logger."
target = "/Users/rohit.rathore/Desktop/Log Script/target"
result = []
count = 0
for root, dirs, files in os.walk(target):
    for filename in files:
        path = root+"/"+filename
        relative_path = os.path.relpath(path, target)
        try:
            with open(path) as df:
                for line in df:
                    if re.match(to_find,line.strip()):
                        count += 1
                        log_detail = re.search("\"(.*?)\"", line).group(1) if (re.search("\"(.*?)\"", line) != None) else "" # in between ""
                        if(log_detail == ""):
                            log_detail = re.search("\'(.*?)\'", line).group(1) if (re.search("\'(.*?)\'", line) != None) else "" # in between ''
                        log_type_string = to_find+"(.*?)\("
                        log_type = re.search(log_type_string, line).group(1) # get log type before () and after Logger.
                        result.append({"Path":relative_path,"Log Type":log_type,"Log Message":log_detail,"Characters":len(log_detail)})
        except:
            print("ERROR GETTING FILE CONTENTS")

field_names = ["Path","Log Type","Log Message","Characters"]
with open('Log_Details.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(result)

# import os
# import fnmatch
# import re


# def search_files(directory, keyword):
#     count = 0
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if fnmatch.fnmatch(file, '*.*'):
#                 # with open(os.path.join(root, file), "r") as f: # ye sirf UTF-8 encoded ke liye
#                 # error = 'ignore' -> utf-8 ko ignore karne ke liye
#                 with open(os.path.join(root, file), "r", encoding="utf-8", errors='ignore') as f:
#                     contents = f.read()
#                     matches = re.findall(keyword, contents)
#                     if matches:
#                         count += len(matches)
#                         print(f"{file} in {root} has {len(matches)} occurrences")
#     print(f"{count} occurrences found in total.")

# search_files("/Users/rohit.rathore/Desktop/Log Script/target", "FourKitesCommon::Logger.")