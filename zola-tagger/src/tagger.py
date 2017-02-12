'''
Created on Jan 24, 2017

@author: Stefan

Contains the basics of MP3 file tag manipulation.

'''

from bitstring import BitArray
import re
import os

class HeaderError(Exception):
    '''Thrown if the file header is not a valid ID3v2 tag.'''
    pass

def loadFrameDict():
    '''Populates the dictionary of ID3v2.0 frame IDs, their meanings and sorting order.'''
    frame_dict = {}
    frame_dict["AENC"] = ("Audio Encryption", 100)
    frame_dict["APIC"] = ("Attached Picture", 10)
    frame_dict["COMM"] = ("Comments", 38)
    frame_dict["COMR"] = ("Commercial Frame", 101)
    frame_dict["DFLT"] = ("Unknown Frame ID", 999)
    frame_dict["ENCR"] = ("Encryption Method Registration", 102)
    frame_dict["EQUA"] = ("Equalization", 102)
    frame_dict["ETCO"] = ("Event Timing Codes", 103)
    frame_dict["GEOB"] = ("General Encapsulated Object", 104)
    frame_dict["GRID"] = ("Group Identification Registration", 105)
    frame_dict["IPLS"] = ("Involved People List", 106)
    frame_dict["LINK"] = ("Linked Information", 107)
    frame_dict["MCDI"] = ("Music CD Identifier", 108)
    frame_dict["MLLT"] = ("MPEG Location Lookup Table", 109)
    frame_dict["OWNE"] = ("Ownership Frame", 110)
    frame_dict["PRIV"] = ("Private Frame", 111)
    frame_dict["PCNT"] = ("Play Counter", 112)
    frame_dict["POPM"] = ("Popularimeter", 113)
    frame_dict["POSS"] = ("Position Synchronization Frame", 114)
    frame_dict["RBUF"] = ("Recommended Buffer Size", 115)
    frame_dict["RVAD"] = ("Relative Volume Adjustment", 116)
    frame_dict["RVRB"] = ("Reverb", 117)
    frame_dict["SYLT"] = ("Synchronized Lyric/Text", 118)
    frame_dict["SYTC"] = ("Synchronized Tempo Codes", 119)
    frame_dict["TALB"] = ("Album/Movie/Show Title", 3)
    frame_dict["TBPM"] = ("BPM (Beats Per Minute)", 16)
    frame_dict["TCOM"] = ("Composer", 7)
    frame_dict["TCON"] = ("Content Type", 6)
    frame_dict["TCOP"] = ("Copyright Message", 20)
    frame_dict["TDAT"] = ("Date", 17)
    frame_dict["TDLY"] = ("Playlist Delay", 19)
    frame_dict["TENC"] = ("Encoded By", 14)
    frame_dict["TEXT"] = ("Lyricist/Text Writer", 13)
    frame_dict["TFLT"] = ("File Type", 11)
    frame_dict["TIME"] = ("Time", 18)
    frame_dict["TIT1"] = ("Content Group Description", 21)
    frame_dict["TIT2"] = ("Title/Songname/Content Description", 0)
    frame_dict["TKEY"] = ("Initial Key", 22)
    frame_dict["TLAN"] = ("Language(s)", 23)
    frame_dict["TMED"] = ("Media Type", 12)
    frame_dict["TOAL"] = ("Original Album/Movie/Show Title", 24)
    frame_dict["TOFN"] = ("Original Filename", 25)
    frame_dict["TOLY"] = ("Original Lyricist(s)/Text Writer(s)", 26)
    frame_dict["TOPE"] = ("Original Artist(s)/Performer(s)", 27)
    frame_dict["TORY"] = ("Original Release Year", 28)
    frame_dict["TOWN"] = ("File Owner/License", 29)
    frame_dict["TPE1"] = ("Lead Performer(s)/Soloist(s)", 2)
    frame_dict["TPE2"] = ("Band/Orchestra/Accompaniment", 1)
    frame_dict["TPE3"] = ("Conductor/Performer Refinement", 30)
    frame_dict["TPE4"] = ("Interpreted, Remixed, or otherwise Modified By", 31)
    frame_dict["TPOS"] = ("Part of a Set", 8)
    frame_dict["TPUB"] = ("Publisher", 32)
    frame_dict["TRCK"] = ("Track Number/Position in Set", 4)
    frame_dict["TRDA"] = ("Recording Dates", 33)
    frame_dict["TRSN"] = ("Internet Radio Station Name", 34)
    frame_dict["TRSO"] = ("Internet Radio Station Owner", 35)
    frame_dict["TSIZ"] = ("Size", 36)
    frame_dict["TSOA"] = ("Album Sort Order", 9)
    frame_dict["TSRC"] = ("ISRC (International Standard Recording Code)", 37)
    frame_dict["TSSE"] = ("Software/Hardware and Settings used for Encoding", 15)
    frame_dict["TYER"] = ("Year", 5)
    frame_dict["TXXX"] = ("User Defined Text Information Frame", 39)
    frame_dict["UFID"] = ("Unique File Identifier", 40)
    frame_dict["USER"] = ("Terms of Use", 200)
    frame_dict["USLT"] = ("Unsynchronized Lyric/Text Transcription", 201)
    frame_dict["WCOM"] = ("Commercial Information", 202)
    frame_dict["WCOP"] = ("Copyright/Legal Information", 203)
    frame_dict["WOAF"] = ("Official Audio File Webpage", 204)
    frame_dict["WOAR"] = ("Official Artist/Performer Webpage", 205)
    frame_dict["WOAS"] = ("Official Audio Source Webpage", 206)
    frame_dict["WORS"] = ("Official Internet Radio Station Homepage", 207)
    frame_dict["WPAY"] = ("Payment", 208)
    frame_dict["WPUB"] = ("Publishers Official Webpage", 209)
    frame_dict["WXXX"] = ("User Defined URL Link Frame", 210)
    
    return frame_dict

def loadGenreList():
    '''Populates the list of genres defined by the ID3v2.0 standard. Genres added by Winamp included.'''
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
        raise HeaderError("File does not have a valid ID3v2 tag!")
        
def parseFrames(frame_data):
    
    frame_dict = loadFrameDict()
    genre_list = loadGenreList()
    pos = 0
    frame_list = []
    while pos < len(frame_data) - 10:
        if frame_data[pos:pos+4] != b'\x00\x00\x00\x00':
            frame = {}
            frame["id"] = frame_data[pos:pos+4].decode('iso-8859-1')
            if frame["id"] in frame_dict:
                frame["desc"], frame["sort"] = frame_dict[frame["id"]]
            else:
                frame["desc"], frame["sort"] = frame_dict["DFLT"]
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
            if frame["id"].startswith('T'):    #textual frame         
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
            elif frame["id"] == 'APIC':     #attached picture
                start = pos     #keeping pos safe and sound...
                if frame_data[start:start+1] == b'\x01':
                    encoding = 'utf-8'
                else:
                    encoding = 'iso-8859-1'
                start += 1
                end = start + 1
                while frame_data[end-1:end] != b'\x00':     #getting MIME type
                    end += 1
                frame["image_file_type"] = frame_data[start:end-1].decode('iso-8859-1').replace("image/", "")
                start = end + 1   #skipping picture type, because who cares ;-)
                end = start + 1
                while frame_data[end-1:end] != b'\x00':     #getting picture description
                    end += 1
                frame["picture_desc"] = frame_data[start:end-1].decode(encoding)
                start = end
                frame["content"] = frame_data[start:content_end]
            else:
                frame["content"] = frame_data[pos:content_end]
            pos += frame["size"]
            frame_list.append(frame)
        else:
            pos += 10
    return sorted(frame_list, key=lambda frame: frame["sort"])
               
def parseFile(file_name):
    try:
        f = open(file_name, 'rb')
        try:
            tag_header = parseHeader(f.read(10))
            tag_frames = parseFrames(f.read(tag_header["size"]))
        except HeaderError as err:
            raise err
        except (IOError, ValueError) as err:
            print('Error while reading from a file: {0}'.format(file_name))
            print(err)
            raise err
        finally:
            f.close()
    except IOError as err:
        print('Error while opening file: {0}'.format(file_name))
        print(err)
        raise err
        
    print(file_name)
    for frame in tag_frames:
        if frame["id"].startswith('T'):
            print("{0}: {1}".format(frame["desc"].ljust(35), frame["content"]))
        #=======================================================================
        # elif frame["id"] == 'APIC':
        #     print("{0}: {1}: {2}".format(frame["desc"].ljust(35), frame["image_file_type"], frame["picture_desc"]))
        #=======================================================================
    print("----------------------------------------------------------------------------------------")
    return tag_frames
        
        
if __name__ == '__main__':
    dir_name = "C:\\Users\\Stefan\\Music\\Alternative\\Red Hot Chili Peppers\\(1999) Californication"          
    for f in [os.path.join(dir_name, f) for f in os.listdir(dir_name) if os.path.splitext(f)[1] == ".mp3"]:
        parseFile(f)
        
    