爬小猪佩奇视频，问题总结

0.JavaScript菜鸟学库：https://www.runoob.com/

1.什么是javascript:void(0)？  
答：https://m.runoob.com/js/js-void.html
javascript:void(0) 中最关键的是 void 关键字， void 是 JavaScript 中非常重要的关键字，该操作符指定要计算一个表达式但是不返回值。
如果要定义一个死链接请使用 javascript:void(0) 。

2.爬取视频，当前最好的方案是什么？
答：利用第三方解析网站对视频进行解析。  https://www.cnblogs.com/pontoon/p/10306826.html
打开：http://jx.618g.com/?url=这个第三方解析网站，将待解析的视频url加在后面就行了。如：http://jx.618g.com/?url=https://www.iqiyi.com/v_19rr57g7ng.html?vfm=2008_aldbd#curid=1354363600_0a0926c68b65688792f7c1052bcccd38

3.Fiddler抓取的安装与使用？
答：https://www.cnblogs.com/fuxinxin/p/9146693.html

4.视频文件是什么后缀？
m3u8是苹果公司推出一种视频播放标准，是m3u的一种，不过 编码方式是utf-8，是一种文件检索格式，将视频切割成一小段一小段的ts格式的视频文件，
然后存在服务器中（现在为了减少I/o访问次数，一般存在服务器的内存中），通过m3u8解析出来路径，然后去请求。
关于详细的介绍.m3u8以及.ts文件推荐一篇博客给大家，如果不懂的话可以去看看https://blog.csdn.net/a33445621/article/details/80377424。

5.处理视频的python库？
import m3u8

6.视频加密了吗？
可以用python脚本自动下载这些ts文件，但实际上有些网站的ts文件是用AES-128加密过的，所以需要解密才能播放。

7.octet-stream是什么？
application/octet-stream数据除非你明确知道是什么格式内容，否则不可能正确解析。
比如其可能是传递的字符串数据，也可能是传递的二进制数据，就这点你就没有办法光凭application/octet-stream进行正确区分了。
所以对于application/octet-stream数据的使用，一般是前后端能够协调的开发中使用。








