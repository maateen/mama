#Mama
The aim of this project is to let you use [Microsoft powered Bing Speech Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api) to control your Linux computer. The project is developed in Python3. For note, this is a fork of project [google2ubuntu](https://github.com/benoitfragit/google2ubuntu).

The mother project, [google2ubuntu](https://github.com/benoitfragit/google2ubuntu), is a tool that **Franquet Benoit** started 2 years ago, written in Python2. Unfortunately, he was not able to do what he wanted because of a lack of time. Perhaps, he used Google Web Speech API which isn't free anymore.

So I am moving the project to the next level using [Microsoft powered Bing Speech Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api) by renaming it **Mama**.

###Why is it renamed Mama?
In **Bangladesh**, the term **Mama** is similar to maternal uncle. But now-a-days, it has become a common calling name of people, known/unknown. Actually we call someone **mama** with love. That's the matter!

The project consists in 2 principal Python3 scripts:

* mama.py
* mama-manager.py

The first one lets you send commands to Microsoft and then execute some actions. The second one lets you manage all the commands.

**Franquet Benoit** has done huge efforts to make the program easy to install and easy to use. Besides, he has made the project internationalized by bringing it available in French, English, Dutch, Spanish and Italian.

# Special thanks
Before I begin, I want to thank some of you who help **Franquet Benoit** a  lot.

##Contributors
Devs | Translators | Bug reports
-----| ----- | -----
[tectas](https://github.com/tectas)|[tectas](https://github.com/tectas)|[bmeznarsic](https://github.com/bmeznarsic)
[mte90](https://github.com/mte90)|[mte90](https://github.com/mte90)|[Andrew from Webupd8](https://github.com/hotice)
[levan7](https://github.com/Levan7)|[lincus](https://github.com/lincus)|[mte90](https://github.com/mte90)
[ladios](https://github.com/ladios)|[ladios](https://github.com/ladios)|[mads5408](https://github.com/mads5408)
Josh Chen|[Frank Claessen](https://github.com/frankclaessen)|

#Installation
### Dependancies

For the moment, dependancies are:

* bash
* python3
* python3-gi
* libnotify-dev
* sox
* xdotool
* libsox-fmt-mp3
* acpi
* python3-simplejson
* python3-xmltodict
* python3-pyaudio

If you are installing Mama from source not from deb or from ppa, type this:
```
sudo apt-get install bash python3 python3-gi python3-simplejson libsox-fmt-mp3 sox libnotify-dev acpi xdotool
```

##First launch
###Main programs
Once you have installed Mama, you can attribute a shortcut to those 2 Python scripts:

```
python3 /usr/share/Mama/mama.py
python3 /usr/share/Mama/mama-manager.py
```

Moreover, if you search in the application's menu you will find two launchers, one for each of those programs.

After that, you can launch `mama-manager.py` in order to manage all commands.
![Mama-manager](http://pix.toile-libre.org/upload/original/1392223354.png)


As you can see, Mama comes with several default commands. I will explain you how to manage and add commands.

###Basic configs
Then you can configure Mama by clicking on the **Setup** button, that will open a window
![setup](http://pix.toile-libre.org/upload/original/1392400825.png)

In this window you can:

1. configure the language you want to use, by changing the language in the combobox. For the GUI the will take effect after restart.
2. Set the recording time (seconds) between 1 and 10 seconds
3. Set the command to pause/play the media player, (If you don't know what command to use let it emply)
4. Activate/Deactivate and configure the hotword mode

For the last two parameters, as there is a lot of media player (vlc, mplayer, banshee, ...) I think this way is the most efficient because it lets anybody writing a basic shell script that will pause or play his favorite media player. So those commands could be shell commands or could be more elaborated scripts

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
| dictation mode | Enter in dictation mode |
| exit dictation mode | Exit dictation mode |

If you want to add an internal command, open the little menu near the "Add" button and select "internal". Then replace "your key" by the "key" you will pronounce to call this command and replace "word" by one of those 5 actions' name.

####Some words about dictation mode

The dictation mode let you type all word you pronouce. If you want to enter in the dictation mode use the dictation mode internal function. If you want to exit this mode just use the associated function. Dictation is not continue so you have to launch Mama for each sentence you want to type

###Modules
In order to extand Mama very easily I've implemented a system of modules that lets developers adds their own scripts in Mama. Besides, all modules will receive the text that you pronounce in parameter

####Module's description
A module is basically, an executable file that will receive some text in argument. each module embed its configuration in your configuration file. Two fields are recorded for each module:

* linker
a vord that let us distinguish the call to the module and the parameter we have to send to this module. For example, if I want to configure the module google, I can choose the linker "google " because when I make a research I say:
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
* **meaning**
This plugin allows you to ask to the meaning of a word, for exemple if I ask:
```
meaning barack obama
```
The plugin will tell me that he is the actual president of the US

####Note for the user
Perhaps, you will have to modify the linker field of those module by selecting the module and clicking on the edit button

#Go Linux automation
Once you have personalized and take care about the commands already included in Mama, you can launch the recognition by launching `Mama.py`

A little sound is played and a notification tell you to speak. Then the notification show the result and the action associated to the text you have pronounced is played.

#How-to contribute
##Design some modules
If you want you can write a module that will be integrated in the Github page, the user will have to download it and will be able to use it
##Translate the app
###Translate the Mama core
If you want to translate this app, you need first to download the [project](https://github.com/benoitfragit/Mama/archive/master.zip) then unzip it and open a terminal and place yourself in the folder newly created. Then, be sure that all string that you want to translate are like that:
```
_('text to translate')
```
Then be sure, that there is this at the begenning of the file you want to translate (only needed for Mama.py, gogl2ubuntu-manager.py)
```
import gettext

gettext.install('Mama',os.path.dirname(os.path.abspath(__file__))+'/i18n/')
```

So, if you want to add a new language, you should type:

```
mkdir -p i18n/<new_language/LC_MESSAGES
xgettext --language=Python --keyword=_ --output=./i18n/Mama.pot ./*.py librairy/*.py
msginit --input=./i18n/Mama.pot --output=./i18n/<new_language>/LC_MESSAGES/Mama.po
```
The 2 first line are optional and are usefull only there is no .pot file in the i18n/ folder.

Then, open the `.po` file and translate all the line, then compoile the `.po` :
```
msgfmt ./i18n/<new_language>/LC_MESSAGES/Mama.po --output-file ./i18n/<new_language>/LC_MESSAGES/Mama.mo
```


###Update the translation
To update an existing translation, you have to do several actions:
```
xgettext --language=Python --keyword=_ --output=./i18n/Mama.pot ./*.py librairy/*.py
msgmerge --update --no-fuzzy-matching --backup=off ./i18n/<current_language>/LC_MESSAGES/Mama.po ./i18n/Mama.pot
```

Then translate new line and compile the `.po`:
```
msgfmt ./i18n/<current_language>/LC_MESSAGES/Mama.po --output-file ./i18n/<current_language>/LC_MESSAGES/Mama.mo
```
## Share ideas
You can share ideas and contact me on the google+ comunauty:
[Mama](https://plus.google.com/u/0/communities/103854623082229435165)

## Demonstration
<a href="http://www.youtube.com/watch?feature=player_embedded&v=vkuX4tqaLFU
" target="_blank"><img src="http://img.youtube.com/vi/vkuX4tqaLFU/0.jpg"
alt="Mama" width="480" height="360" border="5" /></a>

## Documentation page
I've wrote a documentation page with Sphinx
[Documentation](http://benoitfragit.github.io/Mama/)

#Update

## Improvements

| State | Addons
|---|---
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a menu to change language
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a class to manage locale easily
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a dictation mode
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding the possibility to reconfigure a module from Mama-manager
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | drag & drop a folder automaticcaly add a line in the treeview with a command to open it
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a man page
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding spanish translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding deutch translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding italian translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct dependancies
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding Sox not recording in 16kHz bug fixe
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct module setup button bug
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct pyGobject constructor issue
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | regroupe both remove all and delete in one button
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | delete button bug fixe when no item selected
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | localHelper not cut locale name
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | beginning to work on the HelpWindow
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | changing i18n locale's folder name
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct a bug due to module execution
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding pt_BR support
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding pt_PT support
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding traditional chinese translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct the wikipedia module
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding nl_NL support
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | simplify module configuration storage
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding an edit button that open an edit window
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding an hotword mode
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | Support for google web speech api v2
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | update the documentation
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | improve translation
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | bug fixe
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | adding russian translation
