import os
import sys
from typing import List

import music_tag

SUPPORTED_FILES_EXT = {'.mp3', '.wav', '.mp4', '.flac', '.aiff'}
excluded_directories = set()
if len(sys.argv) > 1:
    excluded_directories = set(sys.argv[1].split(','))


def build_tag(directories):
    return ' '.join(directories)


def tag_song(filename: str, directories: List[str]):
    genre_tag = build_tag(directories)
    print(f'Tagging {filename} with genre:{genre_tag}')
    try:
        f = music_tag.load_file(filename)
        f.remove_tag('genre')
        f.append_tag('genre', genre_tag)
        f.save()
    except Exception as e:
        print(f'Failed to process {filename} because of {e}, skipping file')



def process_file(base_filename: str):
    extension = os.path.splitext(base_filename)[1]
    if extension in SUPPORTED_FILES_EXT:
        dirname, filename = os.path.split(base_filename)
        dirs = dirname.split(os.path.sep)
        dirs.remove('.')

        if set(dirs).isdisjoint(excluded_directories) and len(dirs) > 1:
            dirs = dirs[1:]
            tag_song(base_filename, dirs)


for root, dirs, files in os.walk('.'):
    for filename in files:
        process_file(os.path.join(root, filename))
