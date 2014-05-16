#!/usr/bin/ruby -w
require 'optparse' #gem install OptionParser
require 'date'


# using POSIX Date/Time formats
# http://en.wikipedia.org/wiki/Date_(Unix)


class CatArguments < Hash
  def initialize(args)
    super()
    self[:input] = "%d/%b/%y %I:%M %p" # 28/Aug/12 06:18 AM
    self[:output] = "%d.%m.%y %H:%M" # 28.08.12 06:18
    self[:datum] = nil
    self[:delimiter] = ";"
    self[:field] = 0
    self[:file] = nil
    
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
            'use [STRING] as the delimiter') do |string|
            self[:delimiter] = string || '$'
      end
      
      opts.on('-c', '--column [INT]', Integer, 
            'convert in field number [INT]') do |int|
            self[:field] = int || '$'
      end
      
      opts.on('-f', '--file [STRING]',
            'use [STRING] as the file') do |string|
            self[:file] = string || '$'
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
  date = DateTime.strptime(datum, inputformat)
  
  puts date.strftime(outputformat)
end

# replace string in a certain column of a delimited file
def convert_in_file(args)
  
  begin
  File.open(args[:file], "r").each_line do |line|
    fields = line.chomp.split(args[:delimiter])
    toconvert = fields[args[:field]+1] 

    begin
      indate = DateTime.strptime(toconvert, args[:input])
      outdate = indate.strftime(args[:output])
    rescue ArgumentError 
      outdate = toconvert
    end
    
    fields[args[:field]+1] = outdate
    fields.each do | field |
      print field + args[:delimiter]
    end
    print "\n"
          # puts "Before: " + toconvert + " after: " + outdate

  end
rescue   Exception => e  
    puts "Error: " + e.message  
    puts e.backtrace
    #puts "Can't open the file: " + args[:file]
end
end


convert_in_file(arguments)