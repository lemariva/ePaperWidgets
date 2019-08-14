#!/bin/bash
# ePaper-Widgets-Calendar software installer for Raspberry pi
# Version: 0.1 (August 2019)
# Stability status of this installer: Stable

echo -e "\e[1mPlease select an option from below:"
echo -e "\e[97mEnter \e[91m1 \e[97m to update the ePaper-Widgets software"
echo -e "\e[97mEnter \e[91m2 \e[97m to install the ePaper-Widgets software"
echo -e "\e[97mEnter \e[91m3 \e[97m to uninstall the ePaper-Widgets software"
echo -e "\e[97mConfirm your selection with [ENTER]"
read -r -p 'Waiting for input...  ' option

if [ "$option" != 1 ] && [ "$option" != 2 ] && [ "$option" != 3 ]; then
    echo -e "invalid number, aborting now"
    exit
fi
if [ -z "$option" ]; then
    echo -e "You didn't enter anything, aborting now."
    exit
fi
if [ "$option" = 3 ]; then
    echo -e "\e[1;36m"Removing the ePaper-Widgets software now..."\e[0m"
    pip3 uninstall Pillow -y && sudo pip3 uninstall Pillow -y && sudo pip3 uninstall pyowm -y&& sudo pip3 uninstall ics -y && pip3 uninstall pyowm -y && pip3 uninstall ics -y && sudo apt-get remove supervisor -y && pip3 uninstall feedparser -y && sudo pip3 uninstall feedparser -y && sudo apt-get clean && sudo apt-get autoremove -y
    if [ -e /etc/supervisor/conf.d/e_paper_widgets.conf ]; then
        sudo rm /etc/supervisor/conf.d/e_paper_widgets.conf
    fi
    echo -e "\e[1;36m"The libraries have been removed successfully"\e[0m"
    sleep 1
    echo -e "Removing the ePaper-Widgets folder if it exists"
    if [ -d "/home/pi/e_paper_widgets" ]; then
        sudo rm -r /home/pi/e_paper_widgets/
	echo -e "\e[1;36m"Found the ePaper-Widgets software folder and deleted it"\e[0m"
    fi
    echo -e "\e[1;36m"All done!"\e[0m"
fi

if [ "$option" = 1 ]; then
    echo -e "\e[1;36m"Checking if the settings.py exists..."\e[0m"
    if [ -e /home/pi/e_paper_widgets/settings.py ]; then
        echo -e "Found an ePaper-Widgets settings file."
        sleep 2
	echo "Backing up the current settings file in the home directory."
	sleep 2
	cp /home/pi/e_paper_widgets/settings.py /home/pi/settings-old.py
	echo -e "renaming the old ePaper-Widgets software folder"
	sleep 2
	cp -r /home/pi/e_paper_widgets /home/pi/e_paper_widget_old
	sudo rm -r /home/pi/e_paper_widgets
	echo "Updating now..."
        cd
    else
        # Ask to update anyway. May not work always, but can help with new versions.
	echo -e "\e[1;36m"Could not find the configuration file -settings.py- in /home/pi/e_paper_widgets"\e[0m"
	sleep 2
	echo -e "\e[1;36m"Would you like to update the ePaper-Widgets software anyway?"\e[0m"
        echo -e "\e[97mPlease type [y] for yes or [n] for no and confirm your selection with [ENTER]"
        read -r -p 'Waiting for input...  ' update_anyway
    
        if [ "$update_anyway" != Y ] && [ "$update_anyway" != y ] && [ "$update_anyway" != N ] && [ "$update_anyway" != n ]; then
            echo -e "invalid input, aborting now"
            exit
        fi
        if [ -z "$update_anyway" ]; then
            echo -e "You didn't enter anything, aborting now."
            exit
        fi
    
        if [ "$update_anyway" = Y ] || [ "$update_anyway" = y ]; then
            echo "Updating now..."
	else
	    echo -e "Not attempting to update, exiting now."
            exit
        fi
    fi
fi

if [ "$option" = 2 ]; then
    echo -e "\e[1;36m"Setting up the system by installing some required libraries for python3"\e[0m"

    # Installing a few packages which are missing on Raspbian Stretch Lite
    echo -e "\e[1;36m"Installing a few packages that are missing on Raspbian Stretch Lite..."\e[0m"
    sudo apt-get install python3-pip -y 
    sudo apt-get install python-rpi.gpio-dbgsym -y python3-rpi.gpio -y python-rpi.gpio -y python3-rpi.gpio-dbgsym -y python3-spidev -y git -y libopenjp2-7-dev -y libtiff5 -y python3-numpy -y
    echo ""

    # Running apt-get clean and apt-get autoremove
    echo -e "\e[1;36m"Cleaning a bit of mess to free up some space..."\e[0m"
    sudo apt-get clean && sudo apt-get autoremove -y
    echo ""
fi

if [ "$option" = 1 ] || [ "$option" = 2 ]; then
    # Ask to update system
    echo -e "\e[1;36m"Would you like to update and upgrade the operating system first?"\e[0m"
    sleep 1
    echo -e "\e[97mIt is not scrictly required, but highly recommended."
    sleep 1
    echo -e "\e[97mPlease note that updating may take quite some time, in rare cases up to 1 hour."
    sleep 1
    echo -e "\e[97mPlease type [y] for yes or [n] for no and confirm your selection with [ENTER]"
    read -r -p 'Waiting for input...  ' update
    
    if [ "$update" != Y ] && [ "$update" != y ] && [ "$update" != N ] && [ "$update" != n ]; then
        echo -e "invalid input, aborting now"
        exit
    fi
    if [ -z "$update" ]; then
        echo -e "You didn't enter anything, aborting now."
        exit
    fi
    
    if [ "$update" = Y ] || [ "$update" = y ]; then
        # Updating and upgrading the system, without taking too much space
        echo -e "\e[1;36m"Running apt-get update and apt-get dist-upgrade for you..."\e[0m"
	sleep 1
        echo -e "\e[1;36m"This will take a while, sometimes up to 1 hour"\e[0m"
        sudo apt-get update && sudo apt-get dist-upgrade -y
        echo -e "\e[1;36m"System successfully updated and upgraded!"\e[0m"
        echo ""
    fi

    # Installing dependencies
    
    #PYOWM for user pi
    echo -e "\e[1;36m"Installing dependencies for the Inky-Calendar software"\e[0m"
    
    echo -e "\e[1;36m"Checking if pyowm is installed for user pi"\e[0m"
    if python3.5 -c "import pyowm" &> /dev/null; then
        echo 'pyowm is installed, skipping installation of this package.'
    else
        echo 'pywom is not installed, attempting to install now'
	pip3 install pyowm
    fi
    
    #PYOWM for user sudo
    echo -e "\e[1;36m"Checking if pyowm is installed for user sudo"\e[0m"
    if sudo python3.5 -c "import pyowm" &> /dev/null; then
        echo 'pyowm is installed, skipping installation of this package.'
    else
        echo 'pywom is not installed, attempting to install now'
	sudo pip3 install pyowm
    fi
    
    #Pillow for user pi  
    echo -e "\e[1;36m"Checking if Pillow is installed for user pi"\e[0m"
    if python3.5 -c "import PIL" &> /dev/null; then
        echo 'Pillow is installed, skipping installation of this package.'
    else
        echo 'Pillow is not installed, attempting to install now'
	pip3 install Pillow==5.3.0
    fi
    
    #Pillow for user sudo
    echo -e "\e[1;36m"Checking if Pillow is installed for user sudo"\e[0m"
    if sudo python3.5 -c "import PIL" &> /dev/null; then
        echo 'Pillow is installed, skipping installation of this package.'
    else
        echo 'Pillow is not installed, attempting to install now'
	sudo pip3 install Pillow==5.3.0
    fi
    
    #Ics.py for user pi  
    echo -e "\e[1;36m"Checking if ics is installed for user pi"\e[0m"
    if python3.5 -c "import ics" &> /dev/null; then
        echo 'ics is installed, skipping installation of this package.'
    else
        echo 'ics is not installed, attempting to install now'
	pip3 install ics
    fi
    
    #Ics.py for user sudo
    echo -e "\e[1;36m"Checking if ics is installed for user sudo"\e[0m"
    if sudo python3.5 -c "import ics" &> /dev/null; then
        echo 'ics is installed, skipping installation of this package.'
    else
        echo 'ics is not installed, attempting to install now'
	sudo pip3 install ics
    fi

    #feedparser for user pi  
    echo -e "\e[1;36m"Checking if feedparser is installed for user pi"\e[0m"
    if python3.5 -c "import feedparser" &> /dev/null; then
        echo 'feedparser is installed, skipping installation of this package.'
    else
        echo 'feedparser is not installed, attempting to install now'
	pip3 install feedparser
    fi
    
    #feedparser for user sudo
    echo -e "\e[1;36m"Checking if feedparser is installed for user sudo"\e[0m"
    if sudo python3.5 -c "import feedparser" &> /dev/null; then
        echo 'feedparser is installed, skipping installation of this package.'
    else
        echo 'feedparser is not installed, attempting to install now'
	sudo pip3 install feedparser
    fi
    
    #pytz for user pi  
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if python3.5 -c "import pytz" &> /dev/null; then
        echo 'pytz is installed, skipping installation of this package.'
    else
        echo 'pytz is not installed, attempting to install now'
	pip3 install pytz
    fi
    
    #pytz for user sudo
    echo -e "\e[1;36m"Checking if pytz is installed for user sudo"\e[0m"
    if sudo python3.5 -c "import pytz" &> /dev/null; then
        echo 'pytz is installed, skipping installation of this package.'
    else
        echo 'pytz is not installed, attempting to install now'
	sudo pip3 install pytz
    fi
    
    #googleapiclient for user pi 
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if python3.5 -c "from googleapiclient.discovery import build" &> /dev/null; then
        echo 'googleapiclient is installed, skipping installation of this package.'
    else
        echo 'googleapiclient is not installed, attempting to install now'
	pip3 install google-api-python-client
    fi

    #googleapiclient for user sudo 
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if sudo python3.5 -c "from googleapiclient.discovery import build" &> /dev/null; then
        echo 'googleapiclient is installed, skipping installation of this package.'
    else
        echo 'googleapiclient is not installed, attempting to install now'
	sudo pip3 install google-api-python-client
    fi

    #google-auth-httplib2 for user pi 
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if python3.5 -c "google_auth_oauthlib.flow import InstalledAppFlow" &> /dev/null; then
        echo 'google_auth_oauthlib is installed, skipping installation of this package.'
    else
        echo 'google_auth_oauthlib is not installed, attempting to install now'
	pip3 install google-auth-httplib2
    fi

    #google-auth-httplib2 for user sudo
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if sudo python3.5 -c "google_auth_oauthlib.flow import InstalledAppFlow" &> /dev/null; then
        echo 'google_auth_oauthlib is installed, skipping installation of this package.'
    else
        echo 'google_auth_oauthlib is not installed, attempting to install now'
	sudo pip3 install google-auth-httplib2
    fi

    #google.auth for user pi 
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if python3.5 -c "from google.auth.transport.requests import Request" &> /dev/null; then
        echo 'googleapiclient is installed, skipping installation of this package.'
    else
        echo 'googleapiclient is not installed, attempting to install now'
	pip3 install google-auth-oauthlib
    fi

    #google.auth for user sudo
    echo -e "\e[1;36m"Checking if pytz is installed for user pi"\e[0m"
    if sudo python3.5 -c "from google.auth.transport.requests import Request" &> /dev/null; then
        echo 'googleapiclient is installed, skipping installation of this package.'
    else
        echo 'googleapiclient is not installed, attempting to install now'
	sudo pip3 install google-auth-oauthlib
    fi

    echo -e "\e[1;36m"Finished installing all dependencies"\e[0m"
    
    # Clone the repository, then delete some non-required files
    echo -e "\e[1;36m"Installing the Inky-Calendar Software for your display"\e[0m"
    cd ~
    git clone https://github.com/lemariva/ePaperWidgets.git e_paper_widgets
    
    # Make a copy of the sample settings.py file
    cd ~/e_paper_widgets
    cp settings.py.sample settings.py

    # add a short info
    cat > /home/pi/e_paper_widgets/info.txt << EOF
This document contains a short info of the e-paper-widget software version

Version: 0.1
Installer version: 0.1 (August 2019)
configuration file: /home/pi/e_paper_widgets/settings.py
If the time was set correctly, you installed this software on:
EOF
    echo "$(date)" >> /home/pi/e_paper_widgets/info.txt
    echo ""

    # Setting up supervisor
    echo -e "\e[1;36m"Setting up auto-start of script at boot"\e[0m"
    sudo apt-get install supervisor -y

    sudo bash -c 'cat > /etc/supervisor/conf.d/e_paper_widgets.conf' << EOF
[program:e_paper_widgets]
command = sudo /usr/bin/python3.5 /home/pi/e_paper_widgets/e_paper_widget.py
stdout_logfile = /home/pi/e_paper_widgets/e_paper_widgets.log
stdout_logfile_maxbytes = 1MB
stderr_logfile = /home/pi/e_paper_widgets/e_paper_widgets_err.log
stderr_logfile_maxbytes = 1MB
autorestart = true
EOF

    sudo service supervisor start e_paper_widgets

    echo ""

    # Final words
    echo -e "\e[1;36m"The install was successful"\e[0m"
    echo -e "\e[1;36m"The programm is set to start at every boot."\e[0m"
    
    echo -e "\e[1;31m"To enter your personal details, please check"\e[0m"
    echo -e "\e[1;31m"the file settings.py"\e[0m"
    echo -e "\e[1;36m"inside /home/pi/e_paper_widgets/"\e[0m"
    
    echo -e "\e[1;36m"You can test if the programm works by typing:"\e[0m"
    echo -e "\e[1;36m"python3.5 /home/pi/e_paper_widgets/e_paper_widgets.py"\e[0m"
fi
