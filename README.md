DummyScripts
============

SRT Shifter
-----------

    $ python srt_shifter.py
    usage: srt_shifter.py [options] <time_shift> <input> <output>

    positional arguments:
      time_shift            format=(-)hh:mm:ss,mmm
      input_file
      output_file
      
    optional arguments:
      -h, --help            show this help message and exit
      -e ENCODING, --encoding ENCODING
                            encoding of input and output files
      -f STARTING_TIME, --from STARTING_TIME
                            approximated time from which the shifting must start
      -u ENDING_TIME, --until ENDING_TIME
                            approximated (non-included) time until which the
                            shifting must be done
      
    $ python srt_shifter.py -00:00:00,625 utf-16 juno_vn.srt juno_vn.new.srt
