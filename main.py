import requests


with open(".env") as f:
        env = f.read().split(",")


def update(force_update = False):
    with open("VERSION") as file:
        twax_version = file.read()
        githubversion = requests.get(env[0]).text
        if twax_version != githubversion or force_update:
            print(twax_version.split("-")[0]+" / "+ str(githubversion).split("-")[0])
            with open('VERSION', 'w') as f:
                  f.write(githubversion)
            with open('main.py', 'w') as f:
                  f.write(requests.get(env[1]).text)
            with open('AnetBoard', 'w') as f:
                  f.write(requests.get(env[2]).text)
            print('done updating')
    return twax_version









if __name__ == "__main__":
    print("starting")
    update()