# pypodbackup

A simple script to backup a podcast's episodes to your computer. See my [post][1] for more information.

## Usage

You can check a single feed by passing it to the script:

	./pypodbackup.py http://example.com/path/to/feed

Alternatively, you can add a file named `podcasts.txt` in the script's directory and fill in multiple podcast feed urls (one per line). If you don't pass a feed as a parameter then the script tries to download all episodes for all those feeds.

The script does not download files that have already been downloaded (it checks if the file already exists in the script's directory.)

## Author

Florian Heiber (florian@heiber.me, [@flohei](http://twitter.com/flohei))

[1]:https://flohei.de/2015/02/podcast-backup-script/