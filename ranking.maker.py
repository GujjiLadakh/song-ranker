# R A N K E R

#############
# Libraries #
#############
from typing import Union, Tuple
from collections import deque
import logging

#############
# Constants #
#############
EMPTY_STRING = ''
LAST_TRACK = -1
FILENAME = 'rankings.txt'

###########
# Classes #
###########
class Track:
    def __init__(self, track_name: str):
        self.track_name: str = track_name
        self.position: int = 0

    def __repr__(self):
        return f'Track name: {self.track_name}\nPosition: {self.position}'

class Album:
    def __init__(self):
        self.album_name: str = EMPTY_STRING
        self.num_of_tracks: int = 0
        self.is_empty: bool = False
        self.tracklist: list[str] = []
        self.tracklist_copy: list[Track] = []
        self.average: int = 0

    def __repr__(self):
        return f'Album name: {self.album_name}\nNumber of tracks: {self.num_of_tracks}\nTracklist: {",".join(self.tracklist)}'

###############
# Subprograms #
###############
def reset_data_structures(num_of_albums: int) -> Tuple[list[Album], deque[Track], list[str]]:
    Albums: list[Album] = [Album() for _ in range(num_of_albums)]
    Final_ranking: deque[Track] = deque()
    display: list[str] = [EMPTY_STRING] * num_of_albums
    return Albums, Final_ranking, display

def initialise(Albums: list[Album], display: list[str], num_of_albums: int) -> Tuple[list[Album], list[str], int]:
    for album in range(num_of_albums):
        curr_album_name: str = input('Enter album name: ')
        curr_tracklist = input(f'Enter the ranked tracklist for \'{curr_album_name}\' separated by commas: ').split(',')
        Albums[album].album_name = curr_album_name
        Albums[album].num_of_tracks = len(curr_tracklist)
        Albums[album].tracklist = curr_tracklist
        # logger.info(f'Album name: {Albums[album].album_name}, Number of tracks: {Albums[album].num_of_tracks}, Tracklist: {Albums[album].tracklist}')
        display[album] = curr_tracklist[LAST_TRACK]
    # logger.info(f'Starting display: {display}')
    return Albums, display, num_of_albums

def display_menu(Albums: list[Album], display: list[str], num_of_albums: int) -> None:
    print()
    for album in range(num_of_albums):
        print(f'{Albums[album].album_name}: {display[album]:>20}')
    print()

def is_empty(Albums: list[Album], index: int) -> bool:
    if Albums[index].is_empty:
        return True
    elif len(Albums[index].tracklist) == 0:
        Albums[index].is_empty = True
        return True
    return False

def update_display(Albums: list[Album], display: list[str], num_of_albums: int, choice: str) -> Tuple[list[Album], list[str], int]:
    for track in range(num_of_albums):
        if display[track] == choice:
            if not is_empty(Albums, track):
                Albums[track].tracklist.pop(LAST_TRACK)
                if not is_empty(Albums, track):
                    display[track] = Albums[track].tracklist[LAST_TRACK]
                    # logger.info(f'Updated display: {display}, Tracklist: {Albums[track].tracklist}')
                    # logger.info(f'Updated tracklist: {Albums[track].tracklist}')
                    Albums[track].num_of_tracks -= 1
                else:
                    display[track] = EMPTY_STRING
            else:
                display[track] = EMPTY_STRING
            break
    return Albums, display, num_of_albums

def get_user_choice(Albums: list[Album], display: list[str], Final_ranking: deque[Track], num_of_albums: int) -> Tuple[list[Album], list[str], deque[Track], int]:
    choice: Union[None, str] = None
    while choice not in display:
        choice = input('Enter track to add: ')
    current_track = Track(choice)
    Final_ranking.appendleft(current_track)
    album_track = Albums[display.index(choice)]
    album_track.tracklist_copy.append(current_track)
    Albums, display, num_of_albums = update_display(Albums, display, num_of_albums, choice)
    return Albums, display, Final_ranking, num_of_albums

def is_processing_over(Albums: list[Album], num_of_albums: int) -> bool:
    if all([is_empty(Albums, i) for i in range(num_of_albums)]):
        return True
    return False

def display_final_ranking(Final_ranking: deque[Track]) -> None:
    print()
    print('Final ranking')
    for idx, track in enumerate(Final_ranking):
        track.position = idx + 1
        print(f'{track.position}: {track.track_name}')
    with open(FILENAME, 'w') as file:
        for song in Final_ranking:
            file.write(f'{song.position}: {song.track_name}\n')
        calculate_averages(Albums)
        file.write('\n')
        for album in Albums:
            file.write(f'{album.album_name}: {album.average:.0f}\n')
    print()

def calculate_averages(Albums: list[Album]) -> None:
    for album in Albums:
        for track in album.tracklist_copy:
            album.average += track.position
        album.average /= len(album.tracklist_copy)

def ranker() -> None:
    # logger.info('Starting program')
    num_of_albums: int = int(input('Enter the number of albums: '))
    Albums, Final_ranking, display = reset_data_structures(num_of_albums)
    Albums, display, num_of_albums = initialise(Albums, display, num_of_albums)
    while not is_processing_over(Albums, num_of_albums):
        display_menu(Albums, display, num_of_albums)
        get_user_choice(Albums, display, Final_ranking, num_of_albums)
    display_final_ranking(Final_ranking)
    # logger.info('End of program')

if __name__ == '__main__':
    # logging.basicConfig(
    # level=logging.INFO,
    # format="{asctime} | {levelname} | {name} | {lineno} | {funcName} | {message}",
    # style="{",
    # datefmt='%Y-%m-%d-%H:%M',
# )
    # logger = logging.getLogger(__name__)
    ranker()
