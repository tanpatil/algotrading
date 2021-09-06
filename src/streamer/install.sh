sudo apt-get update
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
sudo apt install python3-selenium 
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
wget -N https://chromedriver.storage.googleapis.com/91.0.4472.101/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver