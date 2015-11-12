ALTER TABLE article_author DROP CONSTRAINT article_author_article_id_fkey;
ALTER TABLE article_author DROP CONSTRAINT article_author_author_id_fkey;

ALTER TABLE article_author ADD CONSTRAINT article_author_article_id_fkey
FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE;
ALTER TABLE article_author ADD CONSTRAINT article_author_author_id_fkey
FOREIGN KEY (author_id) REFERENCES authors (id) ON DELETE CASCADE;


ALTER TABLE article_conference DROP CONSTRAINT article_conference_article_id_fkey;
ALTER TABLE article_conference DROP CONSTRAINT article_conference_conference_id_fkey;

ALTER TABLE article_conference ADD CONSTRAINT article_conference_article_id_fkey
FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE;
ALTER TABLE article_conference ADD CONSTRAINT article_conference_conference_id_fkey
FOREIGN KEY (conference_id) REFERENCES conferences (id) ON DELETE CASCADE;


ALTER TABLE article_journal DROP CONSTRAINT article_journal_article_id_fkey;
ALTER TABLE article_journal DROP CONSTRAINT article_journal_journal_id_fkey;

ALTER TABLE article_journal ADD CONSTRAINT article_journal_article_id_fkey
FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE;
ALTER TABLE article_journal ADD CONSTRAINT article_journal_journal_id_fkey
FOREIGN KEY (journal_id) REFERENCES journals (id) ON DELETE CASCADE;

ALTER TABLE article_keyword DROP CONSTRAINT article_keyword_article_id_fkey;
ALTER TABLE article_keyword DROP CONSTRAINT article_keyword_keyword_id_fkey;

ALTER TABLE article_keyword ADD CONSTRAINT article_keyword_article_id_fkey
FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE;
ALTER TABLE article_keyword ADD CONSTRAINT article_keyword_keyword_id_fkey
FOREIGN KEY (keyword_id) REFERENCES keywords (id) ON DELETE CASCADE;