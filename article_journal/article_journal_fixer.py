import re

from utils import *

ARTICLE_JOURNAL_INS_STM = "INSERT INTO article_journal(article_id, journal_id, volume, number) VALUES "


def journals(cursor):
    cursor.execute("SELECT name,id FROM journals")
    return dict(cursor)


# ((SELECT id FROM articles WHERE title = 'Inductive Completion with Retracts.' AND year = 1988),
# (SELECT id FROM journals WHERE name = 'Acta Inf.'), '25', '5'),
def fix_through_file():
    conn = connect()
    cursor = conn.cursor()
    articles_dict = articles(cursor)
    journals_dict = journals(cursor)
    article_ids = set()
    with open("article_journal.sql") as f_in:
        with open("article_journal_fixed.sql", 'w') as f_out:
            f_out.write(ARTICLE_JOURNAL_INS_STM + '\n')
            stm_pattern = re.compile(
                "articles WHERE title = '(.+)' AND year = [0-9]{4}\),\(.+ journals WHERE name = '(.+)'\), ('.+'|NULL), ('.*'|NULL)")
            f_in.readline()
            for line in f_in:
                matcher = stm_pattern.search(line)
                if matcher:
                    title, journal_name, volume, number = matcher.groups()
                    title.replace("''", "'")
                    if title in articles_dict and journal_name in journals_dict:
                        journal_name.replace("''", "'")
                        volume.replace("''", "'")
                        # if volume.startswith("'") and volume.endswith("'"):
                        #     volume = volume[1:len(volume) - 1]
                        # if journal_name.startswith("'") and journal_name.endswith("'"):
                        #     journal_name = journal_name[1:len(volume) - 1]
                        article_id = articles_dict[title]
                        if article_id not in article_ids:
                            article_ids.add(article_id)
                            f_out.write("(%s,%s,%s,%s),\n" % (article_id, journals_dict[journal_name], volume, number))
            f_out.seek(f_out.tell() - 2)
            f_out.write(';')

# fix_through_file()
# run_script("article_journal_fixed.sql")
