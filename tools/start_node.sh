echo "·· BEGIN ··"
echo "Minecraft: <minecraft_version>"
echo "Java: <java_binary>"
echo "Path: <path>"
echo "Port: <port>"
echo "Max Players: <max_players>"

cd <path>

while true
do
  echo "· START ·"
  echo 'eula=true'>eula.txt

  # ———————————————————————————————————————————————— #
  <java_binary> -Xms6144M -Xmx6144M --add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -Dcom.mojang.eula.agree=true -jar server.jar -p <port> -s <max_players> --nogui > run.log
  # ———————————————————————————————————————————————— #
  
  echo 'eula=true'>eula.txt
  echo "RESTARTING... Use CTRL + C to terminate."
  sleep 5
  echo "· STOP ·"
done
