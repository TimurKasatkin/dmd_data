import os
import subprocess

import psycopg2


def connect():
    return psycopg2.connect(database="dmd_semester_task", user="postgres", password="postgres")


def articles(cursor):
    """
    :return: article title -> articles id
    """
    cursor.execute("SELECT title,id FROM articles")
    return dict(cursor)


def split_file(file_path, lines=100000, target_dir: str = '.'):
    path, filename = os.path.split(file_path)
    basename, ext = os.path.splitext(filename)
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    with open(file_path, 'r') as f_in:
        try:
            f_out = open(os.path.join(path, '{}/{}_{}{}'.format(target_dir, basename, 0, ext)), 'w')
            for i, line in enumerate(f_in):
                if i % lines == 0:
                    f_out.close()
                    f_out = open(os.path.join('{}/{}_{}{}'.format(target_dir, basename, i, ext)), 'w')
                f_out.write(line)
        finally:
            if f_out:
                f_out.close()


def fix_parts(file_prefix: str, insert_stm: str, dir: str = '.'):
    files = os.listdir(dir)
    for file in files:
        if file_prefix in file:
            with open('{0}/{1}'.format(dir, file), 'r+') as f:
                lines = f.read().splitlines()
                lines_count = len(lines)
                last_line = lines[lines_count - 1]
                lst_line_length = len(last_line)
                if last_line[lst_line_length - 1] == ',':
                    lines[lines_count - 1] = last_line[0:lst_line_length - 1] + ';'
                f.seek(0)
                if insert_stm not in lines[0]:
                    f.write("{0}\n{1}".format(insert_stm, '\n'.join(lines)))
                else:
                    f.write('\n'.join(lines))


def run_script(filepath: str, username: str = 'postgres', dbname: str = 'dmd_semester_task'):
    subprocess.call(['psql', '-U', username, '-d', dbname, '-f', filepath])
