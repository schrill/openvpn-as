# openvpn-as
Simple OPENVPN Access server implementation
based on documentation provided by https://github.com/eduvpn/documentation/blob/master/attic/AS_API.md

To every one who would like to use OpenVPN client app on Android and iOS and found placing ovpn files to mobile manually to much work.
I've writen this python servlet in order to easily access the configuration files from within the android client as by using an official openvpn AS server.
The script is writen in python3 and the following libraries are required os,base64,xmlrpc.server,redis
The script listens on localhost port 15000 y default. Default redis configuration: localhost port 6379. 
The script can distribute multiple ovpn files depending on the hostname by which the servlet is accessed.
For example if you proxy the server through apache by accessing for ex. https://vpn.example.com from your openvpn mobile client, the file which will be returned is vpn_vpn.ovpn
The default ovpn file location is /etc/openvpn_conf/ with prefix vpn_
Change the above to fit your needs.

As of now the script only functions for autologin, other methods are also included but according functions are not written. 
