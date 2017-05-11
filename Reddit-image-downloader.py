import cookielib
import urllib
import urllib2
import re
import webbrowser
from bs4 import BeautifulSoup
import Tkinter

username = ''
password = ''
auto_open_text = ''
auto_open_links = ''
get_hot = ''
get_week = ''
get_month = ''
get_all = ''
txt_subreddits = ''
top_subreddits = [
    'gonewild',
    'nsfw',
    'RealGirls',
    'NSFW_GIF',
    'holdthemoan',
    'nsfw_gifs',
    'BustyPetite',
    'Amateur',
    'ass',
    'boobies',
    'milf',
    'GirlsFinishingTheJob',
    'OnOff',
    'LegalTeens',
    'rule34',
    '60fpsporn',
    'girlsinyogapants',
    'gonewildcurvy',
    'dirtysmall',
    'nsfwhardcore',
    'homemadexxx',
    'pornvids',
    'ginger',
    'asstastic',
    'Blowjobs',
    'porninfifteenseconds',
    'curvy',
    'GWCouples',
    'palegirls',
    'TittyDrop',
    'hentai',
    'thick',
    'O_Faces',
    'pussy',
    'datgap',
    'facedownassup',
    'pawg',
    'NSFW_HTML5',
    'lesbians',
    'Unashamed',
    'burstingout',
    'nsfw2',
    'HighResNSFW',
    'hugeboobs',
    'rearpussy',
    'porn_gifs',
    'Upskirt',
    'Bondage',
    'adorableporn',
    'porn',
    'BigBoobsGW',
    'bdsm'
]

my_subreddits = [
    'ADD',
    'YOUR',
    'FAVORITE',
    'SUBREDDITS',
    'HERE'
]

def login_to_reddit():
    print "Logging in to Reddit...",
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'RedditTesting')]
    urllib2.install_opener(opener)
    authentication_url = 'https://ssl.reddit.com/post/login'

    global username
    global password

    payload = {
      'op': 'login-main',
      'user': username.get(),
      'passwd': password.get()
    }

    data = urllib.urlencode(payload)
    req = urllib2.Request(authentication_url, data)
    resp = urllib2.urlopen(req)
    if "incorrect username or password" in resp.read():
        print "incorrect username or password"
        return False

    print "done!"
    return True

def build_link_from_subreddits(subreddits, level = "hot"):
    link = "https://reddit.com/r/"
    
    for subreddit in subreddits:
        link = link + subreddit + "+"
    link = link[:-1]
    
    if level == "top-week":
        link = link + "/top/?sort=top&t=week"
    elif level == "top-month":
        link = link + "/top/?sort=top&t=month"
    elif level == "top-all":
        link = link + "/top/?sort=top&t=all"
    
    return link

def download_reddit_pages(link, pages = 1):
    good_extensions = [ '.jpg', '.png', '.webm', '.gif', '.mp4', '.jpeg' ]
    
    print "Loading " + link + "...",
    response = urllib2.urlopen(link)
    contents = response.read()
    print "Done!"

    print "Reading... ",
    soup = BeautifulSoup(contents, 'html.parser')
    things = soup.findAll('div', attrs={'class':'thing'})
    print str(len(things)) + " links found!"
    
    for thing in things:
        links = thing.findAll('a', attrs={'class':'title'})
        if len(links) > 0:
            link = links[0]
            print "\nLINK [" + str(things.index(thing)+1) + "/" + str(len(things)) + "]",
            
            if '.gifv' in link['href']:
                print "File:",
                download_file(link['href'].replace('gifv','mp4'))
            elif any(ext in link['href'] for ext in good_extensions):
                print "File:",
                download_file(link['href'])
            elif 'gfycat' in link['href']:
                print "Gfycat:", link['href']
                download_gfycat_link(link['href'])
            elif 'imgur' in link['href']:
                print "Imgur:", link['href']
                download_imgur_media(link['href'])
            elif '/comments/' in link['href']:
                if 'self' not in thing['class']:
                    print "Reddit: https://www.reddit.com" + link['href']
                    download_reddit_media("https://www.reddit.com" + link['href'])
                else:
                    print "Text post: https://www.reddit.com" + link['href']
                    if (auto_open_text.get()):
                        print "Auto-opening..."
                        webbrowser.open(link['href'], new=2, autoraise=False)
            else:
                print "UNHANDLED: " + link['href']
                if (auto_open_links.get()):
                    print "Auto-opening..."
                    webbrowser.open(link['href'], new=2, autoraise=False)
   
    remaining_pages = pages - 1
    print "\nDONE! " + str(remaining_pages) + " PAGES LEFT...\n"

    if pages > 1:
        new_link = soup.findAll('a',attrs={'rel':'next'})[0]['href']
        download_reddit_pages(new_link, remaining_pages)
    

def download_reddit_media(link):
    response = urllib2.urlopen(link)
    contents = response.read()
    soup = BeautifulSoup(contents, 'html.parser')

    # Look for image
    if soup is not None:
        imglink = soup.findAll('a', attrs={'class':'title'})
        if len(imglink) > 0:
            print "\t",
            download_file(imglink[0]['href'])
    

def download_imgur_media(link):
    try:
        response = urllib2.urlopen(link)
    except:
        print "Imgur returned 404!"
        return
    
    contents = response.read()
    soup = BeautifulSoup(contents, 'html.parser')

    # First try to download as imgur 'album'
    imglinks = soup.findAll('a',attrs={'class':'zoom'})    
    if len(imglinks) > 0:
        if len(imglinks) >= 10:
            print "\tNOTE: There may be more images as this is an album!"
            
        for imglink in imglinks:
            print "\t" + str(imglinks.index(imglink)+1) + "/" + str(len(imglinks)) + ": ",
            download_file('https:' + imglink['href'])
    else:
        # It could be a single-image page
        imglinks = soup.findAll('link', attrs={'rel':'image_src'})
        if len(imglinks) > 0:
            for imglink in imglinks:
                print "\t" + str(imglinks.index(imglink)+1) + "/" + str(len(imglinks)) + ": ",
                download_file(imglink['href'])
        else:
            # It could be an mp4/webm
            imglinks = soup.findAll('meta',attrs={'itemprop':'contentURL'})
            if len(imglinks) != 0:
                for imglink in imglinks:
                    print "\t" + str(imglinks.index(imglink)+1) + "/" + str(len(imglinks)) + ": ",
                    download_file(imglink['content'])
            else:
                print "Could not understand IMGUR page " + link

def download_gfycat_link(link):
    json_link = link.replace('gfycat.com', 'gfycat.com/cajax/get')
    
    try:
        response = urllib2.urlopen(json_link)
    except:
        print "Gfycat returned 404!"
        return
    
    response = urllib2.urlopen(json_link)
    contents = response.read()
    webm_links = re.findall('mp4Url\"\:\"(https?:.*?\.mp4)', contents)
    if len(webm_links) > 0:
        webm_links[0] = webm_links[0].replace('\/', '/')
        download_file(webm_links[0])
    else:
        print "COULDN'T"

def download_file(link):
    print link
    
    if '?' in link:
        cutoff = link.index('?')
        link = link[:cutoff]
        
    f = open(link.split('/')[-1],'wb')
    f.write(urllib.urlopen(link).read())
    f.close()

def gui_start_download():
    if login_to_reddit() == False:
        return
    
    global num_hot
    global num_week
    global num_month
    global num_all
    global txt_subreddits

    all_text = txt_subreddits.get('1.0', 'end-1c')
    subreddits = all_text.splitlines()

    if int(num_hot.get()) > 0:
        link = reddit_page = build_link_from_subreddits(subreddits, "hot")
        download_reddit_pages(link, int(num_hot.get()))

    if int(num_week.get()) > 0:
        link = reddit_page = build_link_from_subreddits(subreddits, "top-week")
        download_reddit_pages(link, int(num_week.get()))

    if int(num_month.get()) > 0:
        link = reddit_page = build_link_from_subreddits(subreddits, "top-month")
        download_reddit_pages(link, int(num_month.get()))

    if int(num_all.get()) > 0:
        link = reddit_page = build_link_from_subreddits(subreddits, "top-all")
        download_reddit_pages(link, int(num_all.get()))

def fill_subs(subs):
    txt_subreddits.delete(1.0, Tkinter.END)
    for subreddit in subs:
        txt_subreddits.insert(Tkinter.END, subreddit + "\n")

def build_options_window():
    root = Tkinter.Tk()

    global num_hot
    global num_week
    global num_month
    global num_all
    global txt_subreddits
    global auto_open_links
    global auto_open_text
    
    global top_subreddits
    global my_subreddits
    global username
    global password

    num_hot = Tkinter.StringVar()
    num_week = Tkinter.StringVar()
    num_month = Tkinter.StringVar()
    num_all = Tkinter.StringVar()
    auto_open_links = Tkinter.BooleanVar()
    auto_open_text = Tkinter.BooleanVar()
    username = Tkinter.StringVar()
    password = Tkinter.StringVar()
    
    txt_subreddits = Tkinter.Text(root, width=20, height=30)

    lbl_username = Tkinter.Label(root, text="Username")
    ent_username = Tkinter.Entry(root, width=20, textvariable=username)

    lbl_password = Tkinter.Label(root, text="Password")
    ent_password = Tkinter.Entry(root, show="*", width=20, textvariable=password)

    lbl_instruct = Tkinter.Label(root, text="Number of pages")
    lbl_hot = Tkinter.Label(root, text="Hot")
    lbl_week = Tkinter.Label(root, text="Top of week")
    lbl_month = Tkinter.Label(root, text="Top of month")
    lbl_all = Tkinter.Label(root, text="Top of all time")
    
    entry_hot = Tkinter.Spinbox(root, from_=0, to=10, textvariable=num_hot)
    entry_week = Tkinter.Spinbox(root, from_=0, to=10, textvariable=num_week)
    entry_month = Tkinter.Spinbox(root, from_=0, to=10, textvariable=num_month)
    entry_all = Tkinter.Spinbox(root, from_=0, to=10, textvariable=num_all)

    chk_open_xlinks = Tkinter.Checkbutton(root, text="Auto-open unhandled links", variable=auto_open_links)
    chk_open_text = Tkinter.Checkbutton(root, text="Auto-open text posts", variable=auto_open_text) 

    txt_subreddits.pack()
    lbl_username.pack()
    ent_username.pack()
    lbl_password.pack()
    ent_password.pack()
    lbl_instruct.pack()
    lbl_hot.pack()
    entry_hot.pack()
    lbl_week.pack()
    entry_week.pack()
    lbl_month.pack()
    entry_month.pack()
    lbl_all.pack()
    entry_all.pack()
    chk_open_xlinks.pack()
    chk_open_text.pack()

    Tkinter.Button(root, text="Top NSFW subreddits", command=lambda : fill_subs(top_subreddits)).pack()
    Tkinter.Button(root, text="My subreddits", command=lambda : fill_subs(my_subreddits)).pack()
    
    btn_download = Tkinter.Button(root, text="Download!", command=gui_start_download)
    btn_download.pack()

    root.mainloop()

build_options_window()
