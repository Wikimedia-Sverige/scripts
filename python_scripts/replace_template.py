#! /usr/bin/env python

# Expects pywikibot 7.0
"""Bot to replace all uses of a given template by a new template."""
from queue import Queue

import pywikibot
from pywikibot.tools.formatter import color_format
from pywikibot.bot_choice import QuitKeyboardInterrupt

changed_pages = 0
_pending_processed_titles = Queue()


def init_generator(old_template, site):
    """Create a generator for pages transcluding the old template."""
    page = pywikibot.Page(
        pywikibot.Link(old_template, default_namespace=10, source=site))
    return page.getReferences(only_template_inclusion=True)


def _count_changes(page, err):
    """Count successfully changed pages; log changed titles for display."""
    # This is an async put callback
    if not isinstance(err, Exception):
        global changed_pages
        changed_pages += 1
        _pending_processed_titles.put((page.title(as_link=True), True))
    else:  # unsuccessful pages
        _pending_processed_titles.put((page.title(as_link=True), False))


def _replace_async_callback(page, err):
    """Callback for asynchronous page edit."""
    _count_changes(page, err)


def main():
    """Main entrypoint for the script."""
    always = False
    site = pywikibot.Site('se', 'wikimediachapter')
    site.login()
    old_template = pywikibot.input('Name of old template (no prefix)')
    new_template = pywikibot.input('Name of new template (no prefix)')
    summary = pywikibot.input('Edit summary')

    summary = '{sum} ({old} -> {new})'.format(
        sum=summary, old='{{%s' % old_template, new='{{%s' % new_template)

    for page in init_generator(old_template, site):
        try:
            # Load the page's text from the wiki
            original_text = page.get(get_redirect=True)
            if not page.has_permission('edit'):
                pywikibot.output(
                    "You can't edit page %s" % page.title(as_link=True))
                continue
        except pywikibot.NoPage:
            pywikibot.output('Page %s not found' % page.title(as_link=True))
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
            try:
                choice = pywikibot.input_choice(
                    'Do you want to accept these changes?',
                    [('Yes', 'y'), ('No', 'n'), ('all', 'a')],
                    default='N')
            except QuitKeyboardInterrupt:
                break

        if choice == 'a':
            always = True
            choice = 'y'
        if choice == 'y':
            page.text = new_text
            page.save(summary=summary,
                      asynchronous=True,
                      callback=_replace_async_callback,
                      quiet=True)
        # choice must be 'N'
        continue

    pywikibot.output('{} page(s) were updated'.format(changed_pages))


if __name__ == "__main__":
    main()
