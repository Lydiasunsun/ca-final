Drop TABLE if EXISTS activities;

CREATE TABLE activities
(
              activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              score REAL NOT NULL,
              description TEXT

);
INSERT INTO activities
              (name,score,description)
VALUES
              ('Healthy and delicious food', '4', 'Eating heathy is fundamental for a healthy mind and body~'),
              ('Connection with people', '2', 'No one should feel an lonely island ^^')

,
              ('Connection with nature', '1', 'Mother nature offers endless love'),
              ('Sports and excercise ', '3', 'Sweat genarate dopamine'),
              ('Achievements and Value in work or life', '2', 'achievements give us possitive feedback'),
              ('Money', '2', 'Money is important'),
              ('Meditation', '1', 'Stop the monkey mind'),

              ('Daily small stuff', '1', "Keep a record of daily small hapiness, maybe just your cat sit on your leg, or smell flower on the street ^^")
;

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
              user_id TEXT PRIMARY KEY,
              password TEXT NOT NULL
);