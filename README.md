# WebSlideshow
Play images slideshow directly from popular web galleries.


There are image providers from following web pages:
- nasa.gov
- www.break.com
- www.demotywatory.pl


Application is implemented in Python and contains following usage examples:
- displaying images (gtk),
- playing animated giffs (gtk),
- sending and handling custom signals (gtk),
- parsing xml (lxml),
- opening urls (pycurl),
- load classes in dynamic way,
- threading,
- unittest,
- logging.


### Features

List of features:
- fullscreen / windowed mode (key F11),
- play / pause (key Space),
- controlling display time (command line),
- playing directly from RAM (no store to hard drive),
- disable screensaver if needed (restore settings on exit).


### Adding new provider

To add new provider just put new module in "provider" directory. Module should contain class 
with the same name. The class needs to provide "provideUrl()" method returning url to image.
