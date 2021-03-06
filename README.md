# Nothing to Hide
## Warning
This project is on the very early stages of development. On same rare
occasions it might tele-transport your computer to event
horizon. Also, this version only supports the English language, sorry :(
## The Problem
Email is [not a very private method of communication.](https://en.wikipedia.org/wiki/Email_security#Privacy_concerns)
## Current Solutions
There has been several attempts to make email more secure such as using end-to-end
encryption. Some technologies, such as [GPG](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) do provide great security.
But this and other methods of encryption have failed to gather
traction. Without being popular, the system is not very effective since
it requires all parties involved in communication to have a special
setup. Also, many of the current solutions are hard to setup and configure for many
users. Nothing to Hide tries a radically different approach to securing email.

## Our Solution
Nothing to Hide attempts to make email more secure by making messages
more vague, in such a way that the intended recipient can still
understand the message but snoopers can't. In it's current form it
only available as [Google Chrome](https://www.google.com/intl/en/chrome/browser/) and [Chromium](http://www.chromium.org/Home) add-on for [Gmail](https://mail.google.com). A
[Firefox](https://www.mozilla.org/en-US/firefox/new/) version of the add-on is on the works.

## Installation

First install our [Chrome extension](https://chrome.google.com/webstore/detail/keiegjchmoggjbpgfjdjghbiicpjneoe). Also, you need the following installed:

-   [Java](http://openjdk.java.net/) (Only tested with Java 7 and higher)
-   [Python](http://python.org/) (Only tested with Python 2.7.x and higher)
-   [pip](https://pypi.python.org/pypi/pip/) (Only tested with 1.4.x and higher) How to install pip on
      [Windows](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows) and [Mac OS X.](http://docs.python-guide.org/en/latest/starting/install/osx/) Ubuntu users run `sudo apt-get install python-pip`.

### Automated
The automated method has only been tested in GNU/Linux and Mac OS
X. It should work for other Unix operating systems. Windows users have
to use the manual method.

####  Via Curl
If you're using `curl` type the following command:
```bash
curl -L https://raw.github.com/climatewarrior/nothing-to-hide/master/utils/installer.sh | bash
```
#### Via Wget
If you're using `wget` type:
```bash
wget --no-check-certificate https://raw.github.com/climatewarrior/nothing-to-hide/master/utils/installer.sh -O - | bash
```

### Manual
1. Download the latest [Stanford NER](http://nlp.stanford.edu/software/CRF-NER.shtml)
2. Download the latest [Stanford Postagger](http://nlp.stanford.edu/software/tagger.shtml)
3. Get extra NTLK dependencies `python -m nltk.downloader punkt`
4. Install Flask and Pyner `pip install flask ner`
5. Get the [latest version of our code](https://github.com/climatewarrior/nothing-to-hide/archive/master.zip)
6. Uncompress Stanford NER and Stanford Postagger into the `anstractor-server` directory within Nothing to Hide.
7. See [run.sh](https://github.com/climatewarrior/nothing-to-hide/blob/master/utils/run.sh) to how to start your servers manually.

## How to use
1.  `cd` to the install directory, the default one is `~/nothing-to-hide`.
2.  Start the server with: `bash utils/run.sh`.
3.  Open Chrome or Chromium and open your Gmail account.
4.  Write your email messages as you normally would.
5.  Before sending them hit the VAGUE-IFY button below the compose button.
6.  Revise your messages. You can click on change words to bring them to their original form.
7.  When you are happy with your changes click Accept on the compose window.
8.  Shutdown the server whenever you wish or just leave it running in
    the background.

# Developer
## Contributing
### Building
####  Dependencies

-   [Pyner](https://github.com/dat/pyner)
-   [Flask](http://flask.pocoo.org/)
-   [Stanford NER](https://github.com/dat/stanford-ner)
-   [Stanford Tagger](http://nlp.stanford.edu/software/tagger.shtml)
-   [NLTK](https://pypi.python.org/pypi/nltk/2.0.1)
