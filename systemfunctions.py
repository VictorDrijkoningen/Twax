import requests

def update(force_update = False):
    with open(".env") as f:
        env = f.read().split(",")
    with open("VERSION") as file:
        twax_version = file.read()
        githubversion = requests.get(env[0]).text
        if twax_version != githubversion or force_update:
            print(twax_version.split("-")[0]+" / "+ str(githubversion).split("-")[0])
            with open('VERSION', 'w') as f:
                f.write(githubversion)
            with open('main.py', 'w') as f:
                f.write(requests.get(env[1]).text)
            with open('AnetBoard/AnetBoard.ino', 'w') as f:
                f.write(requests.get(env[2]).text)
            with open('systemfunctions.py', 'w') as f:
                f.write(requests.get(env[3]).text)
            upload_to_anet()
        print('done updating')
    return twax_version


def upload_to_anet():
    pass