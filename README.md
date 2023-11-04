<h1 style="display: flex; justify-content: center">Zipper Bot</h1>

---

## Overview

This is an enhanced version of the [Zipper Bot](https://github.com/htrueman/sfu-telegram-bot) that can package files and
images into ZIP archives on Telegram.
The enhancements introduced to the bot include the features below.

## Features

1. ***Expanded File Format Support***

   The bot can now package a wider variety of file formats, making it more versatile and useful for users.

2. ***Handling Telegram File Size Limit***

   The bot now takes into account Telegram's file size limit of 50 MB. If a file exceeds this limit, the bot will inform
   the user and not process the file.

3. ***Automatic Buffer Cleanup***

   To prevent excessive storage usage, the bot now includes an automatic buffer cleanup feature. If the total size of
   files in the buffer exceeds 20 MB, the bot will automatically remove the oldest files to stay within the limit.

4. ***Notification for Buffer Cleanup***

   When the bot performs a buffer cleanup, it will send a message to the user, informing them about the number of files
   and images removed during the cleanup process.

5. ***Meaningful Image Naming***

   Images are now given more meaningful filenames in the format "image_year-month-day_hour-minute-second_ms",
   making it easier for users to identify and manage their images.

6. ***Empty Buffer Notification***

   If the bot's buffer is empty, it will send a notification to the user, indicating that the buffer is clear. The bot
   will remain idle until the user sends files for processing.

## How to Use

* Start a chat with the bot on Telegram.
* Send the bot a file or image you wish to package in a ZIP archive.
* Run a command ```/zip``` and press ```Yes```. You will get a structured ZIP archive back.
  Or you can manually delete all cached files by clicking another button.  
