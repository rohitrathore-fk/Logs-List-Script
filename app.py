import os
import re
import csv

#VARIABLES
# to_find = "FourKitesCommon::Logger." #FOR RUBY
to_find = "fk_logger." #FOR GO
target = "/Users/rohit.rathore/Desktop/Log Script/target" #WHERE THE REPO IS STORED
result = []
words = []
freq = {}
freq_list = []
log_codes = {}
next_line = False
count = 0

#FUNCTIONS
def get_logs():
    global next_line
    for root, dirs, files in os.walk(target):
        for filename in files:
            path = root+"/"+filename
            relative_path = os.path.relpath(path, target)
            try:
                with open(path) as df:
                    for line in df:
                        if re.match(to_find,line.strip()) or next_line:
                            # print(relative_path)
                            # first_index = line.find('"')
                            # last_index = line.rfind('"')
                            log_detail = re.search("\"(.*?)\"", line).group(1) if (re.search("\"(.*?)\"", line) != None) else ""
                            # if(first_index != -1 and last_index != -1):
                            #     log_detail = line[first_index+1:last_index]
                            if(log_detail == ""):
                                # first_index = line.find("'")
                                # last_index = line.rfind("'")
                                log_detail = re.search("\'(.*?)\'", line).group(1) if (re.search("\'(.*?)\'", line) != None) else ""
                                # if(first_index != -1 and last_index != -1):
                                #     log_detail = line[first_index+1:last_index]    
                            if next_line:
                                next_line = False
                                result[-1]["Log Message"] = log_detail
                                result[-1]["Characters"] = len(log_detail)
                                continue
                            #IF LOG DETAILS STILL EMPTY THEN NEXT LINE WILL HAVE DETAILS
                            if(log_detail == ""):
                                next_line = True
                            words.extend(log_detail.split())
                            log_type_string = to_find+"(.*?)\("
                            log_type = re.search(log_type_string, line).group(1)
                            result.append({"Path":relative_path,"Log Type":log_type,"Log Message":log_detail,"Characters":len(log_detail)})
            except Exception as e:
                print(e)

def create_log_codes(result):
    global log_codes
    log_types = {"error":["err",0],"info":["info",0],"debug":["dbg",0],"warn":["wn",0]}
    for log in result:
        if log["Log Message"] not in log_codes:
            log_types[log["Log Type"]][1] += 1
            log_codes[log["Log Message"]] = log_types[log["Log Type"]][0] + str(log_types[log["Log Type"]][1])
    print(log_codes)

def get_word_freq(words):
    global freq
    for word in words:
        if word in freq.keys():
            freq[word] += 1
        else:
            freq[word] = 1
    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    for item in freq:
        freq_list.append({"Word":item[0],"Frequency":item[1]})

def create_csv():
    field_names = ["Path","Log Type","Log Message","Characters"]
    with open('Log_Details.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(result)
    # with open('Word_Frequency.csv', 'w') as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=["Word", "Frequency"])
    #     writer.writeheader()
    #     writer.writerows(freq_list)

#MAIN
if __name__ == "__main__":
    get_logs()
    # get_word_freq(words)
    # create_log_codes(result)
    create_csv()