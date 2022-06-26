while true
do
    echo Started LibreNode
    screen -S lino python3 librenode/app.py
    screen -x lino
    echo Stopped LibreNode
    sleep 3
done