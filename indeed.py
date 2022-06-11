from requests_html import HTMLSession
import csv


def job_data_get(s, location: str, start: int) -> list:
    # return the elements for each job car
    print(f'Retrieving jobs for {location}, page {start}')
    url = f'https://uk.indeed.com/jobs?q=python&l={location}&start={start}'
    r = s.get(url)
    return r.html.find('div.job_seen_beacon')


def parse_html(job) -> dict:
    job_dict = {'title': job.find('h2 > a')[0].text,
                'link': 'https://uk.indeed.com/viewjob?jk=' + job.find('h2 > a')[0].attrs['data-jk'],
                'companyname': job.find('span.companyName')[0].text,
                'snippet': job.find('div.job-snippet')[0].text.replace('\n', '').strip()}

    try:
        job_dict['salary'] = job.find('div.metadata.salary-snippet-container')[0].text
    except IndexError as err:
        job_dict['salary'] = 'no salary info'

    return job_dict


def export(results):
    keys = results[0].keys()
    with open('results.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


def main():
    s = HTMLSession()
    results = []
    for x in range(0, 50, 10):
        jobs = job_data_get(s, 'london', x)
        for job in jobs:
            results.append(parse_html(job))
    export(results)


if __name__ == '__main__':
    main()
