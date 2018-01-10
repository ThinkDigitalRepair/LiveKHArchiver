import requests
import regex as r
import argparse

parser = argparse.ArgumentParser(
    description="This is a program to download meeting recordings from www.livekingdomhall.com. " \
                "If you don't know your congregation id, enter 0 for the id and use the --lookup command.")
parser.add_argument("congregation_id", action="store", help="your congregation id")
parser.add_argument("--mm", action="store_true", default=False, help="download the recording from midweek meeting")
parser.add_argument("--wm", action="store_true", default=False, help="download the recording from weekend meeting")
parser.add_argument("--lookup", action="store",
                    help="follow this option with the url of the congregation you want to lookup")
args = parser.parse_args()


# As of 1-7-2018, livekingdomhall doesn't use any authentication behind the scenes. This allows us to
# access our files without having to login. This may change. Please do not abuse this fact.
def get_congregation_id(url):
    """
    grab congregation_id from webpage and return it
    :param url: the url of the kingdom hall's page.
    :return: congregation_id
    """
    text = requests.get(url).text
    result = r.findall('\<input type\=\"hidden\" name\=\"congregation_id\" value\=\"(\d+)\"/>', text)

    return False if len(result) == 0 else result[0]


def download(c_id: int, fn) -> object:
    """
    :param fn: the name to save the file under
    :return:
    :param c_id: the id for your congregation.
    :return: request object
    """
    assert c_id != 0

    download_url = "http://162.244.81.220/audio_recordings/" + fn
    mp3 = requests.get(download_url)
    with open(fn, 'wb') as fd:
        for chunk in mp3.iter_content(chunk_size=128):
            fd.write(chunk)
    return mp3


if __name__ == '__main__':
    if args.lookup:
        congregation_id = get_congregation_id(args.lookup)

    if args.mm:  # if midweek meeting download flag is set
        filename = "record_{0}_{1}.mp3".format(congregation_id, "MM")
        download(args.congregation_id, fn=filename)
    if args.wm:  # if weekend meeting download flag is set
        filename = "record_{0}_{1}.mp3".format(congregation_id, "WM")
        download(args.congregation_id, fn=filename)
