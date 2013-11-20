dns_manager
===========

有这样一个需求,域名testoa.com使用DNSPOD管理，配置公网DNS；
服务器内网同样有一套Bind的DNS管理系统，用来管理内部域名；
但是在内网却解析不了外部的testoa.com，dns_mananger解决了这样的问题，
在添加外部域名时，同时在DNSPOD上与内部Bind上增加公网域名记录，这样就可以解析
脚本只提供了增加、更新记录功能，没有删除操作
