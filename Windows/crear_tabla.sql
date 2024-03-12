CREATE SCHEMA `tiempo` ;
CREATE TABLE `tiempo`.`temperaturas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `Maxima` FLOAT NOT NULL,
  `Minima` FLOAT NULL,
  `ciudad` VARCHAR(45) NULL,
  `latitud` FLOAT NULL,
  `longitud` FLOAT NULL,
  PRIMARY KEY (`id`));
