(transcript-on "lab1")
;; This starts the transcript file.
(load "pigl.scm")
;; This reads in the file you created earlier.
(pigl 'scheme)
;; Try out your program.<br>; Feel free to try more test cases here!
(trace pigl)
; This is a debugging aid. Watch what happens
(pigl 'scheme)
; when you run a traced procedure.
(transcript-off)
(exit)
