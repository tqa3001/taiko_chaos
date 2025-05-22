python .\poc.py --track .\example\vocaloid.mp3

# TODO
- Consolidate v1 -> pick features necessary
- Make sure v1 == v(embedded) == v(core)
- Get hardware setup done for simple drum input
- Implement v(core) in rust and add a python port for extension

# TaikoChaos Core :: features
- TBD

# List of all future features for full extension

## Short-term

### Usability
    [] Embedded friendly
        ? Minimal core version that can fit with a $12 microcontroller + 32gb sd?
            - might need to port or rewrite C++/rust to optimize time and memory
    [] CLI friendly
        [] Single binary
        [] ? Display the whole control tree when -h ? like each node having
            a character and etc and all valid commands must be complete (no states between bin calls)
        [] colored text
    [] Web friendly
        - No menu but the URL? Or simple tree based like above but GUI?
    [] Keep it simple 
        [] ? Load custom file type -> has all needed data
        [] Single build/install step

### Track exploration
    [] Import module
        [x] Youtube
        [] MIDI
    [] reorganize track storage
    [] Search (simple grep or tag based)
    [] track menu 
        per difficulty
        - edit (below)
        - play options (below)
        - stats (below)

### Stats
#### User stats
#### Track stats

### Track edit options
    [] Generate
        [] Checklist of difficulties to generate for?
        [] Manual generate by playing on an empty map + specify min alignment/bpm?
    [] Manual edits (e.g correct autogen errs)
    [] Segment of interest: Create, edit, loop, play
    ? more deterministic note color marking
        - based on type of drum sound?
        - based on pattern (length, etc)

### Play options :: (onsets, song segment)
    [] Select speed (original +-5(slow tap) bpm)
    [] Modes
        - Randomize notes
        - Divergent notes (differing velocities)
        - Strict alternate (penalty if not)
        - Restart on miss
    [] Time travel (ideas?)
        - Pause and move + set checkpoints?

## Morse code mode (. = don, - = ka)
    [] Normal scoring with a slow song: each word -> play morse of first letter
    [] Min time to finish a paragraph (like type racer)

### Core
    [x] Decide on a smallest beat duration and smoothen all notes to that
    [] Gold drum
        [] Drum spam practice mode? 
    [] Scoring system
    [] Find accurate methods for onsets
    [] Minimize render jitter
    [] Optimize source query + generation times + Diversify sources

### GUI
    [] MUST keep non distracting
    [] Sound to alert 50x, 100x

### Preferences (low prio)
    [] Drum sounds

## Medium-term
[] integrate all to a single cli (gui only when playing track)
[] crossplatform support
[] embedded support: drum input only 
[] web support

## Longer-term
[] add CONTRIBUING.md
[] full embedded support -> separate hardware, usb for programming

## Unrelated
[] abstractions
    [] IO
        - left_don()
        - right_don()
        - left_ka()
        - right_ka()
    [] Track
        - list_tracks(query_args...)
        - get_track_from_youtube()
            > save onsets + made tracks
    [] GUI
        - play_track()
no need for sounddevice anymore (confirm)
consider upgrading to a higher python if not using spleeter