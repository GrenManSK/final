# final

This is group of functions from installing carousel to packing files with encoding

## anime_rename.py

- Will ask for directory containing video files (anime episodes) and rename it to the simpler titles

- Sometimes process would fail and will try to rename it to episode number 'none'. There is always a confirmation, so be careful if you see an error message

## code2string.py

- Library that will convert script to one-line file format

### example for code2string.py

```python
from final.code2string import c2s
c2s('foo.txt', 'bar.txt').start() # Arg 1. is input file name; Arg 2. is output file name also returns output
# If output file is set to 'None' or empty string then it will only output a text
```

## completer.py

- Library to auto-complete with tab key
- Input is list

### Example for completer.py

```python
import readline
from final.completer import SimpleCompleter

readline.set_completer(
    SimpleCompleter(['foo', 'bar']).complete)
readline.parse_and_bind('tab: complete')
```

## downloadmusic.py

- Library to dowload music
  
### Example for downloadmusic.py

```python
from final.downloadmusic import DownloadMusic
DownloadMusic('Shelter - Robinson')
# Mind that video have to be on Youtube

```

### Installation

If you have already installed pytube go to the pytube directory and cipher.py file ({your_python}/site-packages/pytube/cipher.py)

On line 411 remove all content of the line and change it to 'transform_plan_raw = js'

## git.py

- Same as `git clone`

## mathematical.py

- Library to use some mathematical calculations inclucding random id generation

## music.py

- Little better than `pygame.mixer`

## pack.py

- Using [krkr-xp3](https://github.com/awaken1ng/krkr-xp3/) as packer
- Can pack files with filesize limit e.g. file will be split

## profiler.py

- Profile your function
- See how many time your function run and also if you output a file you can see see how long operations run

## pymp4.py

- Convert gif to mp4

## pywinmove.py

- Move window to desired place

## rapi.py

- Random anime quotes
- Random anime fanart  

## sql.py

- Library that handles SQL server

### Example for sql.py

```python
HOST_NAME = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = 'password'
DATABASE = 'foo'

server = SQLServer(HOST_NAME,
                   port=PORT,
                   user=USER,
                   passwd=PASSWORD,
                   database=DATABASE,
                   log=True)

server.connect()

database = server.execute('SELECT * FROM foo.bar') # returns tuple
```

## unpack.py

- Using [krkr-xp3](https://github.com/awaken1ng/krkr-xp3/) as packer
- Oposite of `pack.py`

## writing.py

- log function
- installing carousel
