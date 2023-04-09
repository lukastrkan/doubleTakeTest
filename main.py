import json
import pathlib
import time
import requests
import os


def get_file(path, index):
    return pathlib.PurePath(path).name, os.listdir(path)[index]


def dirs(path):
    out = []
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)):
            out.append(os.path.join(path, d))
    return out


def handle_files(path, index):
    for d in dirs(path):
        folder, file = get_file(d, index)
        requests.post(f'http://192.168.1.55:3000/api/filesystem/folders/{folder}')

        res = requests.post(f'http://192.168.1.55:3000/api/train/add/{folder}',
                            files=[('files[]', (file, open(f'{d}/{file}', 'rb'), 'image/jpeg'))])
        print(f'Uploaded {file} to {folder}')


def testFiles(path):
    result = {}
    for d in dirs(path):
        for i in range(90, 99):
            folder, file = get_file(d, i)
            if folder not in result:
                result[folder] = []
            requests.post(f'http://192.168.1.55:3000/api/recognize/upload',
                          files=[('files[]', (file, open(f'{d}/{file}', 'rb'), 'image/jpeg'))])

            print(f'Uploaded {folder}/{file} for testing. Waiting for result')

            time.sleep(10)

            match = requests.get('http://192.168.1.55:3000/api/match?page=1').json()['matches'][0]

            toAdd = {}
            for r in match['response']:
                toAdd[r['detector']] = r['results']

            result[folder].append(toAdd)
    return result


def main():
    for i in range(0, 50):
        print(i)
        handle_files('/home/lukas/Downloads/Celebrity_Faces_Dataset', i)
        running = True
        while running:
            print('waiting')
            sum = 0
            res = requests.get('http://192.168.1.55:3000/api/train/status')
            for r in res.json():
                sum += r['percent']

            if sum >= 1000:
                running = False
                print('All trained')
                break

        r = testFiles('/home/lukas/Downloads/Celebrity_Faces_Dataset')
        f = open(f"result{i}.json", "w")
        f.write(json.dumps(r))
        f.close()


if __name__ == '__main__':
    main()
