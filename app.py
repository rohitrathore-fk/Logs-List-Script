import os
import re
import csv

to_find = "FourKitesCommon::Logger."
target = "/Users/rohit.rathore/Desktop/Log Script/target/tracking-service"
result = []
words = []
freq = {}
freq_list = []


def get_logs():
    for root, dirs, files in os.walk(target):
        for filename in files:
            path = root+"/"+filename
            relative_path = os.path.relpath(path, target)
            try:
                with open(path) as df:
                    for line in df:
                        if re.match(to_find,line.strip()):
                            log_detail = re.search("\"(.*?)\"", line).group(1) if (re.search("\"(.*?)\"", line) != None) else "" # in between ""
                            if(log_detail == ""):
                                log_detail = re.search("\'(.*?)\'", line).group(1) if (re.search("\'(.*?)\'", line) != None) else "" # in between ''
                            words.extend(log_detail.split())
                            log_type_string = to_find+"(.*?)\("
                            log_type = re.search(log_type_string, line).group(1) # get log type before () and after Logger.
                            result.append({"Path":relative_path,"Log Type":log_type,"Log Message":log_detail,"Characters":len(log_detail)})
            except:
                print("ERROR GETTING FILE CONTENTS")

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
    with open('Word_Frequency.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Word", "Frequency"])
        writer.writeheader()
        writer.writerows(freq_list)

if __name__ == "__main__":
    get_logs()
    get_word_freq(words)
    create_csv()