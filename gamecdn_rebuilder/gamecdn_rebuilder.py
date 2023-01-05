from glob import glob
import shutil
import os
import json


def main():

    with open("./_Index.json","r") as index_file:
        index_data = json.loads(index_file.read())

    index_data_entries = index_data['entries']

    unsorted_bundles = glob("../generated_bundles/*/*",recursive=True)
    #print(unsorted_bundles)

    print(f"Total entities in _Index: {len(index_data_entries)}")
    i = 1

    missing = 0
    perfect_crc = 0
    blind_pick = 0

    for gamecdn_entry in index_data_entries:
        i += 1
        gamecdn_bundle_candidates = []


        for bundle_path in unsorted_bundles:

            if f"{gamecdn_entry['name']}.unity3d" == os.path.basename(bundle_path):
                gamecdn_bundle_candidates.append(bundle_path)

        if len(gamecdn_bundle_candidates) == 0:
            print(f"[{i}] No bundle {gamecdn_entry['name']}.unity3d. Skipping")
            missing += 1
            continue

        biggest_file_path = ""
        biggest_file_size = 0

        file_was_found = False

        for gamecdn_bundle_candidate_path in gamecdn_bundle_candidates:

            file_crc = int(os.path.dirname(gamecdn_bundle_candidate_path).split("/")[-1])

            file_size = os.path.getsize(gamecdn_bundle_candidate_path)

            if file_size > biggest_file_size:
                biggest_file_size = file_size
                biggest_file_path = gamecdn_bundle_candidate_path

            if file_crc == gamecdn_entry['crc']:
                print(f"[{i}] Found perfect CRC match {gamecdn_entry['name']}.unity3d.")
                file_mover(gamecdn_bundle_candidate_path,gamecdn_entry['version'])
                file_was_found = True
                perfect_crc += 1
                break

        if file_was_found is False:

            print(f"[{i}] No perfect CRC matches for {gamecdn_entry['name']}.unity3d.")
            print(f"[{i}] Oh well, let's just pray and pick the biggest file")
            blind_pick += 1
            file_mover(biggest_file_path,gamecdn_entry['version'])

    total = perfect_crc + blind_pick
    print(f"Restored {total}/{len(index_data_entries)} (Missing: {missing}, Perfect: {perfect_crc}, Blind: {blind_pick})")

def file_mover(file_path:str,version:int):

    file_crc = int(os.path.dirname(file_path).split("/")[-1])


    print(f"Moving {os.path.basename(file_path)} | CRC: {file_crc}")

    if os.path.exists(f"../gamecdn/{version}/"):
        pass
    else:
        os.mkdir(f"../gamecdn/{version}")

    # print("Existing file in cdn tree is newer. Skipping")

    # shutil.copy(file_path,
    #             f"../gamecdn/{version}/{os.path.basename(file_path)}")
    # with open(f"../gamecdn/{version}/{os.path.basename(file_path)}.crc",
    #           "w") as version_file:
    #     version_file.write(str(file_crc))

if __name__ == '__main__':
    main()