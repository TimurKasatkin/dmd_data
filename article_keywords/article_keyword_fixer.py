import re

from utils import *

ARTICLE_KEYWORD_INS_STM = 'INSERT INTO article_keyword(article_id, keyword_id) VALUES '


def keywords(cursor):
    cursor.execute("SELECT word,id FROM keywords")
    return dict(cursor)


# ((SELECT id FROM articles WHERE title = 'Inductive Completion with Retracts.' AND year = 1988),
# (SELECT id FROM keywords WHERE word = 'inductive')),
def fix_through_db():
    conn = connect()
    cursor = conn.cursor()
    articles_dict = articles(cursor)
    keywords_dict = keywords(cursor)
    rows = set()
    stm_pattern = re.compile("articles WHERE title = '(.+)' AND year = [0-9]{4}\),\(.+ keywords WHERE word = '(.*)'")
    with open("article_keyword.sql") as f_in:
        with open("article_keyword_fixed.sql", 'w') as f_out:
            f_out.write(ARTICLE_KEYWORD_INS_STM + '\n')
            for line in f_in:
                matcher = stm_pattern.search(line)
                if matcher:
                    title, word = matcher.groups()
                    title, word = title.replace("''", "'"), word.replace("''", "'")
                    if title in articles_dict and word in keywords_dict:
                        row = "(%s,%s),\n" % (articles_dict[title], keywords_dict[word])
                        if row not in rows:
                            rows.add(row)
                            f_out.write(row)
            f_out.seek(f_out.tell() - 2)
            f_out.write(";")


# fix_through_db()

print("File splitting ...")
split_file('article_keyword_fixed.sql', 500000, './parts')
print("Parts fixing...")
fix_parts("article_keyword", ARTICLE_KEYWORD_INS_STM, './parts')
print("Scripts running")
for file in os.listdir('./parts'):
    run_script('./parts/%s' % file)
