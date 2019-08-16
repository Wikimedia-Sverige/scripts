import sys
from xml.etree import ElementTree
import datetime


DAY_TITLE_FORMAT = '%A %d %B'
CSS_PAGE = 'Program List.css'
PAGE_NAME = 'Program List'
PAGE_NAMESPACE = 'Template'


def get_next_day(days):
    next_day = None
    for day in days:
        if next_day is None:
            next_day = day
        else:
            next_date = strptime(next_day.get('date'), '%Y-%m-%d')
            date = strptime(day.get('date'), '%Y-%m-%d')
            if date < next_date:
                next_day = day
    return next_day


def strptime(*args):
    return datetime.datetime.strptime(*args)


def build_day_string(day):
    date = strptime(day.get('date'), '%Y-%m-%d')
    return date.strftime(DAY_TITLE_FORMAT)


def get_next_event(events):
    """Get the next from a list of event

    Checks first for start time and then title alphabetically.
    """

    next_event = None
    for event in events:
        if next_event is None:
            next_event = event
        else:
            start = strptime(event.find('start').text, '%H:%M')
            next_start = strptime(next_event.find('start').text, '%H:%M')
            title = event.find('title').text
            next_title = next_event.find('title').text
            if start < next_start or \
               start == next_start and title < next_title:
                next_event = event
    return next_event


def create_wikitext_item(event):
    parameters = {}
    start = event.find('start').text
    parameters['start'] = start
    start_time = strptime(start, '%H:%M')
    duration_string = event.find('duration').text
    duration_time = strptime(duration_string, '%H:%M')
    end_time = start_time + datetime.timedelta(
        hours=duration_time.hour, minutes=duration_time.minute
    )
    parameters['end'] = end_time.strftime('%H:%M')
    space_element = event.find('space')
    if space_element is not None:
        parameters['space'] = space_element.text
    parameters['room'] = event.find('room').text
    parameters['title'] = event.find('title').text
    persons_element = event.find('persons')
    if persons_element is not None:
        parameters['presenters'] = build_presenters_string(persons_element)
    for k, v in event.find('identifiers').attrib.items():
        parameters[k] = v
    parameters['link'] = event.find('links/link').get('href')[37:]
    wikitext = build_invoke_string(parameters)
    return wikitext


def build_invoke_string(parameters):
    wikitext = '{{#invoke:Program|item'
    for k, v in parameters.items():
        wikitext += '|{}={}'.format(k, v)
    wikitext += '}}'
    return wikitext


def build_presenters_string(persons_element):
    person_elements = persons_element.findall('person')
    presenters_string = ", ".join([p.text for p in person_elements])
    return presenters_string


if __name__ == '__main__':
    tree = ElementTree.parse(sys.argv[-1])
    out = '<templatestyles src="{}" />\n'.format(CSS_PAGE)
    root = tree.getroot()
    days = root.findall('.//day')
    day_index = 1
    while days:
        day = get_next_day(days)
        days.remove(day)
        day_string = build_day_string(day)
        out += '{{#ifeq:{{{day}}}' + '|{}|'.format(day_index)
        out += '{{#invoke:Program|start|accessibility={{{accessibility}}}|research={{{research}}}|strategy={{{strategy}}}|education={{{education}}}|growth={{{growth}}}|technology={{{technology}}}|partnerships={{{partnerships}}}|technology={{{technology}}}|strategy={{{strategy}}}|health={{{health}}}|partnerships={{{partnerships}}}|multimedia={{{multimedia}}}|glam={{{glam}}}}}'
        events = day.findall('.//event')
        while events:
            event = get_next_event(events)
            events.remove(event)
            out += create_wikitext_item(event)
        out += '{{#invoke:Program|end_}}}}\n'
        day_index += 1
    if '--bot' in sys.argv:
        from pywikibot import Site
        from pywikibot import Page
        page = Page(Site(), PAGE_NAME, PAGE_NAMESPACE)
        page.text = out
        page.save()
    else:
        print(out)
