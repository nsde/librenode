# This is not the runner for nodes!
# This is the runner for the Flask server!

echo Please enter your sudo password.
sudo echo Done. Server can start.

while true
do
    echo · Started LibreNode ·
    python3 librenode/app.py
    echo · Stopped LibreNode ·
    sleep 3
done