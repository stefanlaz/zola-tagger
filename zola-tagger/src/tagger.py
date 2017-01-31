'''
Created on Jan 24, 2017

@author: Stefan
'''

from bitstring import BitArray
import re
import os

def loadFrameDict():
    frame_dict = {}
    frame_dict["AENC"] = "Audio Encryption"
    frame_dict["APIC"] = "Attached Picture"
    frame_dict["COMM"] = "Comments"
    frame_dict["COMR"] = "Commercial Frame"
    frame_dict["DFLT"] = "Unknown Frame ID"
    frame_dict["ENCR"] = "Encryption Method Registration"
    frame_dict["EQUA"] = "Equalization"
    frame_dict["ETCO"] = "Event Timing Codes"
    frame_dict["GEOB"] = "General Encapsulated Object"
    frame_dict["GRID"] = "Group Identification Registration"
    frame_dict["IPLS"] = "Involved People List"
    frame_dict["LINK"] = "Linked Information"
    frame_dict["MCDI"] = "Music CD Identifier"
    frame_dict["MLLT"] = "MPEG Location Lookup Table"
    frame_dict["OWNE"] = "Ownership Frame"
    frame_dict["PRIV"] = "Private Frame"
    frame_dict["PCNT"] = "Play Counter"
    frame_dict["POPM"] = "Popularimeter"
    frame_dict["POSS"] = "Position Synchronization Frame"
    frame_dict["RBUF"] = "Recommended Buffer Size"
    frame_dict["RVAD"] = "Relative Volume Adjustment"
    frame_dict["RVRB"] = "Reverb"
    frame_dict["SYLT"] = "Synchronized Lyric/Text"
    frame_dict["SYTC"] = "Synchronized Tempo Codes"
    frame_dict["TALB"] = "Album/Movie/Show Title"
    frame_dict["TBPM"] = "BPM (Beats Per Minute)"
    frame_dict["TCOM"] = "Composer"
    frame_dict["TCON"] = "Content Type"
    frame_dict["TCOP"] = "Copyright Message"
    frame_dict["TDAT"] = "Date"
    frame_dict["TDLY"] = "Playlist Delay"
    frame_dict["TENC"] = "Encoded By"
    frame_dict["TEXT"] = "Lyricist/Text Writer"
    frame_dict["TFLT"] = "File Type"
    frame_dict["TIME"] = "Time"
    frame_dict["TIT1"] = "Content Group Description"
    frame_dict["TIT2"] = "Title/Songname/Content Description"
    frame_dict["TKEY"] = "Initial Key"
    frame_dict["TLAN"] = "Language(s)"
    frame_dict["TMED"] = "Media Type"
    frame_dict["TOAL"] = "Original Album/Movie/Show Title"
    frame_dict["TOFN"] = "Original Filename"
    frame_dict["TOLY"] = "Original Lyricist(s)/Text Writer(s)"
    frame_dict["TOPE"] = "Original Artist(s)/Performer(s)"
    frame_dict["TORY"] = "Original Release Year"
    frame_dict["TOWN"] = "File Owner/License"
    frame_dict["TPE1"] = "Lead Performer(s)/Soloist(s)"
    frame_dict["TPE2"] = "Band/Orchestra/Accompaniment"
    frame_dict["TPE3"] = "Conductor/Performer Refinement"
    frame_dict["TPE4"] = "Interpreted, Remixed, or otherwise Modified By"
    frame_dict["TPOS"] = "Part of a Set"
    frame_dict["TPUB"] = "Publisher"
    frame_dict["TRCK"] = "Track Number/Position in Set"
    frame_dict["TRDA"] = "Recording Dates"
    frame_dict["TRSN"] = "Internet Radio Station Name"
    frame_dict["TRSO"] = "Internet Radio Station Owner"
    frame_dict["TSIZ"] = "Size"
    frame_dict["TSOA"] = "Album Sort Order"
    frame_dict["TSRC"] = "ISRC (International Standard Recording Code)"
    frame_dict["TSSE"] = "Software/Hardware and Settings used for Encoding"
    frame_dict["TYER"] = "Year"
    frame_dict["TXXX"] = "User Defined Text Information Frame"
    frame_dict["UFID"] = "Unique File Identifier"
    frame_dict["USER"] = "Terms of Use"
    frame_dict["USLT"] = "Unsynchronized Lyric/Text Transcription"
    frame_dict["WCOM"] = "Commercial Information"
    frame_dict["WCOP"] = "Copyright/Legal Information"
    frame_dict["WOAF"] = "Official Audio File Webpage"
    frame_dict["WOAR"] = "Official Artist/Performer Webpage"
    frame_dict["WOAS"] = "Official Audio Source Webpage"
    frame_dict["WORS"] = "Official Internet Radio Station Homepage"
    frame_dict["WPAY"] = "Payment"
    frame_dict["WPUB"] = "Publishers Official Webpage"
    frame_dict["WXXX"] = "User Defined URL Link Frame"
    
    return frame_dict

def loadGenreList():
    return ["Blues", "Classic Rock", "Country", "Dance", "Disco", "Funk", "Grunge", "Hip-Hop", "Jazz", "Metal",
            "New Age", "Oldies", "Other", "Pop", "R&B", "Rap", "Reggae", "Rock", "Techno", "Industrial", "Alternative",
            "Ska", "Death Metal", "Pranks", "Soundtrack", "Euro-Techno", "Ambient", "Trip-Hop", "Vocal", "Jazz+Funk",
            "Fusion", "Trance", "Classical", "Instrumental", "Acid", "House", "Game", "Sound Clip", "Gospel", "Noise",
            "AlternRock", "Bass", "Soul", "Punk", "Space", "Meditative", "Instrumental Pop", "Instrumental Rock",
            "Ethnic", "Gothic", "Darkwave", "Techno-Industrial", "Electronic", "Pop-Folk", "Eurodance", "Dream",
            "Southern Rock", "Comedy", "Cult", "Gangsta", "Top 40", "Christian Rap", "Pop/Funk", "Jungle", "Native American",
            "Cabaret", "New Wave", "Psychadelic", "Rave", "Showtunes", "Trailer", "Lo-Fi", "Tribal", "Acid Punk", "Acid Jazz",
            "Polka", "Retro", "Musical", "Rock & Roll", "Hard Rock", "Folk", "Folk-Rock", "National Folk", "Swing",
            "Fast Fusion", "Bebob", "Latin", "Revival", "Celtic", "Bluegrass", "Avantgarde", "Gothic Rock", "Progressive Rock",
            "Psychedelic Rock", "Symphonic Rock", "Slow Rock", "Big Band", "Chorus", "Easy Listening", "Acoustic", "Humour",
            "Speech", "Chanson", "Opera", "Chamber Music", "Sonata", "Symphony", "Booty Bass", "Primus", "Porn Groove",
            "Satire", "Slow Jam", "Club", "Tango", "Samba", "Folklore", "Ballad", "Power Ballad", "Rhythmic Soul",
            "Freestyle", "Duet", "Punk Rock", "Drum Solo", "A Capella", "Euro-House", "Dance Hall"]

def parseHeader(header_data):
    header = {}  
    if header_data[0:3] == b'ID3':
        header["version"] = "{0}.{1}".format(header_data[3], header_data[4])
        tag_flags = BitArray(header_data[5:6])
        header["unsync"] = tag_flags[0]
        header["extended_header"] = tag_flags[1]
        header["experimental"] = tag_flags[2]
        tag_size = BitArray(header_data[6:10])
        del tag_size[0::8]
        header["size"] = tag_size.int
        return header
    else:
        print('Error while parsing file: {0}'.format(header_data))
        print('File does not have a valid ID3v2 tag!')
        
def parseFrames(frame_data):
    
    frame_dict = loadFrameDict()
    genre_list = loadGenreList()
    pos = 0
    frame_list = []
    while pos < len(frame_data) - 10:
        #print(pos, len(frame_data))
        if frame_data[pos:pos+4] != b'\x00\x00\x00\x00':
            frame = {}
            frame["id"] = frame_data[pos:pos+4].decode('iso-8859-1')
            if frame["id"] in frame_dict:
                frame["desc"] = frame_dict[frame["id"]]
            else:
                frame["desc"] = frame_dict["DFLT"]
            pos += 4
            frame["size"] = int.from_bytes(frame_data[pos:pos+4], 'big')
            pos += 4
            frame_flags = BitArray(frame_data[pos:pos+2])
            frame["tag_alter_discard"] = frame_flags[0]
            frame["file_alter_discard"] = frame_flags[1]
            frame["read_only"] = frame_flags[2]
            frame["compressed"] = frame_flags[8]
            frame["encrypted"] = frame_flags[9]
            frame["group"] = frame_flags[10]
            pos += 2
            content_end = pos + frame["size"]
            if frame["id"].startswith('T'):             
                if frame_data[content_end-1:content_end] == b'\x00':
                    content_end -= 1
                if frame_data[pos:pos+1] == b'\x00':
                    frame["content"] = frame_data[pos+1:content_end].decode('iso-8859-1')
                elif frame_data[pos:pos+1] == b'\x01':
                    frame["content"] = frame_data[pos+1:content_end].decode('utf-8')
                else:
                    frame["content"] = frame_data[pos:content_end]
                if frame["id"] == 'TCON':
                    pattern = re.compile(r'\((\d+)\)')
                    genres = pattern.findall(frame["content"])
                    refinement = pattern.sub("", frame["content"])
                    if refinement == "(RX)":
                        refinement = "Remix"
                    elif refinement == "(CR)":
                        refinement = "Cover"
                    frame["content"] = ", ".join(genre_list[int(index)] for index in genres if int(index) < len(genre_list))
                    if refinement != "":
                        if frame["content"] == "":
                            frame["content"] = refinement
                        else:
                            frame["content"] += " - " + refinement 
            else:
                frame["content"] = frame_data[pos:content_end]
            pos += frame["size"]
            frame_list.append(frame)
        else:
            pos += 10
    return frame_list
               
def parseFile(file_name):
    try:
        f = open(file_name, 'rb')
        try:
            tag_header = parseHeader(f.read(10))
            tag_frames = parseFrames(f.read(tag_header["size"]))
        except (IOError, ValueError) as err:
            print('Error while reading from a file: {0}'.format(file_name))
            print(err)
        finally:
            f.close()
    except IOError as err:
        print('Error while opening file: {0}'.format(file_name))
        print(err)
        
    print(file_name)
    for frame in tag_frames:
        if frame["id"].startswith('T'):
            print("{0}: {1}".format(frame["desc"].ljust(35), frame["content"]))
    print("----------------------------------------------------------------------------------------")
        
        
if __name__ == '__main__':
    dir_name = "C:\\Users\\Stefan\\Music\\Alternative\\Red Hot Chili Peppers\\(1999) Californication"          
    for f in [os.path.join(dir_name, f) for f in os.listdir(dir_name) if os.path.splitext(f)[1] == ".mp3"]:
        parseFile(f)
        
    