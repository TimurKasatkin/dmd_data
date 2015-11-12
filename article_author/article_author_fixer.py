import re

from utils import *

ARTICLE_AUTHOR_INS_STM = 'INSERT INTO article_author (article_id,author_id) VALUES '


# ((SELECT id FROM articles WHERE title = 'Project scheduling with irregular costs: complexity, approximability, and algorithms.' AND year = 2004),
# (SELECT id FROM authors WHERE first_name = 'Alexander' AND last_name = 'Grigoriev')),
def fix_through_db():
    conn = connect()
    cursor = conn.cursor()
    articles_dict = articles(cursor)
    authors_dict = authors(cursor)
    stm_pattern = re.compile(
        "SELECT id FROM articles WHERE title = '(.+)' AND year = [0-9]+\),"
        "\(SELECT id FROM authors WHERE first_name = '(.+)' AND last_name = '(.+)'")

    files = filter(lambda f: f.startswith("article_author") and f.endswith(".sql"),
                   os.listdir("../article_author"))
    rows = set()
    with open("article_author.sql", 'w') as f_out:
        f_out.write(ARTICLE_AUTHOR_INS_STM + '\n')
        for file_name in files:
            with open(file_name) as f_in:
                f_in.readline()
                for line in f_in:
                    matcher = stm_pattern.search(line)
                    if matcher:
                        groups = matcher.groups()
                        title = groups[0].replace("''", "'")
                        if title in articles_dict:
                            first_name = groups[1].replace("''", "'")
                            last_name = groups[2].replace("''", "'")
                            full_name = tuple([first_name, last_name])
                            if full_name in authors_dict:
                                row = "({article_id},{author_id}),\n" \
                                    .format(article_id=articles_dict[title],
                                            author_id=authors_dict[full_name])
                                if row not in rows:
                                    rows.add(row)
                                    f_out.write(row)
        f_out.seek(f_out.tell() - 2)
        f_out.write(';')


def authors(cursor):
    cursor.execute("SELECT first_name,last_name,id FROM authors")
    authors_dict = dict(map(lambda t: tuple([t[0:2], t[2]]), cursor))
    return authors_dict


# fix_through_db()
# split_file("article_author.sql", 500000, "./parts")
# fix_parts("article_author_", ARTICLE_AUTHOR_INS_STM, "./parts")

# files_dir = './parts'
# files = os.listdir(files_dir)
# for file in files:
#     run_script("{0}/{1}".format(files_dir, file))


def fix_through_file():
    # parse all article titles
    titles = set()
    # files = os.listdir('./articles')
    files = ["../articles/articlesFixed_0.sql", "../articles/articlesFixed_500000.sql"]
    for file in files:
        with open(file) as f_in:
            titles = titles.union(map(lambda l: l[2:l.index("',")],
                                      filter(lambda l_inner: "INSERT" not in l_inner, f_in.readlines())))

    # fix file
    file_name = 'article_author_0.sql'

    print("Titles count: %d" % len(titles))

    with open(file_name) as f:
        # line_count = sum(1 for _ in f)
        name, ext = os.path.splitext(file_name)
        f.readline()  # skip line with insert
        with open("%s_fixed%s" % (name, ext), 'w') as f_out:
            f.readline()
            f_out.write(ARTICLE_AUTHOR_INS_STM + "\n")
            search_word = "title = "
            for line in f:
                title = line[line.index(search_word) + len(search_word) + 1:line.index(" AND") - 1]
                if title in titles:
                    f_out.write(line)

# with open(file_name, 'r+') as f:
#     line_count = sum(1 for _ in f)
#     f.seek(0)
#     name, ext = os.path.splitext(file_name)
#     with open("%s_fixed%s" % (name, ext), 'w') as f_out:
#         for i in range(1, line_count + 1):
#             cur_line = f.readline()
#             line_length = len(cur_line)
#             if i % offset == 0:
#                 f_out.seek(cur(f_out) - 2)
#                 f_out.write(";\n")
#                 f_out.write(ARTICLE_AUTHOR_INS_STM + "\n")
#             f_out.write(cur_line)
