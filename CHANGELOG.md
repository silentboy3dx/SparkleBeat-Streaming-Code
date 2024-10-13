# v0.0.17
* An exception will now been thrown if trying to load from a directory that is not found fixing #16.
* The playlist class now has a new function called get_first_song()
* The stream class now has a new function called set_first_song()

# v0.0.16

* Fixed a bug where the end stream callback was triggered even the stream did not start. Fixing #11 
* Fixed a bug where announcements for songs would not play for the first song in the playlist.
* Added support for nm3u playlist files, fixing #12
* Added the function should_announce_songs() to the stream class. Fixing #14


# v0.0.15

* Updated the example code.
* Added decorators for @stream_started and @stream_ended

# v0.0.14

* Added an option to the song object to construct it with the requested_by parameter.
* Added a trigger to the stream object to announce songs with two new decorators stream.song_announcement()
  and stream.song_announcement_played()


# v0.0.13 and v0.0.13.1
* Fixed a bug that could crash the stream if there are no jingles.

# v0.0.12
* Updated the stop stream function as it had a small bug.

# v0.0.11
* Added an option to force stop streaming.
* 
# v0.0.11

* Removed some files that made it into release v0.0.10

# v0.0.10

* Added an example configuration file
* Updated the README.md file
* Added a CHANGELOG.md file.
* Added an example .env file
* Added usage code in README.md
* Added documentation