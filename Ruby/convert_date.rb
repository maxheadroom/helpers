#!/usr/bin/ruby -w
require 'optparse' #gem install OptionParser
require 'date'

# convert one date string into another
# beyond what the Unix/Mac/Linux date command maybe able to parse
# using POSIX Date/Time formats
# http://en.wikipedia.org/wiki/Date_(Unix)


class CatArguments < Hash
  def initialize(args)
    super()
    self[:input] = "%d/%b/%y %I:%M %p"
    self[:output] = "%d.%m.%y %H:%M"
    self[:datum] = nil
    self[:delimiter] = ";"
    
    opts = OptionParser.new do |opts|
      opts.banner = "Usage: #$0 [options]"
      opts.on('-i', '--input [STRING]',
              'use [STRING] as input format') do |string|
        self[:input] = string || '$'
      end
      
      opts.on('-o', '--output [STRING]', 
            'use [STRING] as output format') do |string|
        self[:output] = string || '$'
      end
                  
      opts.on('-d', '--datum [STRING]',
            'use [STRING] as the date to convert') do |string|
            self[:datum] = string || '$'
      end
      
      opts.on('-l', '--delimiter [STRING]',
            'use [STRING] as the date to convert') do |string|
            self[:delimiter] = string || '$'
      end
      
      
      opts.on_tail('-h', '--help', 'display this help and exit') do
        puts opts
        exit
      end
    end
    opts.parse!(args)
  end
end

# parse command line arguments
arguments = CatArguments.new(ARGV)

def convert_date( inputformat, outputformat, datum )
  begin
  date = DateTime.strptime(datum, inputformat)
  
  puts date.strftime(outputformat)
rescue Exception => e
  puts "The date string: " + datum + " can't be parsed with \"" + inputformat + "\""
end
end

 
convert_date( arguments[:input], arguments[:output], arguments[:datum])