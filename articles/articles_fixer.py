__author__ = 'timur'

ARTICLES_INSERT_STM = 'INSERT INTO articles (title,publtype,url,year) VALUES '


def parse_title(line):
    return line[1: line.index("','")]

# fix_parts('article_author', ARTICLE_AUTHOR_INS_STM, './article_author')

# files = os.listdir('./article_author')
#
# for file in files:
#     if 'article_author_' in file and 'fixed' not in file:
#         # cat article_author_*.sql | sed "s/ AND year = [0-9]\{4\}//"  >> article_author_0_fixed.sql
#         p1 = subprocess.Popen(split('cat {0}/{1}'.format('./article_author', file)), stdout=subprocess.PIPE)
#         p2 = subprocess.Popen(['sed', 's/ AND year = [0-9]\{4\}//'], stdin=p1.stdout, stdout=subprocess.PIPE)
#         name, ext = os.path.splitext(file)
#         output = p2.communicate()[0]
#         with open('{}/{}_fixed{}'.format('./article_author', name, ext), 'w') as f_out:
#             f_out.write(str(output))

# subprocess.Popen(['>>', '{}_fixed{}'.format(name, ext)], stdin=p2.stdout)
# subprocess.call('cat')
# subprocess.call(['psql', '-U', 'postgres', '-d', 'dmd_semester_task', '-f',
#                  '{0}/{1}'.format('./article_author', file)])

# art_dict = {}
# with open("articles.sql") as f:
#     for l in f:
#         l = l.rstrip('\n')  # remove '\n'
#         if 'INTO articles' in l:
#             insert_str = l
#         elif "','" in l and not '(NULL' in l:
#             l = l.replace(');', '),')
#             art_dict[parse_title(l)] = l
#
# with open('articlesFixed.sql', 'w') as art_f:
#     art_f.write('%s\n' % insert_str)
#     art_f.writelines('%s\n' % line for line in art_dict.values())

# split_file('articlesFixed.sql', 500000)

# files = os.listdir('./articles')

# for file in files:
#     if 'articlesFixed_' in file:
#         f = open(file, 'rw')
#         break


# split_file('article_author.sql', 500000, './article_author')
