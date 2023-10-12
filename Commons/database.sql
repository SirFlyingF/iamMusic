CREATE TABLE `iammusic`.`song` (
  `song_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(64) NOT NULL,
  `path` VARCHAR(256) NOT NULL,
  `song_artist` VARCHAR(64),
  `album_artist` VARCHAR(64),
  `album` VARCHAR(64),
  `track_num` INT,
  `duration` INT,
  PRIMARY KEY (`song_id`));

CREATE TABLE `iammusic`.`playlist` (
  `playlist_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`playlist_id`));

CREATE TABLE `iammusic`.`playlist_song_reltn` (
  `song_id` INT NOT NULL,
  `playlist_id` INT NOT NULL,
  PRIMARY KEY (`song_id`, `playlist_id`));