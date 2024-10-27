from collections import namedtuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup

POSTS = dict()

Post = namedtuple("Post", ["link", "title", "date"])

url = "https://recruiting.ultipro.com/COM1019CTDI1/JobBoard/ab728dae-48cf-43af-8869-6b591e5d9495/JobBoardView/LoadSearchResults"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Cookie': '.AspNetCore.Antiforgery.JethAzbTYfI=CfDJ8BHmAv0GmhpOmOe2LfzwiCVJFPXo_x1_3juU64RE3tD-N6e5NB29PcaGzjagsB4KvO5yX0KTMLlgLUOMmmg_rcdqZSvZdJfG2FwNbzbArQ9VUSK3sqr42FLSgegr8rBzVnIp882eX6k-gATcEp3pMKg; nonce=qjftAofyAyJnOjD9JRusCiqUxtBdEl0bNqoWe-IzivQ; _ga_X9M5GGEYRH=GS1.1.1729997513.1.0.1729997513.0.0.0; _ga=GA1.1.688193734.1729997513; _ga_GK72NCW8CT=GS1.1.1729997513.1.0.1729997513.0.0.0; _dd_s=rum=2&id=a966421c-8e73-4c29-b784-f1908909d6c7&created=1729997512708&expire=1729998436319',
    'Origin': 'https://recruiting.ultipro.com',
    'Referer': 'https://recruiting.ultipro.com/COM1019CTDI1/JobBoard/ab728dae-48cf-43af-8869-6b591e5d9495/?q=&o=postedDateDesc',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-RequestVerificationToken': 'CfDJ8BHmAv0GmhpOmOe2LfzwiCVtzhH3x469vd8xUCCDia4xyiJBZQJO33G0ClcuhN9nGqdpXhg-rdnqxLW4aNOTfy45zYC5tqrx3zvQkmedXKaulz78W5Qu9pDOGx6HVcr1tIoouURUNh-PyJMzCoHwrWU',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'traceparent': '00-000000000000000072c35a237383666a-30acd7a995559166-01',
}

json_data = {
    "opportunitySearch":{
        "Top":50,
        "Skip":0,
        "QueryString":"",
        "OrderBy":[
            {
                "Value":"postedDateDesc",
                "PropertyName":"PostedDate",
                "Ascending":False
            }
        ],
        "Filters":[
            {
                "t":"TermsSearchFilterDto",
                "fieldName":4,
                "extra":None,
                "values":[]
            },
            {
                "t":"TermsSearchFilterDto",
                "fieldName":5,
                "extra":None,
                "values":[]
            },
            {
                "t":"TermsSearchFilterDto",
                "fieldName":6,
                "extra":None,
                "values":[]
            },
            {
                "t":"TermsSearchFilterDto",
                "fieldName":37,
                "extra":None,
                "values":[]
            }
        ]
    },
    "matchCriteria": {
        "PreferredJobs":[],
        "Educations":[],
        "LicenseAndCertifications":[],
        "Skills":[],
        "hasNoLicenses":False,
        "SkippedSkills":[]
    }
}

response = requests.post(
    url=url,
    headers=headers,
    json=json_data,
)

jobs = dict(response.json())['opportunities']


for job in jobs:
    title = job['Title']
    id = job['Id']
    link = "https://recruiting.ultipro.com/COM1019CTDI1/JobBoard/ab728dae-48cf-43af-8869-6b591e5d9495/OpportunityDetail?opportunityId="+id
    date = datetime.strptime(job['PostedDate'], "%Y-%m-%dT%H:%M:%S.%fZ")
    POSTS[link] = Post(link, title, date)

STREAM = sorted(
    [POSTS[key] for key in POSTS.keys()], key=lambda x: x.date, reverse=True
)

if __name__ == "__main__":
    NOW = datetime.now()
    XML = "\n".join(
        [
            r"""<?xml version="1.0" encoding="UTF-8" ?>""",
            r"""<rss version="2.0">""",
            r"""<channel>""",
            r"""<title>CTDI Careers</title>""",
            r"""<description>CTDI Careers</description>""",
            r"""<language>en-us</language>""",
            r"""<pubDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</pubDate>""",
            r"""<lastBuildDate>"""
            + NOW.strftime("%a, %d %b %Y %H:%M:%S GMT")
            + r"""</lastBuildDate>""",
            "\n".join(
                [
                    r"""<item><title><![CDATA["""
                    + x.title
                    + r"""]]></title><link>"""
                    + x.link
                    + r"""</link><pubDate>"""
                    + x.date.strftime("%a, %d %b %Y %H:%M:%S GMT")
                    + r"""</pubDate></item>"""
                    for x in STREAM
                ]
            ),
            r"""</channel>""",
            r"""</rss>""",
        ]
    )

    print(XML)
