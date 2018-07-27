#!/usr/bin/env python

import sys, os
import shlex, subprocess
import re
import json
import struct

def findDOI(text):
  doi_patterns = [
    r"(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+)",
    r"(10.\d{4,9}/[-._;()/:A-Z0-9]+)",
    r"(10.\d{4}/\d+-\d+X?(\d+)\d+<[\d\w]+:[\d\w]*>\d+.\d+.\w+;\d)",
    r"(10.1021/\w\w\d+)",
    r"(10.1207/[\w\d]+\&\d+_\d+)"
  ]
  for pattern in doi_patterns:
    match = re.search(pattern,text)
    if match:
      return match.group()
  return None

def papisCommand(receivedMessage):
  if receivedMessage.startswith('papis:'):
    match = re.match(r'^papis:(.*)',receivedMessage)
    if match:
      url = match.group(1)
          
      command_pre = "gnome-terminal -- bash -c "
      command_end= ";read -p \"Press any key to close.\""

      doi = findDOI(url)
      if doi:
        command_line = "papis add --from-doi %s" % doi
      else:
        command_line = "papis add --from-url %s" % url

      statement = "echo $\"Executing command: %s\n\";" % command_line#\\\n';";#\'Executing command: \'";#"+command_line+"\';echo;echo;"

      sendMessage(encodeMessage("Papis connector executing command: %s" % command_line))
      process = subprocess.Popen(shlex.split(' '.join([command_pre,'\'',statement,command_line,command_end,'\''])))
      process.wait()

try:
    # Python 3.x version
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.buffer.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.buffer.read(messageLength).decode('utf-8')
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent).encode('utf-8')
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.buffer.write(encodedMessage['length'])
        sys.stdout.buffer.write(encodedMessage['content'])
        sys.stdout.buffer.flush()

    while True:
        receivedMessage = getMessage()
        papisCommand(receivedMessage)

except AttributeError:
    # Python 2.x version (if sys.stdin.buffer is not defined)
    # Read a message from stdin and decode it.
    def getMessage():
        rawLength = sys.stdin.read(4)
        if len(rawLength) == 0:
            sys.exit(0)
        messageLength = struct.unpack('@I', rawLength)[0]
        message = sys.stdin.read(messageLength)
        return json.loads(message)

    # Encode a message for transmission,
    # given its content.
    def encodeMessage(messageContent):
        encodedContent = json.dumps(messageContent)
        encodedLength = struct.pack('@I', len(encodedContent))
        return {'length': encodedLength, 'content': encodedContent}

    # Send an encoded message to stdout
    def sendMessage(encodedMessage):
        sys.stdout.write(encodedMessage['length'])
        sys.stdout.write(encodedMessage['content'])
        sys.stdout.flush()

    while True:
        receivedMessage = getMessage()
        papisCommand(receivedMessage)
