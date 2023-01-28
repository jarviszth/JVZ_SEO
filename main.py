import configparser, requests, string, random, os, json, shutil, stat, ctypes, gc
from subprocess import call

ctypes.windll.kernel32.SetConsoleTitleW("JVZTH | SEO [V 1.0]")

config = configparser.ConfigParser()
config.read('config.ini')

with open("keyword.json", 'r', encoding='utf-8') as f:
    keyword = json.load(f)

def randomRepoName(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def RandomKeyword():
    return random.choice(keyword['keyword'])

def RandomName():
    return random.choice(keyword['name'])

def RandomUrl():
    return random.choice(keyword['url'])

def RandomPackage(REPOSITORY):
    package = {
        "name": REPOSITORY,
        "theme": "syntax",
        "version": "0.0.0",
        "description": RandomKeyword() + " " + RandomKeyword() + " " + RandomKeyword(),
        "keywords": [
            RandomKeyword() + " " + RandomKeyword() + " " + RandomKeyword(),
            RandomKeyword() + " " + RandomKeyword() + " " + RandomKeyword(),
            RandomKeyword() + " " + RandomKeyword() + " " + RandomKeyword()
        ],
        "repository": "https://github.com/" + config['config']['GITHUB_USER'] + "/" + REPOSITORY +".git",
        "license": "MIT",
        "engines": {
            "atom": ">=1.0.0 <2.0.0"
        }
    }

    with open('package.json', 'w', encoding='utf-8') as f:
        json.dump(package, f, ensure_ascii=False, indent=4)

def RandomReadme():
    README = "# " + RandomName() + " " + RandomName() + " " + RandomName() + "\n\n"
    for topic in range(4):
        README += "## " + RandomName() + " " + RandomName() + " " + RandomName() + " " + RandomName() + "\n\n"
        for row in range(5):
            for detail in range(0, random.randint(15, 20)):
                README += RandomKeyword() + " "
            README += "\n"
        README += "\n"
    for link in range(6):
        README += "[" + RandomName() + "](" + RandomUrl() + ")\n\n"
    
    with open('README.md', 'w', encoding='utf-8') as f:
       f.write(README)

def AtomPublish():
    try:
        name = str(config['config']['GITHUB_USER']) + str(random.randrange(10000, 999999))
        os.system("apm publish major --rename " + str(name))
    except:
        return AtomPublish()
    else:  
        return
    
def SEO():
    API_URL = "https://api.github.com"
    REPOSITORY = randomRepoName()
    payload = '{"name": "' + REPOSITORY + '", "private": false}'
    headers = {
        "Authorization": "token " + config['config']['GITHUB_TOKEN'],
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        r = requests.post(API_URL + "/user/repos", data = payload, headers = headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    try:
        REPO_PATH = "Repository/"
        os.chdir(REPO_PATH)
        os.system("mkdir " + REPOSITORY)
        os.chdir(REPOSITORY)
        RandomPackage(REPOSITORY)
        RandomReadme()
        os.system("git init")
        os.system("git remote add origin https://" + config['config']['GITHUB_TOKEN'] + "@github.com/" + config['config']['GITHUB_USER'] + "/" + REPOSITORY + ".git")
        os.system("git add . && git commit -m 'Initialized' && git push -u origin master")
        os.system("git config --global credential.helper wincred")
        AtomPublish()
        os.chdir("../")
    except FileExistsError as err:
        raise SystemExit(err)

    for i in os.listdir(str(REPOSITORY)):
        if i.endswith('git'):
            tmp = os.path.join(str(REPOSITORY), i)
            while True:
                call(['attrib', '-H', tmp])
                break
            shutil.rmtree(tmp, onerror=on_rm_error)
    shutil.rmtree(str(REPOSITORY))
    os.chdir("../")

    try:
        r = requests.delete(API_URL + "/repos/" + config['config']['GITHUB_USER'] + "/" + REPOSITORY, headers = headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

if __name__ == "__main__":
    # SEO()
    while True:
        SEO()
        gc.collect()
