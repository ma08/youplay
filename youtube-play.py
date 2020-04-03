#!/home/ma08/pro/repos/youplay/youvenv/bin/python
import datetime
from urlparse import parse_qs
from urlparse import urlparse
import re
import unicodedata
#install https://developers.google.com/api-client-library/python/ , youtube-dl and mplayer
import sys
import isodate
sys.path.append("/home/ma08/pro/repos/youplay/curses-menu-0.5.0/")

# Import the necessary packages
from cursesmenu import *
from cursesmenu.items import *

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os
import time
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDX3LlP3uSmZ0jwQXkVOr7tdmw-RQTJ0-4"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
import subprocess

import concurrent.futures
from urllib import urlretrieve  # Python 2

catname = 'amateur'

temp_folder='/tmp/'
import imgbackground

import curses
import curses.textpad

def textbox_demo(stdscr):

    # stdscr = curses.initscr()
    # don't echo key strokes on the screen
    # curses.noecho()
    # read keystrokes instantly, without waiting for enter to ne pressed
    # curses.cbreak()
    # enable keypad mode
    # stdscr.keypad(1)
    # stdscr.clear()
    # stdscr.refresh()
    win = curses.newwin(1, 60, stdscr.getmaxyx()[0]-1, 0)
    # win.addstr(0,10,"Enter Search: ")
    win.addstr(0,0,"Search String:")
    win.refresh()
    # stdscr.refresh()
    text_win = curses.newwin(1, 60, stdscr.getmaxyx()[0]-1, len("Search String")+1)
    win.border()
    text_win.box()
    tb = curses.textpad.Textbox(text_win)
    text_win.refresh()
    tb.do_command(11) #CTRL-K ASCII
    # f1=open('./testfile', 'w+')
    # print >> f1, tb.gather() 
    text = tb.edit()
    f1=open('./testfile', 'w+')
    print >> f1, tb.gather() 
    text_win.refresh()
    # text_win.getch()

    # print >> f1, tb.gather() 
    # print >> f1, text 
    # print >> f1, "   ----       " 
    # print text
    # curses.beep()
    # win.addstr(0,10,"Enter Search: ")

def demo_menu():
    # Create the menu
    menu = CursesMenu("Title", "Subtitle")

    # Create some items

    # MenuItem is the base class for all items, it doesn't do anything when selected
    menu_item = MenuItem("Menu Item")

    # A FunctionItem runs a Python function when selected
    function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

    # A CommandItem runs a console command
    command_item = CommandItem("Run a console command",  "touch hello.txt")

    # A SelectionMenu constructs a menu from a list of strings
    selection_menu = SelectionMenu(["item1", "item2", "item3"])

    # A SubmenuItem lets you add a menu (the selection_menu above, for example)
    # as a submenu of another menu
    submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

    # Once we're done creating them, we just add the items to the menu
    menu.append_item(menu_item)
    menu.append_item(function_item)
    menu.append_item(command_item)
    menu.append_item(submenu_item)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()

def paste(str, p=True, c=True):
    print "ffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    #exit()
    from subprocess import Popen, PIPE

    if p:
        p = Popen(['xsel', '-pi'], stdin=PIPE)
        p.communicate(input=str)
    if c:
        p = Popen(['xsel', '-bi'], stdin=PIPE)
        p.communicate(input=str)

# paste('Hello', False)    # pastes to CLIPBOARD only
# paste('Hello', c=False)  # pastes to PRIMARY only
# paste('Hello')           # pastes to both

def process_input(user_input,results,menu):
    index = menu.current_option
    if user_input == ord('i') and index!=len(results):
        if not "formats" in results[index]:
            format_lines=get_format_info(results[index]["url"])
            results[index]["formats"]=format_lines
        format_index = SelectionMenu.get_selection(results[index]["formats"],"Select format")
        if(format_index>=0 and format_index<len(results[index]["formats"])):
            selected_format=results[index]["formats"][format_index].split()[0]
            print results[index]
            play_video(results[index]["url"],video_format=selected_format,open_terminal=True,video_name=results[index][u'snippet']['title'])
            menu.show()
        else:
            menu.show()
    elif user_input == ord('y') and index!=len(results):
        paste(results[index]["url"], False)    # pastes to CLIPBOARD only
    elif user_input == ord('o'):
        os.chdir('/home/ma08/pro/repos/youplay/downloads')
        print "aaaaaaaaaaaaaa", len(results),index
        os.system("urxvt -cd /home/ma08/pro/repos/youplay/downloads -e sh -c 'youtube-dl '"+results[index]["url"])




    # menu.resume()



def process_query(menu,query):

    args=argparser.parse_args(['--q',query])
    results, urls,thumbnails = youtube_search(args)
    get_thumbnails(thumbnails)

    for result in results:
        # print result
        url = result["url"]
        f1=open('./testfile', 'w+')
        print >> f1, result 
        print >> f1, url 
        print >> f1, "   ============       " 


        title=result["snippet"]["title"].encode('utf8')
        duration=result["duration"].encode('utf8')
        description=result["snippet"]["description"].encode('utf8')
        thumbnail_medium=result["snippet"]["thumbnails"]["medium"]["url"]

        function_item = FunctionItem(title +"   "+duration , play_video, [url,title])
        menu.append_item(function_item)

    menu.event_change_args[0]=results #updating for thumbnails
    menu.clear_screen()
    menu.draw()

    # show_menu(results)


def show_menu(results):
    try:
        print "shooooooooooooooow meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeenu"
        image_displayer=imgbackground.URXVTImageDisplayer()
        if(results==[]):
            print "goo"
            event_args=[results,image_displayer]
            process_input_args=[results]
            menu = CursesMenu("Title", "Subtitle",event_change_run=draw_current_thumbnail,event_change_args=event_args,input_run=process_input,input_run_args=process_input_args,process_query=process_query)
            process_input_args.append(menu)
            event_args.append(menu)
            menu.show()
            menu_item = MenuItem("Menu Item")
            function_items = []
            print "boo"
            menu.show()
            print "foo"
            exit()

        print "here"
        # Create the menu
        event_args=[results,image_displayer]
        process_input_args=[results]
        menu = CursesMenu("Title", "Subtitle",event_change_run=draw_current_thumbnail,event_change_args=event_args,input_run=process_input,input_run_args=process_input_args,process_query=process_query)
        event_args.append(menu)
        process_input_args.append(menu)

        # Create some items

        # MenuItem is the base class for all items, it doesn't do anything when selected
        menu_item = MenuItem("Menu Item")

        function_items = []

        for result in results:
            # print result
            url = result["url"]
            title=result["snippet"]["title"].encode('utf8')
            duration=result["duration"].encode('utf8')
            description=result["snippet"]["description"].encode('utf8')
            thumbnail_medium=result["snippet"]["thumbnails"]["medium"]["url"]

            function_item = FunctionItem(title +"   "+duration , play_video, [url, title])
            menu.append_item(function_item)
        menu.show()

    except Exception as e:
      print("An exception occurred") 
      print e

def draw_current_thumbnail(results,image_displayer,menu):
    #TODO eror here when results = []
    #possibly due to 0 results
    if(results==[]):
        return

    
    if(menu.current_option==len(menu.items)-1 or len(menu.items)==1):
        image_displayer.clear(0,0,320,180)
        return
    ind = menu.current_option
    result=results[ind]
    video_id=result["id"]["videoId"]
    thumbnail_path=get_thumbnail_local_path(video_id)
    if os.path.isfile(thumbnail_path):
        image_displayer.draw(thumbnail_path,100,100,320,180)
    else:
        image_displayer.clear(0,0,320,180)
    # f1=open('./testfile', 'w+')
    # print >> f1, "all fine"
    

def getimg(thumbnail):
    url=thumbnail['url']
    id=thumbnail['id']
    localpath = '{0}{1}.jpg'.format(temp_folder, id)
    if not os.path.isfile(localpath):
        # print localpath
        urlretrieve(url, localpath)


def get_thumbnails(thumbnails):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        for thumbnail in thumbnails:
            e.submit(getimg, thumbnail)

def get_thumbnail_local_path(id):
    return '{0}{1}.jpg'.format(temp_folder, id)


def draw_thumbnails(thumbnails,start_x=1037,start_y=0):
    size_x=320
    size_y=140
    for thumbnail in thumbnails:
        localpath=get_thumbnail_local_path(thumbnail["id"])
        command = "/home/sourya/pro/bakchodhi/imgdisplay.sh {0} {1} {2} {3} {4}".format(localpath,start_x,start_y,size_x,size_y)
        # print command
        os.system(command)
        start_y+=size_y

def get_format_info(url):
    # p = subprocess.Popen(["youtube-dl","--verbose","-F",url], stdout=subprocess.PIPE)
    p = subprocess.Popen(["youtube-dl","-F",url], stdout=subprocess.PIPE)
    out = p.stdout.read()
    p.kill()
    #TODO how to check if run smoothly
    lines = out.split("\n")
    if(lines[-1]==""):
        lines=lines[:-1]
    #TODO check if this can be hardcoded
    start_index=0
    for i,line in enumerate(lines):
        if(line[:6]=="format"):
            start_index=i+1
    lines = lines[start_index:]
    # for line in lines:
    #     print line
    return lines




YOUTUBE_DOMAINS = [
    'youtu.be',
    'youtube.com',
]


def get_id(url_string):
    # Make sure all URLs start with a valid scheme
    if not url_string.lower().startswith('http'):
        url_string = 'http://%s' % url_string

    url = urlparse(url_string)

    # Check host against whitelist of domains
    if url.hostname.replace('www.', '') not in YOUTUBE_DOMAINS:
        return None

    # Video ID is usually to be found in 'v' query string
    qs = parse_qs(url.query)
    if 'v' in qs:
        return qs['v'][0]

    # Otherwise fall back to path component
    return url.path.lstrip('/')

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def play_video(url,video_name="not set",video_format=None,open_terminal=True):
    # print(url)
    #p = subprocess.Popen(["youtube-dl","-F",url], stdout=subprocess.PIPE)
    #out = p.stdout.read()
    #print out
    #x=raw_input()
    #os.system("urxvt -e sh -c 'youtube-dl -f %s -q -o- %s | mplayer -cache 8192 -' &"%(x,url))
    # os.system("youtube-dl -f 18 -q -o- %s | mpv --cache=512 --force-seekable=yes -"%(url))
    print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
    print video_name
    video_name2=video_name.replace(' ','_')
    video_name2=video_name2.replace('(','_')
    video_name2=video_name2.replace(')','_')
    print video_name2
    print "noooooooooooooosssssssssssssssssssssssssssssssssssssssssseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    if(video_name2=="not_set"):
        print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
        #r = re.compile('(?:(?:https?\:\/\/)?(?:www\.)?(?:youtube|youtu)(?:(?:\.com|\.be)\/)(?:embed\/)?(?:watch\?)?(?:feature=player_embedded)?&?(?:v=)?([0-z]{11}|[0-z]{4}(?:\-|\_)[0-z]{4}|.(?:\-|\_)[0-z]{9}))')
        #print r.match(url)
        print video_id(url)
        #video_name2=r.match(url)
        #print video_name2
    video_name2=video_name2[:28]
        #sleep()
        #video_name = query["v"][0]
    #video_name=unicodedata.normalize('NFKD', video_name).encode('ascii','ignore')
    #video_name='/home/ma08/pro/repos/youplay/downloads/'+str(datetime.datetime.now())
    #vidoe_name=video_name[:10]
    #print(type(video_name)),"naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaame", video_name
    os.chdir('/home/ma08/pro/repos/youplay/downloads')
    #video_name="foobar"
    if not video_format is None and open_terminal:
        os.system("urxvt -cd /home/ma08/pro/repos/youplay/downloads-e sh -c 'youtube-dl -f %s -q -o- %s | mpv --record-file=%s_video.ts --cache=auto --force-seekable=yes -' > debug.out 2> debug.out &"%(video_format,url,video_name2))
    elif open_terminal:
        os.system("urxvt -cd /home/ma08/pro/repos/youplay/downloads --hold -e sh -c 'youtube-dl  -q -o- %s | mpv --record-file=%s_video.ts --cache=auto --force-seekable=yes -' > debug.out 2> debug.out &"%(url,video_name2))
    else:
        os.system("youtube-dl  -q -o- %s | mpv  --record-file=%s_video.ts --cache=auto --force-seekable=yes -"%(url,video_name2))
    # os.system("youtube-dl  -q -o  %s | mpv --cache=512 --force-seekable=yes -"%(url))
    # os.system("youtube-dl -f 18 -q -o- %s | mplayer -vo caca  -"%(url))
    #os.system("youtube-dl -f 18 -q -o- %s | mplayer -cache 8192 - &"%(url))


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified
    # query term.
    # print(options.q)

    # f1=open('./testfile', 'w+')
    # print >> f1, options.q 
    search_response = youtube.search().list(
            q=options.q,
            type="video",
            safeSearch="none",
            #location=options.location,
            #locationRadius=options.location_radius,
            part="id,snippet",
            maxResults=options.max_results
            ).execute()
    urls=[]
    thumbnails=[]
    ids=[]
    results = search_response.get("items", [])

    for search_result in results:
        # print search_result
        thumbnails.append(search_result["snippet"]["thumbnails"]["medium"])
        thumbnails[-1]["id"]=search_result["id"]["videoId"]
        ids.append(search_result["id"]["videoId"])
        #TODO figure out http or https
        # url="https://youtube.com/v/"+search_result["id"]["videoId"]
        url="http://youtube.com/v/"+search_result["id"]["videoId"]
        urls.append(url)
        search_result["url"]=url
    # print ids
    # return

    content_response = youtube.videos().list(
            # q=options.q,
            # type="video",
            id=",".join(ids),
            # safeSearch="none",
            #location=options.location,
            #locationRadius=options.location_radius,
            part="contentDetails",
            maxResults=options.max_results
            ).execute()

    content_results = content_response.get("items", [])
    for i,content_result in enumerate(content_results):
        results[i]["duration"]=isodate.parse_duration(content_result['contentDetails']['duration']).__str__()
        if(results[i]["duration"][:2]=="0:"):
            results[i]["duration"] = results[i]["duration"][2:]
        # print results[i]


    # print content_results[0]


    return results, urls, thumbnails

if __name__ == "__main__":
    # get_format_info("https://www.youtube.com/v/mA1LQRBA6es")
    # exit()

    argparser.add_argument("--l", help="Lucky")
    argparser.add_argument("--q", help="Search term")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    print "e"
    print type(args)
    print dir(args)
    print args
    print type(args.q)
    print "grrrrrrrrr;w"
    if(args.q is None and args.l is None): #empty
        results = [{u'kind': u'youtube#searchResult', 'url': u'http://youtube.com/v/LRP8d7hhpoQ', u'snippet': {u'thumbnails': {u'default': {u'url': u'https://i.ytimg.com/vi/LRP8d7hhpoQ/default.jpg', u'width': 120, u'height': 90}, u'high': {u'url': u'https://i.ytimg.com/vi/LRP8d7hhpoQ/hqdefault.jpg', u'width': 480, u'height': 360}, u'medium': {u'url': u'https://i.ytimg.com/vi/LRP8d7hhpoQ/mqdefault.jpg', u'width': 320, 'id': u'LRP8d7hhpoQ', u'height': 180}}, u'title': u'[OFFICIAL VIDEO] Hallelujah - Pentatonix', u'channelId': u'UCmv1CLT6ZcFdTJMHxaR9XeA', u'publishedAt': u'2016-10-21T13:58:56.000Z', u'liveBroadcastContent': u'none', u'channelTitle': u'PTXofficial', u'description': u"NEW ALBUM 'THE BEST OF PENTATONIX CHRISTMAS' OUT NOW! BUY: https://smarturl.it/bestofPTXmas?IQid=yt STREAM: https://smarturl.it/bestofPTXmas?"}, u'etag': u'"Fznwjl6JEQdo1MGvHOGaz_YanRU/g6GiKsrBbph87ppcgVwd92XKiFQ"', 'duration': '05:06', u'id': {u'kind': u'youtube#video', u'videoId': u'LRP8d7hhpoQ'}}]
        show_menu(results)
    elif(args.q is not None and len(args.q.split())==1 and args.q.find("http")!=-1): #url as input
        print(args.q)
        play_video(args.q)
    else:
        try:
            if(args.l is None): #not i am lucky
                results, urls,thumbnails = youtube_search(args)
                get_thumbnails(thumbnails)
                show_menu(results)
            else: #i am lucky
                args.q=args.l
                results, urls,thumbnails = youtube_search(args)
                print(len(urls),"leeeeeeeee")
                print "ggggggggg", args.q,args.l
                print urls
                print results[0]
                print type(results[0])
                play_video(urls[0],video_name=results[0][u'snippet'][u'title'])
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
