import shutil
import os
import sys
import csv
import stat
import pdb
import time
import datetime

csv.field_size_limit(sys.maxsize)

test_csv_dir = sys.argv[1]
char_dir = sys.argv[2]
output_dir = sys.argv[3]


timestamp = datetime.datetime.now().strftime('%m%d-%H%M%S')
data_dir = 'data.' + timestamp

filenames = []
fict_dict={}
if (not os.path.isdir(data_dir)): 
    os.mkdir(data_dir)  # input text file directory
if (not os.path.isdir(char_dir)): 
    os.mkdir(char_dir)   # output directory for characters
if (not os.path.isdir(output_dir)): 
    os.mkdir(output_dir) # output direcotry for corefs

for filename in os.listdir(test_csv_dir):
    if filename.endswith(".csv"):
        filenames.append(filename)
    else:
        continue
print (test_csv_dir)
print (len(filenames))
print ("Processing inputs..")
for filename in filenames:

    this_text=''
    fic_id = ''
    chap_id = ''
    #print (test_csv_dir+filename)
    # for row in csv.DictReader(open(test_csv_dir+filename, encoding='cp1250'))
    for row in csv.DictReader(open(test_csv_dir+filename)):
        if row["chapter_id"] == "chapter_id": # header
            continue
        if len(fic_id)==0:
            fic_id = row["fic_id"]
        else:
            if fic_id != row["fic_id"]:
                pdb.set_trace()
            assert fic_id == row["fic_id"]

        if len(chap_id)==0:
            chap_id = row["chapter_id"]
        else:
            assert chap_id == row["chapter_id"]

        this_text+=row["text"]
        this_text+=" # . "

    # dump all the txt files in the DataDir folder 
    #print ("DataDir/"+filename[:-4])
    with open(data_dir + "/"+filename[:-4],'w') as f:
        f.write(this_text)
        f.close()

print ("Running coref..")
os.chdir("CoreNLP")
os.system("./run.10G.sh " + data_dir +  " " + char_dir + " " + output_dir)
    #os.remove(filename[:-4])
    #os.chdir("..")
    #if (not os.path.isdir(char_dir)):  
    #   os.mkdir(char_dir)
    #if (not os.path.isdir(output_dir)):       
    #   os.mkdir(output_dir)
    #os.rename("./CoreNLP/"+filename[:-4]+".chars" , "./"+char_dir+"/"+filename[:-4]+".chars" )
    #os.rename("./CoreNLP/"+filename[:-4]+".coref.out" , "./"+char_dir+"/"+filename[:-4]+".coref.out" )
    # pdb.set_trace()
    #shutil.move("./CoreNLP/"+filename[:-4]+".chars" , char_dir+"/"+filename[:-4]+".chars")
    #shutil.move("./CoreNLP/"+filename[:-4]+".coref.out" ,output_dir+"/"+filename[:-4]+".coref.txt")

os.chdir("..")
print("Processing the outputs..")
for filename in filenames:
    
    fname = output_dir+"/"+filename[:-4]+".coref.txt"
    exists = os.path.isfile(fname)
    if(exists):
        f = open(output_dir+"/"+filename[:-4]+".coref.txt")
        #fin = open(test_csv_dir+filename, encoding='cp1250')
        fin = open(test_csv_dir+filename)
        reader = csv.reader(fin)
        header = next(reader)
        #fout = open(output_dir+"/"+filename[:-4]+".coref.csv","w", encoding='cp1250')
        fout = open(output_dir+"/"+filename[:-4]+".coref.csv","w", encoding='utf8')
        writer = csv.writer(fout)
        lines = f.readlines()
        writer.writerow(header)
    
        for row,text in zip(reader, lines):
        #row["paragraph"] = text
        #print (row["paragraph"])
        #print (text)
            row[len(row)-1]= text
            writer.writerow(row)
        #print (row['paragraph'])

        fin.close()
        f.close()
        fout.close()

    else:
        print (fname, " file not found")
        continue
