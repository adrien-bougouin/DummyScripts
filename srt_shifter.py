#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import codecs
import math
import argparse

from sys import argv

################################################################################
## IO FUNCTIONS

def parse_srt_file(srt_file):
  srt = []
  current_number = None
  current_start_time = None
  current_end_time = None
  current_lines = []

  for line in srt_file.read().splitlines():
    if line == "":
      srt.append((current_number,
                  current_start_time,
                  current_end_time,
                  current_lines))
      #-------------------------------------------------------------------------
      current_number = None
      current_start_time = None
      current_end_time = None
      current_lines = []
    else:
      if current_number == None:
        current_number = line
      elif current_start_time == None and current_end_time == None:
        current_start_time = line.split(" --> ")[0]
        current_end_time = line.split(" --> ")[1]
      else:
        current_lines.append(line)

  return srt

def write_srt_file(srt, srt_file):
  for number, start_time, end_time, text_lines in srt:
    srt_file.write("%s\n"%(number))
    srt_file.write("%s --> %s\n"%(start_time, end_time))
    srt_file.write("%s\n\n"%("\n".join(text_lines)))

################################################################################
## TIME MANAGEMENT

def parse_time(time_string):
  splitped_time_string = time_string.split(":")
  hour = int(splitped_time_string[0])
  minute = int(splitped_time_string[1])
  second = int(splitped_time_string[2].split(",")[0])
  milli_second = int(splitped_time_string[2].split(",")[1])

  return hour, minute, second, milli_second

def stringify_time(hour, minute, second, milli_second):
  return "%02d:%02d:%02d,%03d"%(hour, minute, second, milli_second)

def time_string_to_float(time):
  hour, \
  minute, \
  second, \
  milli_second = parse_time(time)

  time_float = float(hour) * 3600.0 \
               + float(minute) * 60.0 \
               + float(second) \
               + float(milli_second) / 1000.0

  if time.startswith("-"):
    time_float = -time_float

  return time_float

def time_float_to_string(time_float):
  remaining_time = time_float
  hour = math.floor(remaining_time / 3600.0)
  remaining_time = remaining_time - (hour * 3600.0)
  minute = math.floor(remaining_time / 60.0)
  remaining_time = remaining_time - (minute * 60.0)
  second = math.floor(remaining_time)
  remaining_time = remaining_time - second
  milli_second = math.floor(remaining_time * 1000.0)

  return stringify_time(hour, minute, second, milli_second)

def time_shifting(time, time_shift):
  time_float = time_string_to_float(time)
  shift_float = time_string_to_float(time_shift)
  shifted_time = time_float + shift_float

  return time_float_to_string(shifted_time)

################################################################################
## SRT SHIFTING

def shift_subtitles(srt, time_shift):
  shifted_srt = []

  for number, start_time, end_time, text_lines in srt:
    start_time = time_shifting(start_time, time_shift)
    end_time = time_shifting(end_time, time_shift)

    shifted_srt.append((number,
                        start_time,
                        end_time,
                        text_lines))

  return shifted_srt

################################################################################
## MAIN

def main(argv):
  positional_arguments = ["(+|-)<time_shift>", "<input>", "<output>"]
  arg_parser = argparse.ArgumentParser(description="Shifts the subtitle time frames of %s with %s and write the result in %s."%(
                                                     positional_arguments[0],
                                                     positional_arguments[1],
                                                     positional_arguments[2],
                                                   ),
                                       usage="Usage: %s [options] %s %s %s"%(
                                               argv[0],
                                               positional_arguments[0],
                                               positional_arguments[1],
                                               positional_arguments[2],
                                             ))
  #-----------------------------------------------------------------------------
  arg_parser.add_argument("-e",
                          "--encoding",
                          dest="encoding",
                          default="utf-8",
                          help="The file encoding of input and output files.")
  arg_parser.add_argument("time_shift",
                          default="-00:00:00,000",
                          help="The value to shift time frames.")
  arg_parser.add_argument("input_file",
                          help="The file containing the original subtitle time frames.")
  arg_parser.add_argument("output_file",
                          help="The file containing the modified subtitle time frames.")

  if len(argv) < 4:
    arg_parser.print_help
  else:
    arguments = arg_parser.parse_args(args=argv[1:-3] + ["--"] + argv[-3:])
  
    time_shift = arguments.time_shift
    encoding = arguments.encoding
    input_filepath = arguments.input_file
    output_filepath = arguments.output_file
    #---------------------------------------------------------------------------
    input_file = codecs.open(input_filepath, "r", encoding)
    output_file = codecs.open(output_filepath, "w", encoding)
    #---------------------------------------------------------------------------
    srt = parse_srt_file(input_file)
    shifted_srt = shift_subtitles(srt, time_shift)
    
    write_srt_file(shifted_srt, output_file)
    
    input_file.close()
    output_file.close()

if __name__ == "__main__":
  main(argv)

