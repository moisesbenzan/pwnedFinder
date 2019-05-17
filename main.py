import argparse
import requests
import urllib.parse
from bs4 import BeautifulSoup


VERSION = "pwnedFinder-0.01"
DATABASES_TODAY = "https://www.databases.today/search-nojs.php"
HAVE_I_BEEN_PWNED = "https://haveibeenpwned.com/api/breachedaccount/{}"


def init_parser():
    parser = argparse.ArgumentParser(
        description='Find in which dumps the credentials (username/email) provided is pwned.')

    parser.add_argument('--version',
                        action='version',
                        version=VERSION,
                        help="Prints the version information and exits.")

    parser.add_argument('--target', "-t",
                        action="append",
                        help="List of targets to search for pwned credentials.")

    parser.add_argument("--find-dumps", "-fd",
                        action="store_true",
                        help="Attempts to find a downloadable dump containing the target's password or hash")

    return parser


def check_pwned(creds):
    """
    Returns a list of breaches where the target appears to be pwned.
    :param creds: String. Email or username to search for.
    :return: List. List of breaches where the target appears to be pwned.
    """
    url = HAVE_I_BEEN_PWNED.format(urllib.parse.quote(creds, safe=''))
    res = requests.get(url,
                       params={
                           "truncateResponse": "true"
                       },
                       headers={
                           "api-version": "2",
                           "User-Agent": VERSION
                       })

    pwned_list = []

    if res.status_code == 404:
        return []

    try:
        for source in res.json():
            pwned_list.append(source['Name'])
    except:
        print("Error occured.")
        print(res)

    return pwned_list


def search_dumps(source_name_list):
    downloadables = []

    for source in source_name_list:
        res = requests.get(DATABASES_TODAY,
                           params={
                               "for": urllib.parse.quote(source, safe='')
                           },
                           headers={
                               "User-Agent": VERSION
                           })

        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", id="myTable")
        t_rows = table.find_all("tr")[1:]

        for row in t_rows:
            data = row.find_all("td")
            s_name, s_size = str(data[0]).replace("<td>", "").replace("</td>", "").split(" ", 1)
            s_link = row.find("a")['href']
            downloadables.append((s_name, s_size, s_link))

    return downloadables


def dump_summary(c_target, c_dumps):

    if len(a_dumps) > 0:
        print("Found dump(s) containing credentials of the supplied target: {}".format(c_target))
        for dump in c_dumps:
            print("""
            Name: {}
            Size: {}
            URL: {}""".format(dump[0], dump[1], dump[2]))
    else:
        print("Target: {} has not been breached".format(c_target))


def sources_summary(c_target, c_sources):
    if len(c_sources) > 0:
        print("Found leaked databases containing credentials of the supplied target: {}".format(c_target))
        for source in c_sources:
            print("Name: {}".format(source))
    else:
        print("Target: {} has not been breached".format(c_target))


if __name__ == '__main__':

    args = init_parser().parse_args()
    for target in args.target:
        sources = check_pwned(target)
        if args.find_dumps:
            a_dumps = search_dumps(sources)
            dump_summary(target, a_dumps)
        else:
            sources_summary(target, sources)
