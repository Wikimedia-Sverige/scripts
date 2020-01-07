#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Bot to replace all uses of a given template by a new template."""
from __future__ import absolute_import, unicode_literals
import sys
import pywikibot
from pywikibot import pagegenerators
from pywikibot.tools.formatter import color_format

if sys.version_info[0] > 2:
    from queue import Queue
    long = int
else:
    from Queue import Queue

changed_pages = 0
_pending_processed_titles = Queue()


def init_generator(old_template, site):
    """Create a generator for pages transcluding the old template."""
    page = pywikibot.Page(
        pywikibot.Link(old_template, defaultNamespace=10, source=site))
    return pagegenerators.ReferringPageGenerator(
        page, onlyTemplateInclusion=True)


def _count_changes(page, err):
    """Count successfully changed pages; log changed titles for display."""
    # This is an async put callback
    if not isinstance(err, Exception):
        global changed_pages
        changed_pages += 1
        _pending_processed_titles.put((page.title(asLink=True), True))
    else:  # unsuccessful pages
        _pending_processed_titles.put((page.title(asLink=True), False))


def _replace_async_callback(page, err):
    """Callback for asynchronous page edit."""
    _count_changes(page, err)


def main():
    """Main entrypoint for the script."""
    always = False
    site = pywikibot.Site('se', 'wikimediachapter')
    site.login(sysop=True)
    old_template = pywikibot.input(u'Name of old template (no prefix)')
    new_template = pywikibot.input(u'Name of new template (no prefix)')
    summary = pywikibot.input(u'Edit summary')

    summary = '{sum} ({old} -> {new})'.format(
        sum=summary, old='{{%s' % old_template, new='{{%s' % new_template)

    for page in init_generator(old_template, site):
        try:
            # Load the page's text from the wiki
            original_text = page.get(get_redirect=True)
            if not page.canBeEdited():
                pywikibot.output(
                    "You can't edit page %s" % page.title(asLink=True))
                continue
        except pywikibot.NoPage:
            pywikibot.output('Page %s not found' % page.title(asLink=True))
            continue

        new_text = original_text.replace(
            '{{' + old_template, '{{' + new_template)
        if original_text == new_text:
            continue

        pywikibot.output(color_format(
            '\n\n>>> {lightpurple}{0}{default} <<<', page.title()))
        pywikibot.showDiff(original_text, new_text)

        if always:
            choice = 'y'
        else:
            choice = pywikibot.input_choice(
                u'Do you want to accept these changes?',
                [('Yes', 'y'), ('No', 'n'), ('all', 'a')],
                default='N')

        if choice == 'a':
            always = True
            choice = 'y'
        if choice == 'y':
            page.text = new_text
            page.save(summary=summary,
                      asynchronous=True,
                      callback=_replace_async_callback,
                      quiet=True, as_group='sysop')
        # choice must be 'N'
        continue


if __name__ == "__main__":
    main()