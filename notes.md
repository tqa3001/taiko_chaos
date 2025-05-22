python .\poc.py --track .\example\vocaloid.mp3

(prioritize) features to work on 
[] improve onset accuracy
    + decide on a smallest beat duration and smoothen all notes to that
        + would actually also be an easy way to make maps easier
[] turn get_yt to a track
[] integrate all to a single cli (gui only when playing track)

[] time travel
    - edit mode? pause button + left right? 
[] difficulty selection in track generation
[] speed change
[] more deterministic note markers
    - based on type of drum sound
    - based on pattern
        + length 

[] midi import


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

[] packaging and use
    [] 

[x] youtube link -> track

no need for sounddevice anymore (confirm)
consider upgrading to a higher python if not using spleeter