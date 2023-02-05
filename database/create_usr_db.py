def create_user():
    pass
# CREATE USER 'temp_user2'@'%' IDENTIFIED BY 'AKJe134##$nar';


def grant_privileges():
    pass
# GRANT select ON tt_main_db.videos TO 'temp_user2'@'%';
# GRANT alter, delete, drop, execute, insert, select, update ON temporary.* TO 'temp_user2'@'%';


def create_database():
    pass
# CREATE SCHEMA `new_schema` ;


def create_users_tb():
    pass
# CREATE TABLE `tt_main_db`.`temporary_tb` (
#   `id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `user_id` BIGINT NULL,
#   `active` TINYINT NULL DEFAULT 1,
#   `date` DATE NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE);

