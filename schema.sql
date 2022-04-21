
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

drop view if exists Resultados;
CREATE VIEW Resultados as
SELECT content AS Bairros, count(*) AS Ocorrências FROM posts group by (content) ORDER BY Ocorrências DESC;

