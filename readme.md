# slack-open-dialog-with-python
Opens a dialog when called with the specified command. This dialog box contains text field and selection boxes. It sends a message to the channel specified in the config file as a result of the request.

#### Gef files
```bash
git remote add origin https://github.com/sevvalkahraman/slack-open-dialog-with-python.git
git pull origin master
```

#### Create an environment

```bash
python -m venv venv
```

#### Activate the environment
```bash
venv\Scripts\activate.bat 
```

#### Deactivate the environment
```bash
venv\Scripts\deactivate.bat
```

#### Install libraries in Requirements file.
```bash
pip install -r requirements.txt
```

#### Run the service
```bash
set FLASK_APP=application.py
flask run
```

#### Post Json 'http://127.0.0.1:5000/'

Create interactivity and shortcut on your Slack app. \
![Command](https://i.ibb.co/bbkx0Hz/7.png)


Write the command.\
![Command](https://i.ibb.co/2gG2bQM/slack1.png)

Opens a dialog window.\
![Command](https://i.ibb.co/kcN7wjw/Slack2.png)

Send it anonymously.\
![Command](https://i.ibb.co/VgcPxVK/Slack3.png)

Message view; (message.txt file)\
![Command](https://i.ibb.co/VMCxSwT/Slack4.png)

![Command](https://i.ibb.co/888F1jH/slack5.png)
