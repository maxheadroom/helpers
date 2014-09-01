

set this_file to (((path to home folder) as string) & "MailLog.log")


on write_to_file(this_data, target_file, append_data)
	try
		set the target_file to the target_file as string
		set the open_target_file to open for access file target_file with write permission
		if append_data is false then set eof of the open_target_file to 0
		write this_data to the open_target_file starting at eof
		close access the open_target_file
		return true
	on error
		try
			close access file target_file
		end try
		return false
	end try
end write_to_file

on replace_chars(this_text, search_string, replacement_string)
	set AppleScript's text item delimiters to the search_string
	set the item_list to every text item of this_text
	set AppleScript's text item delimiters to the replacement_string
	set this_text to the item_list as string
	set AppleScript's text item delimiters to ""
	return this_text
end replace_chars

-- This code is triggered if you manually run the script in AppleScript Editor. It retreives any selected messages and then processes them. This is good for testing.
tell application "Microsoft Outlook"
	set theMessages to current messages
	--(plain text content of (item 1 of theMessages))
	--return paragraphs of result
end tell

-- Count the messages received from Outlook.
set theMessageCount to count theMessages


-- Loop through the messages received from Outlook.
tell application "Microsoft Outlook"
	repeat with a from 1 to theMessageCount
		-- Target the current message in the loop.
		tell item a of theMessages
			-- Retrieve the name of the current message's sender.
			set theSender to sender
			
			
			try
				set theSenderName to name of theSender
				
			on error
				set theSenderName to address of theSender
			end try
			set theSenderAddress to address of theSender
			-- Retrieve the current message's subject.
			set theSubject to subject
			set timeReceived to time received
			set timeSent to time sent
			set thePriority to priority
			set theSource to source as text
			set theSize to length of theSource
			
			-- extract CC recipients
			set theCC to cc recipients
			set CCList to ""
			repeat with rcp in theCC
				set recipientEMail to email address of rcp
				set CCList to CCList & address of recipientEMail as text
				set CCList to CCList & ","
			end repeat
			
			-- extract the TO recipients
			set theTO to to recipients
			set TOList to ""
			repeat with rcp in theTO
				set recipientEMail to email address of rcp
				set TOList to TOList & address of recipientEMail as text
				set TOList to TOList & ","
			end repeat
			
			
			if thePriority = priority normal then
				set mailPriority to "normal"
			else if thePriority = priority high then
				set mailPriority to "high"
			else if thePriority = priority low then
				set mailPriority to "low"
			else
				set mailPriority to "none"
			end if
			
			
			set isMeeting to is meeting
		end tell
		
		set theSubject to my replace_chars(theSubject, "|", "--")
		set output to timeReceived & "|" & timeSent & "|" & theSenderAddress & "|" & TOList & "|" & CCList & "|" & theSubject & "|" & mailPriority & "|" & isMeeting & "|" & theSize & return
		
		my write_to_file(output as string, this_file, true)
		
	end repeat
end tell
