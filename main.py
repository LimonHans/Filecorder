#coding=utf-8
###############################
#   HansLimon on 2023/01/04   #
#                             #
#   Only for personal usage   #
#                             #
#     CopyLEFT Mongrokey      #
###############################
import os
import sys
import json
import zipfile
from io import BytesIO
from PIL import Image

local_position = sys.path[0]
invalid_file = []
customname = "LA_Homework5"
customname_address = "hslimonffs@outlook.com"
customname_prefix = "Hans"
customname_subject = "SME2_LA_Homework5"
custom_skipkey = "2-"

if __name__ == '__main__':
    print(f"[Info] Now at [ {local_position} ]")
    for root, dirs, files in os.walk(os.path.join(local_position, "filenow")):
        for file in files:
            print(f"[Info] Now for file {file}")
            try:
                zfile = zipfile.ZipFile(os.path.join(local_position, "filenow", file), "r")
            except:
                invalid_file.append(file)
                continue
            if file[:-4] in zfile.filelist[0].filename:
                try:
                    zfile.extractall(path=os.path.join(local_position, "filecord"))
                except:
                    invalid_file.append(file)
            else:
                nowpath = os.path.join(local_position, "filecord", file[:-4])
                try:
                    os.mkdir(path=nowpath)
                except:
                    print(f"\033[0;36m[Weak Warning] Dir {file[:-4]} already exists!\033[m")
                try:
                    zfile.extractall(path=nowpath)
                except:
                    invalid_file.append(file)
            zfile.close()
        for file in files:
            if file not in invalid_file:
                os.remove(os.path.join(local_position, "filenow", file))
    if invalid_file.__len__():print(f"\033[0;33m[Warning] These files are invalid {invalid_file}\033[m")
    if True or os.listdir(os.path.join(local_position, "filecord")).__len__() == 29:
        with open("state.json", "r") as jsoncordfile:
            jsoncord = json.load(jsoncordfile)
        if jsoncord["emailstate"]["sent"]:
            exit(0)
        print("[Info] Try to zip")
        try:
            zfile = zipfile.ZipFile(os.path.join(local_position, f"{customname}.zip"), "w")
            for nowdir in os.listdir(os.path.join(local_position, "filecord")):
                #print(root, dirs, files)
                for root, dirs, files in os.walk(os.path.join(local_position, "filecord", nowdir)):
                    for nowfile in files:
                        if nowfile[:1] == custom_skipkey: continue
                        ########
                        # MARK #
                        ########
                        print(f"[Info] Try to write {nowfile} into ZIP")
                        if nowfile.split('.')[-1] == "jpg":
                            imgnow = Image.open(os.path.join(root, nowfile))
                            datanow = BytesIO()
                            imgnow.save(datanow, format="jpeg")
                            zfile.writestr(os.path.join(nowdir, nowfile), datanow.getvalue(), compress_type=zipfile.ZIP_DEFLATED)
                            imgnow.close()
                            datanow.close()
                        else: zfile.write(filename=os.path.join(root, nowfile),
                                          arcname=os.path.join(nowdir, nowfile), compress_type=zipfile.ZIP_DEFLATED)
            zfile.close()
        except:
            os.popen(f'sudo python3 {os.path.join(local_position, "withemail.py")}'
                     f' --name "{customname_address}" --prefix "{customname_prefix}" --subject "{customname_subject}"'
                     f' --errormode')
            exit(412)
        print("[Info] Zip successful")
        print("[Info] Response from withemail.py: ", end="")
        withemail_ans = os.popen(f'sudo python3 {os.path.join(local_position, "withemail.py")}'
                                 f' --name "{customname_address}" --prefix "{customname_prefix}"'
                                 f' --subject "{customname_subject}" --attachment').read()
        print(withemail_ans)
        if "Send Failed" not in withemail_ans:
            jsoncord["emailstate"]["sent"] = 1
            with open("state.json", "w") as jsoncordfile:
                json.dump(jsoncord, jsoncordfile, ensure_ascii=False, indent=4)
        else: print("\033[1;31m[Error] fail to send mail\033[m")