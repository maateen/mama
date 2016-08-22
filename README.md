#Mama
The aim of this project is to let you use [Microsoft powered Bing Speech Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api) to control your Linux computer. The project is developed in Python3. For note, this is a fork of project [google2ubuntu](https://github.com/benoitfragit/google2ubuntu).

The mother project, [google2ubuntu](https://github.com/benoitfragit/google2ubuntu), is a tool that **Franquet Benoit** started 2 years ago, written in Python2. Unfortunately, he was not able to do what he wanted because of a lack of time. Perhaps, he used Google Web Speech API which isn't free anymore.

So I am moving the project to the next level using [Microsoft powered Bing Speech Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api) by renaming it to **Mama**.

###Why is it renamed Mama?
In **Bangladesh**, the term **Mama** is similar to maternal uncle. But now-a-days, it has become a common calling name of people, known/unknown. Actually we call someone **mama** with love. That's the matter!

The project consists in 2 principal Python3 scripts:

* mama.py
* mama-manager.py

The first one lets you send commands to Microsoft and then execute some actions. The second one lets you manage all the commands with a nice GUI, powered by `PyGtk3`.

#Installation
### Dependencies

For the moment, dependencies are:

* python3
* python3-gi
* python3-xmltodict
* python3-pyaudio
* libnotify-dev
* xdotool
* acpi
* gksu
* unzip

If you are using Ubuntu/Debian, type this to install all dependencies:
```
sudo apt-get install python3 python3-gi python3-xmltodict python3-pyaudio libnotify-dev acpi xdotool gksu unzip
```
Now we will install the main things.
```
wget "https://github.com/maateen/mama/releases/download/v0.1/mama-v0.1.zip"

unzip mama-v0.1.zip
cd mama
sudo python3 install.py
```
That's all. Now you should get the success message.
####Note: Mama should run like a king on every Linux distribution. Just install the above dependencies with relevant command.

##Configuration
###Main programs
Once you have installed Mama, you can attribute a shortcut to those two of Python scripts:

```
python3 /usr/share/mama/mama.py
python3 /usr/share/mama/mama-manager.py
```

Moreover, if you search in the application's menu you will find two launchers, one for each of those programs.

After that, you can launch `mama-manager.py` in order to manage all commands.
![Mama-manager](https://raw.githubusercontent.com/maateen/mama/gh-pages/Screenshot_from_2016_07_20_21_32_22.png)


As you can see, Mama comes with several default commands. I will explain you how to manage and add commands.

###Basic configs
Then you can configure Mama by clicking on the **Setup** button, that will open a window
![setup](https://raw.githubusercontent.com/maateen/mama/gh-pages/Screenshot_from_2016_07_20_21_37_12.png)

In this window you can:

1. Set you locale, the language in which the speaker will talk.
2. Set audio chunk
3. Set number of channels
4. Set sampling sate
5. Set recording time
6. Set Microsoft Azure Client ID, please visit: [https://portal.azure.com/](https://portal.azure.com/) for your client ID. It is required.
7. Set Microsoft Bing Speech API Key, please visit [https://www.microsoft.com/cognitive-services/en-us/speech-api](https://www.microsoft.com/cognitive-services/en-us/speech-api) for our API key. It is required.

For the last two parameters, please visit our wiki for details.

#Manage commands

##Commands' storage
By default, Mama comes with several commands stored in a default xml file:
```
/usr/share/mama/config/<your_language>/default.xml
```
For the moment, there is a default file for French, English, Spanish, Deutch and Italian users, if your language is not currently supported the default voice will be English.

At the first, launch, a module folder is created in:
```
~/.config/mama
```
The first time you add, modify or remove a command, your commands' configuration will be also stored in this folder in the file:
```
~/.config/mama/mama.xml
```


##Commands' description
A command is a pair of `key` and `action`. Each `key` referes to an `action`. Many `key` can leads to the same `action`.
To define a command, you do not need to make explicitaly all the word you will tell, I mean, if I want to create the command:
```
key: open my documents
action: xdg-open ~/Documents
```
The word `my` is not usefull so, I will put:
```
key: open documents
action: xdg-open ~/Documents
```
Don't care about capital letter, because the program automatically put the text in lowercase.


I've implemented different types of command:

* **external commands**
* **internal commands**
* **modules**

###External commands

External commands are basically commands that you can run in your terminal:
```
exo-open --launch MailReader
```
If you want to add an external command, just click on the "Add" button. Then find the newline and replace "your key" by the key you want to associate to the command and replace "your command" by the action.

###Internal commands
####What are they ?
Internal commands are commands that I've implemented in Mama, for the moment there is 3 internal commands:

| Name | Function |
| --- | --- |
| time   |  Tell the current time |
| power | Tell the battery state |
| clipboard | Read the text selected by the cursor |

If you want to add an internal command, open the little menu near the "Add" button and select "internal". Then replace "your key" by the "key" you will pronounce to call this command and replace "word" by one of those 5 actions' name.

###Modules
In order to extend Mama very easily I've implemented a system of modules that let developers add their own scripts in Mama. Besides, all modules will receive the text that you pronounce in parameter

####Module's description
A module is basically, an executable file that will receive some text in argument. each module embed its configuration in your configuration file. Two fields are recorded for each module:

* linker
a word that let us distinguish the call to the module and the parameter we have to send to this module. For example, if I want to configure the module google, I can choose the linker "google " because when I make a research I say:
```
google who is barack obama
```
So, the google module will be call with `who is barack obama` in parameter.
* spacebyplus
If spacebyplus=1 then space are replace py +.

####How to add a module
If you want to add a script,  the gui will help you to create one and will place the module in :
```
~/.config/mama/modules
```

You can add a module by opening the menu near to the "Add" button then selecting the executable files of the module.
Yu can also simply drag&drop this executable on the treeview and the module will be automatically added. When you add a new module you don't have to modify the `action` field in the newline. You just have to modify the `key` field in the gui.


####Already available
Mama already comes with 6 modules:

* **google**
This plugin allows you to make search on Google and open the web browser on the search page you ask for.
* **wikipedia**
This plugin allows you to make search on Wikipedia
* **youtube**
This plugin allows you to make search on YouTube
So your locations need to be between the word "between" and "and"
* **weather**
This plugin allows you to ask Google to show you the weather for a city
* **goto**
This plugin allows you to open a new web page with the web page you want. For example if you have configurated the plugin liker this:
```
your sentence = go to
linker = to
```
Then if you say "go to gmail.com", a new web page is going to be open with gmail.com

####Note for the user
Perhaps, you will have to modify the linker field of those module by selecting the module and clicking on the edit button

#Go Linux automation
Once you have personalized and take care about the commands already included in Mama, you can launch the recognition by launching `mama.py`

A little sound is played and a notification tell you to speak. Then the notification show the result and the action associated to the text you have pronounced is played.
