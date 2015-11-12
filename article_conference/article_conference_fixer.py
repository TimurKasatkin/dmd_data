import re

from utils import *

ARTICLE_CONFERENCE_INS_STM = 'INSERT INTO article_conference (article_id, conference_id) VALUES '


def conferences(cursor):
    """
    :return: conference_name -> conference_id
    """
    cursor.execute("SELECT name,id FROM conferences")
    return dict(cursor)


def fix_through_file():
    conn = connect()
    cursor = conn.cursor()
    articles_dict = articles(cursor)
    conferences_dict = conferences(cursor)
    article_ids = set()
    # ((SELECT id FROM articles WHERE title = 'Document Allocation In Multiprocessor Information Retrieval Systems.' AND year = 1993),
    # (SELECT id FROM conferences WHERE name = 'Advanced Database Systems')),
    with open("article_conference.sql") as f_in:
        with open("article_conference_fixed.sql", 'w') as f_out:
            f_out.write(ARTICLE_CONFERENCE_INS_STM + '\n')
            stm_pattern = re.compile(
                "articles WHERE title = '(.+)' AND year = [0-9]+\),\(.+ conferences WHERE name = '(.+)'")
            f_in.readline()
            for line in f_in:
                match = stm_pattern.search(line)
                if match:
                    title, conf_name = match.groups()
                    title = title.replace("''", "'")
                    conf_name = conf_name.replace("''", "'")
                    if title in articles_dict and conf_name in conferences_dict:
                        article_id = articles_dict[title]
                        row = "(%s,%s),\n" % (article_id, conferences_dict[conf_name])
                        if article_id not in article_ids:
                            article_ids.add(article_id)
                            f_out.write(row)
            f_out.seek(f_out.tell() - 2)
            f_out.write(';')


fix_through_file()
