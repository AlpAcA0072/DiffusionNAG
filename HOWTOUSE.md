open terminal shadowsocks proxy server: 
``sslocal -c /etc/shadowsocks.json -d start``

use proxy to download file: 
```proxychains curl xxxx
proxychains wget xxxx
proxychains apt-get xxxx```