from glob import glob
import os
import json
import shutil
import binascii


#we go through all caches from older to newer to generate all bundles


all_cache_paths =  [
    "/TFU Stuff/UnityCache/Transformers Universe/"
    ]

out = "./generated_bundles"

json_template = {'compressed': True, 'streamVersion': 3, 'unityVersion': '3.x.x', 'unityRevision': '4.5.3f3', 'files': []}



def main():

    for cache_path in all_cache_paths:

        subfolders= [f.path for f in os.scandir(cache_path) if f.is_dir()]
        #print(subfolders)

        for folder in subfolders:
            list_of_files = glob(f"{folder}/*")

            file_names = []

            file_revision = ""

            all_files_bytes = b""

            for file in list_of_files:
                if os.path.basename(file) == "__info":
                    pass
                    # with open(file,"r") as info_file:
                    #     file_revision = info_file.readlines()[1:2][0][:-1]
                else:
                    shutil.copyfile(file, f"./disunity_work/test/{os.path.basename(file)}")
                    file_names.append(os.path.basename(file))
                    all_files_bytes += open(f"./disunity_work/test/{os.path.basename(file)}","rb").read()

            # We assume CRC32 is calculated from core file. This might be wrong, but works fine for _Index
            core_file_name = min(file_names, key=len)

            file_crc = binascii.crc32(all_files_bytes)
            file_crc_string = str(file_crc)

            if os.path.exists(f"./generated_bundles/{file_crc_string}"):
                print("Such file CRC already exists. Skipping.")
                continue

            # if os.path.exists(f"./generated_bundles/{file_revision}"):
            #     print("Such file version already exists. Skipping.")
            #     continue

            # if os.path.exists(f"./files/{min(file_names,key=len).split('-')[-1]}.unity3d"):
            #     print(".unity3d file with such name exists. Skipping.")
                #continue

            new_json = json_template.copy()
            new_json['files'] = file_names
            #print(new_json)
            with open(f"./disunity_work/test.json","w") as file:
                file.write(json.dumps(new_json))

            os.system("java -jar ./disunity_work/disunity.jar bundle pack ./disunity_work/test.json")





            if os.path.exists(f"./generated_bundles/{file_crc_string}"):
                # We assume that additional files doesn't matter and if core file CRC32 is the same we skip such file
                pass

                # shutil.move("./disunity_work/test.unity3d",
                #             f"./generated_bundles/{file_crc_string}/{core_file_name.split('-')[-1]}.unity3d")
            else:
                os.mkdir(f"./generated_bundles/{file_crc_string}")
                shutil.move("./disunity_work/test.unity3d",
                            f"./generated_bundles/{file_crc_string}/{core_file_name.split('-')[-1]}.unity3d")

            print(f"{core_file_name.split('-')[-1]}.unity3d\n")
            for file in list_of_files:
                if os.path.basename(file) != "__info":
                    os.remove(f"./disunity_work/test/{os.path.basename(file)}")


if __name__ == '__main__':
    main()
