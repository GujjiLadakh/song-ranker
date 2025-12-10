# Song ranker

This simple program allows you to rank songs by artists by comparing each song from each album and allowing you to choose.

## How it works

Input the artist name (this is purely for the .txt file, no other purpose) and the number of albums.

Then for each album, input the ranked tracklist for that album beginning with the song you like the most and ending with the song you like the least, separated by commas (no spaces).

The program will then display each album and the least liked song off that album. This will allow you to compare songs and choose the one you like the least. The display will update after you provide input. There is some basic validation for inputs.

After the ranking has been created, the average position of each album is calculated and displayed, along with the entire tracklist. This data is then stored in a .txt file title {artist_name}_ranked.txt.

Hope you enjoy!
