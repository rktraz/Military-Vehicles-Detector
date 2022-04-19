# Military-Vehicle-Detector-bot
This is my per-project. Built using YOLOv5 and my custom dataset.

*Send me an image of any military vehicle and I will detect and classify it!📑*


## Installation
Clone this repo and install all required dependencies

```sh
pip install -r requirements.txt 
```

Edit config.py - add a **Telegram Bot Token** in the corresponding variable.

## How to use

To run bot:

```sh
python bot.py
```

Recieved images will be stored in *raw_images* folder, processed - in *processed_images* folder.

## Notes

 - version 1.0
 - Currently logs are printed in the console.
 - Only 10 Ukrainian and Russian tanks are supported
