# This is not the runner for nodes!
# This is the runner for the Flask server!

echo "Please enter your sudo password if asked."
sudo echo "Done. Server can start."

/stuff/./pypy3.9-v7.3.9-linux64/bin/pypy -m pip install -r requirements.txt

while true
do
    echo · Started LibreNode ·
    /stuff/./pypy3.9-v7.3.9-linux64/bin/pypy librenode/app.py
    echo · Stopped LibreNode ·
    sleep 3
done