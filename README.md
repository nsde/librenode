# ⛏️ LibreNode · Minecraft Server Manager
![](librenode/static/assets/cover.png)
A **free and open source** Minecraft server manager with awesome integrations!

## FAQ
### What is a "node"?
Nodes are, as the project's name suggests, one of the most important features of *LibreNode*. But what do they do?

Nodes are essentially Minecraft servers. You can start, stop, modify, create, delete, join them and more. You have console access as well as a file manager and mod/plugin store. They aren't just a folder. They also have a screen process running.

### What does LibreNode cost?
Nothing! If you already have e.g. a VPS ready to run Minecraft, there's nothing you have to pay for. Just install LibreNode, set things up, and have fun!

And even if you don't have a VPS: if you have a powerful PC or laptop, you can use it to host your server!

### Will strangers be able to access the admin panel?
Thanks to the login/auth wall, users are forced to log in first. The user account as well as their IP address and will be verified before they can access the admin panel.

### [PLANNED] Can I also upload my own mods and plugins?
Sure! It's not difficult - just to go the "Files" tab, go to the plugins or mods folder (depending on your server type) and click the upload button.

Just make sure that the server supports your plugin or mod or plugins or mods in general. There are mods for Fabric, as well as Forge and they often aren't compatible with each other. Also check the mod's or plugin's Minecraft recommended version.

### Can I change the server port?
When creating a node, you can assign it a custom port. The port can be almost any number from 1 to 65535 which is not already used by other processes. When changing the server port to anything other than 25565, you can set up a subdomain for the custom port or tell your players to use the new port number when connecting to your server. Here are a few examples:
```
play.examplecraft.net
exampleserver.net:1234
192.168.1.1:9876
127.0.0.1:9999
81.123.432:1212
localhost:1111
```

### Can I have a different server IP?
IP addresses are assigned by your ISP. You can use tools such as [no-ip.com](no-ip.com), [ngrok](https://ngrok.com/) or [CloudFlare tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide) [none of these are an endorsement!] to give your IP address a custom (sub-)domain for free for about a month.

### [PLANNED] Can I use a different server for the web panel than the Minecraft server nodes?
This feature is planned. Sorry. You can use file syncing software, though.

### [PLANNED] Can I self-host LibreNode?
Sure! We're planning on better compatibility, though.
As of right now, you have to change quite a few files, but that might change soon.

###### LibreNode is not affiliated with Mojang, Microsoft or Minecraft in any way.
