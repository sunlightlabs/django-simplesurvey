ALTER TABLE simplesurvey_questionset ADD COLUMN allow_anonymous TINYINT(1) DEFAULT 1;
ALTER TABLE simplesurvey_questionset ADD COLUMN allow_multiple_responses TINYINT(1) DEFAULT 1;