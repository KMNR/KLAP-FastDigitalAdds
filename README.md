KLAP-FastDigitalAdds
====================

Provides windows context tools to make adding digital albums a breeze

Requirements
====================

This needs the following python libraries

* Mutagen
* py2exe
    
Creating the installer needs InnoSetup.

Creating The Installer
=====================
To create the installer, first run the following command

    python setup.py py2exe
    
Which creates the standalone executable.

Then use InnoSetup on the "installer.iss" to build the setup application

The installer will appear in the Output directory.

Using the setup utility will automatically create the shortcuts in windows explorer.

Using This Tool
======================

1. Browse to the folder containing MP3s. You can either right click in the empty space in the folder, or on the folder itself and select "Add To KLAP"
1. A window will open and report any problems and ask you to confirm the artist and album.
1. Once all information has been confirmed, KLAP will open in your default browser and allow you to create the entry.
   
Limitations
=======================
* If you mess up the artist name, you'll have run it again and manually set the correct name.
* If metadata isn't available it will probably not work.
* Weird things can happen if the track numbers are set up correctly.

Changelog
=======================

v0.1 - Initial Release

v0.2
   * Added support for zlib compressing url to allow a greater amount of track data to be sent before the upper limit on url length is met.
   
v0.3
   * Adds compilation support to the submitted data
   * Fixes an issue where strings did not get converted from unicode.