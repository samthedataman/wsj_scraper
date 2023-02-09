# OpenWeb Scrapers WSJ version

## Project setup

### Requirements file (dependency management)

- load all dependencies with the command:

```
pip3.9 install -r requirements.txt
```

### nltk configuration


- If you get a cert error of sorts then you can use this work around
- nltk local files must be downloaded first to your computer. To do so, run `python3.9` in terminal then copy, past this into your python3.9 emulator and run.

```
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()
```

### chromedriver configuration
- https://chromedriver.chromium.org/downloads
- Must match the version of your chrome
- E.G. this chromedriver in the repo is for: Chrome Version 100.0.4896.75 (Official Build)

### .env file setup
1. copy `.env.example` to root dir of repo
2. remove the `.example` part of filename so file is named just `.env`
3. populate values of file with your own ones

### sshing into server

1. update file permissions

`chmod 400 ./datamen-ec2-ssh-access-keypair.pem`

2. ssh into the server 

`ssh -i ./datamen-ec2-ssh-access-keypair.pem ubuntu@54.227.189.23`

### Running script on server in background (so doesn't get killed when closing ssh session)

- Note: this redirects stdout and stderror to the same file
```
nohup /usr/bin/python3.9 "/home/ubuntu/datamen/wallstreet_journal_comments_josh.py" > "/home/ubuntu/log_files/log_wjs_scraper_$var_date.txt" 2>&1 &
echo $! > /home/ubunut/nohup_saved_script_process_pid.txt
```
- then to kill the process you can run
```
kill -9 `cat save_pid.txt`
rm save_pid.txt
```