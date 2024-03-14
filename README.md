# Every Frame in Order Bot
This is tool i use to run my:
[Every Charlotte Frame in Order](https://www.facebook.com/ECFIOID), 
[Every BanG Dream Frame in Order](https://www.facebook.com/EBDFIO)
Facebook Fanspage.

Tested in Debian with Python 3.10.8.
## Preparation

First, you need to extract all frames from video into **frames** folder. You can use **ffmpeg** for this.

Example, if you have Charlotte_episode2.mp4 on **videos** folder, you can run this command.
``` bash
mkdir frames
ffmpeg -i 'videos/Charlotte_episode2.mp4' -vf fps=1 ./frames/%04d.png -hide_banner
```

![Frame Extract](https://telegra.ph/file/2784f4f459293c97a2468.png)

Your extracted frames will named 0001.png, 0002.png, etc. Example:
```bash
ryzen@raspberrypi:~$ ls -lha ./frames/ | head -n 8
total 49M
drwxr-xr-x 2 ryzen ryzen 4.0K Mar 13 17:51 .
drwxr-xr-x 5 ryzen ryzen 4.0K Mar 13 17:51 ..
-rw-r--r-- 1 ryzen ryzen 7.0M Mar 13 17:51 0001.png
-rw-r--r-- 1 ryzen ryzen 8.1M Mar 13 17:51 0002.png
-rw-r--r-- 1 ryzen ryzen 8.2M Mar 13 17:51 0003.png
-rw-r--r-- 1 ryzen ryzen 5.5M Mar 13 17:51 0004.png
-rw-r--r-- 1 ryzen ryzen 5.5M Mar 13 17:51 0005.png
```
![Frames Folder](https://telegra.ph/file/cab273cebf9753f5b7764.png)

If you need to delete opening images, ending images, or some images from **frames** directory, you need to reorder the file name again. Use this command:
``` bash
cd frames
ls -v | grep '.png' | cat -n | while read new old; do mv -n "$old" `printf "%04d.png" $new`; done
```
## Setup Application and Token
First, create your apps in [Facebook Developer](https://developers.facebook.com/apps). Next, get your token at [Graph API Explorer](https://developers.facebook.com/tools/explorer). And then, extend your token expiration at [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/).

## Setup Bot
Ok, all frames is ready to upload. Next, ajjust some value from ``run.py``.

Change value of ``ACCESS_TOKEN`` with your token.

To avoid your application blocked (because of spam detection), i am adding **MIN_DELAY** and **MAX_DELAY** on every requests . You can change to your desired value but remember, dont set below **3 min (180 sec)** because Facebook can limit your page and flag it as **Spam**.

In my case, for 1 Episode of Charlotte, around **1.5GB** disk will be used for extracted frames. So, this tool will remove every frame that already uploaded to freed your disk space.

## Run Bot
After all is completed, just run Frame in Order bot with this command:
``` bash
python3 run.py --start 1
```
And if you want to continue running again, start from frame 41.
``` bash
python3 run.py --start 41
```
Example of output:
![Charlotte Frames in Order](https://telegra.ph/file/bc56964cc6e0188dbf74a.png)

Default loop value is unlimited. But you can set loop value using --loop flag. Example:
``` bash
python3 frame-in-order.py --start 41 -loop 4
```
Above command will upload frame from 0041.png until 0045.png.

## Contact
If you have any question about this Bot, you can contact me directly on [Facebook](https://www.facebook.com/Nao.Tomori.UwU).