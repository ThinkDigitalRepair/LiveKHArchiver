import requests
import regex as r
import argparse

parser = argparse.ArgumentParser(
    description="This is a program to download meeting recordings from www.livekingdomhall.com")
parser.add_argument("congregation_id", action="store", help="your congregation id")
parser.add_argument("--mm", action="store_true", default=False, help="download the recording from midweek meeting")
parser.add_argument("--wm", action="store_true", default=False, help="download the recording from weekend meeting")
args = parser.parse_args()

congregation_id = args.congregation_id

"""session = requests.Session()
#session.post("https://www.livekingdomhall.com/kingdomhall/authenticate", data={"list_pass", "1522"})
session_get = session.get(
    "https://www.livekingdomhall.com/kingdomhall/listen/West%20Desert%20Hot%20Springs,%20USA/ODY4Nw==",
    auth=('1522', ''))
request = requests.get(
    "https://www.livekingdomhall.com/kingdomhall/listen/West%20Desert%20Hot%20Springs,%20USA/ODY4Nw==",
    auth=('1522', ''))
"""


# currently, as of 1-7-2018, livekingdomhall doesn't use any authentication behind the scenes. This allows us to
# access our files without having to login. This may change. Please do not abuse this fact.
def get_cong_id(url):
    """
    grab congregation_id from webpage and return it
    :param url: the url of the kingdom hall's page.
    :return: congregation_id
    """
    text = requests.get(url).text
    result = r.findall('\<input type\=\"hidden\" name\=\"congregation_id\" value\=\"(\d+)\"/>', text)
    if len(result) == 0:
        return False
    else:
        return result[0]


def download(congregation_id: int, filename) -> object:
    """
    :return:
    :param congregation_id: The id for your kingdom hall.
    :return: request object
    """
    assert congregation_id != 0

    download_url = "http://162.244.81.220/audio_recordings/" + filename
    mp3 = requests.get(download_url)
    with open(filename, 'wb') as fd:
        for chunk in mp3.iter_content(chunk_size=128):
            fd.write(chunk)
    return mp3


id = get_cong_id("https://www.livekingdomhall.com/kingdomhall/NzY1NA==/East+Desert+Hot+Springs%2C+USA")
if args.mm:
    filename = "record_{0}_{1}.mp3".format(congregation_id, "MM")
    download(args.congregation_id, filename=filename)
if args.wm:
    filename = "record_{0}_{1}.mp3".format(congregation_id, "WM")
    download(args.congregation_id, filename=filename)
pass
