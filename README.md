<h1 style="display: flex; justify-content: center">Zipper Bot</h1>

---

## Overview

Zipper is a Telegram bot designed to make managing and organizing files into archive.
With a focus on efficient file handling and organization, Zipper offers a set of features that allow you to zip files,
open a buffer for downloading, close the buffer, and clear the buffer with ease.

## Features

1. ***Zip Files***

   Zip all supported file types into an archive.
   Automatically sends the archive back to you if its size is less than 50MB.

2. ***Buffer Management***

   Open Buffer: The buffer for downloading files is automatically opened when you send your first file to the bot.
   Close Buffer: Disable the bots reaction to file messages, preventing them from being downloaded.

3. ***Buffer Cleanup***

   Clear Buffer: Recursively removes files from the buffer.
   Provides the user with statistics on how many files of each type were removed.

4. ***Auto File Renaming***

   Bot renames file in format and watch for duplicate naming in folder if it is, it adds counter.
   The bot follows a specific naming convention to rename files:

   ```<content_type>_<year>_<month>_<day>_<hour>_<minute>_<second>.<extension>```

   For example, an image file uploaded on January 1, 2023,
   at 1:00 pm would be renamed: ```photo_2023_01_01_13_00_00.jpg```
   The bot also checks for duplicate file names in the folder.
   If a file with the same name already exists, it adds a
   counter to the file name: ```photo_2023_01_01_13_00_00(1).jpg```,
   ```photo_2023_01_01_13_00_00(2).jpg``` and so on.
   This consistent naming convention helps organize files by their upload time and content type, while the duplicate
   file check prevents files from being overwritten.

## Supported File Types

* Video
* Animation
* Video Note
* Photo (JPG, JPEG, PNG)
* Document
* Voice
* Audio

## How to Use

* Start a chat with the bot on Telegram.
* Send the bot a file or image you wish to package in a ZIP archive.
* Run a command ```/zip``` and choose the appropriate option.
  You can get a structured ZIP archive back.
  Or you can clear the buffer (delete all files from the buffer).
  Also, you can close it for downloading (files that you are sending won't be downloaded)
  and open the buffer again (it will open by default if you sent to bot a file) 