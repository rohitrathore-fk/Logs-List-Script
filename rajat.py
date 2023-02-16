# import os
# import re
# import csv

# #VARIABLES
# to_find = "FourKitesCommon::Logger."
# target = "/Users/rohit.rathore/Desktop/Log Script/target/tests/"
# result = []
# words = []
# freq = {}
# freq_list = []
# log_codes = {}
# next_line = False

# #FUNCTIONS
# def get_logs():
#     global next_line
#     for root, dirs, files in os.walk(target):
#         for filename in files:
#             path = root+"/"+filename
#             relative_path = os.path.relpath(path, target)
#             try:
#                 with open(path) as df:
#                     for line in df:
#                         if re.match(to_find,line.strip()) or next_line:
#                             first_index = line.find('.')
#                             result.append("func_"+line[first_index+1,])

#                             # result.append({"Path":relative_path,"Log Type":log_type,"Log Message":log_detail,"Characters":len(log_detail)})
#             except:
#                 print("ERROR GETTING FILE CONTENTS")

# # def create_log_codes(result):
# #     global log_codes
# #     log_types = {"error":["err",0],"info":["info",0],"debug":["dbg",0],"warn":["wn",0]}
# #     for log in result:
# #         if log["Log Message"] not in log_codes:
# #             log_types[log["Log Type"]][1] += 1
# #             log_codes[log["Log Message"]] = log_types[log["Log Type"]][0] + str(log_types[log["Log Type"]][1])
# #     print(log_codes)

# def create_py_file():
#     global result
#     with open('Full_logs.py', 'w') as pyfile:
#         for log in result:
#             print(log)
#             pyfile.write(log + "\n")

# #MAIN
# if __name__ == "__main__":
#     create_py_file()
    
import os
import fnmatch
import re
import csv

def search_files(directory, keyword):
    count = 0
    data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, '*.*'):
                with open(os.path.join(root, file), "r", encoding="utf-8", errors='ignore') as f:
                    contents = f.read()
                    matches = re.finditer(keyword + r'(error|warn|debug|info)\((.*?\n?.*?)\)\s?\n', contents, re.M)
                    if matches:
                        for match in matches:
                            count += 1
                            data.append({"File": file,"Path": root,"Matched String" :match.group(),
                                        "String inside": match.groups()[1], "Type" : match.groups()[0]})
    columns=['File', 'Path', 'Matched String','String inside',"Type"]
    with open('Log_Details.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)
    with open('Full_logs.py', 'a') as pyfile:
        for log in data:
            func_call = "func_" + log["Type"] + "(" + log["String inside"] + ")"
            pyfile.write(func_call+"\n")
    print(f"{count} occurrences found in total.")


search_files("/Users/rohit.rathore/Desktop/Log Script/target/tracking-service","FourKitesCommon::Logger.")