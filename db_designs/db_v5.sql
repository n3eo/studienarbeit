-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Remove Tables
DROP TABLE IF EXISTS `MediumWortZuord`;
DROP TABLE IF EXISTS `Schlagwort`;

DROP TABLE IF EXISTS `Ausleihe`;

DROP TABLE IF EXISTS `Video`;
DROP TABLE IF EXISTS `Bild`;
DROP TABLE IF EXISTS `NichtTextMedien`;

DROP TABLE IF EXISTS `Ebooks`;
DROP TABLE IF EXISTS `Hoerbuch`;

DROP TABLE IF EXISTS `AutorBuchZuord`;
DROP TABLE IF EXISTS `Buch`;

DROP TABLE IF EXISTS `Sorte`;
DROP TABLE IF EXISTS `Verlag`;

DROP TABLE IF EXISTS `Maler`;
DROP TABLE IF EXISTS `Ausleiher`;
DROP TABLE IF EXISTS `Sprecher`;
DROP TABLE IF EXISTS `Autor`;
DROP TABLE IF EXISTS `Person`;
-- ---

-- ---
-- Table 'Buch'
-- 
-- ---
		
CREATE TABLE `Buch` (
  `ISBN` VARCHAR(13) NOT NULL,
  `Titel` VARCHAR(100) NOT NULL,
  `Untertitel` VARCHAR(100) NULL DEFAULT NULL,
  `VerlagId` INTEGER(11) NULL DEFAULT NULL,
  `Erscheinungsjahr` YEAR(4) NULL DEFAULT NULL,
  `SorteId` INTEGER(11) NULL DEFAULT NULL,
  `Kurzbeschreibung` VARCHAR(100) NULL DEFAULT NULL,
  `Preis` DECIMAL(10,3) NULL DEFAULT NULL,
  `Auflage` VARCHAR(20) NULL DEFAULT NULL,
  `Sprache` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`ISBN`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Person'
-- 
-- ---;
		
CREATE TABLE `Person` (
  `PersonenId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `Vorname` VARCHAR(20) NOT NULL,
  `Name` VARCHAR(30) NOT NULL,
  `Email` VARCHAR(30) NULL DEFAULT NULL,
  `Geburtsdatum` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`PersonenId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Ausleihe'
-- 
-- ---
		
CREATE TABLE `Ausleihe` (
  `TransaktionsId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `AusleiherId` INTEGER(11) NOT NULL,
  `MediumId` VARCHAR(13) NOT NULL,
  `Ausleihdatum` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Rückgabedatum` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`TransaktionsId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'AutorBuchZuord'
-- 
		
CREATE TABLE `AutorBuchZuord` (
  `AutorId` INTEGER(11) NOT NULL,
  `ISBN` VARCHAR(13) NOT NULL
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Autor'
-- 
-- ---
		
CREATE TABLE `Autor` (
  `AutorId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `PersonenId` INTEGER(11) NOT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`AutorId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Ausleiher'
-- 
-- ---
		
CREATE TABLE `Ausleiher` (
  `AusleiherId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `PersonenId` INTEGER(11) NOT NULL,
  `Strasse` VARCHAR(50) NOT NULL DEFAULT 'NULL',
  `Postleitzahl` VARCHAR(5) NOT NULL DEFAULT 'NULL',
  `Ort` VARCHAR(30) NOT NULL,
  `Telefonnummer` VARCHAR(30) NULL DEFAULT NULL,
  PRIMARY KEY (`AusleiherId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Schlagwort'
-- 
-- ---
		
CREATE TABLE `Schlagwort` (
  `Wort` VARCHAR(20) NOT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`Wort`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Sorte'
-- 
-- ---
		
CREATE TABLE `Sorte` (
  `SorteId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(50) NOT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`SorteId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Verlag'
-- 
-- ---
		
CREATE TABLE `Verlag` (
  `VerlagId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `Kurzname` VARCHAR(20) NULL DEFAULT NULL,
  `Name` VARCHAR(50) NOT NULL,
  `Postleitzahl` VARCHAR(5) NULL DEFAULT NULL,
  `Strasse` VARCHAR(50) NULL DEFAULT NULL,
  `Internetadresse` VARCHAR(30) NULL DEFAULT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`VerlagId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Ebooks'
-- 
-- ---
		
CREATE TABLE `Ebooks` (
  `ISBN` VARCHAR(13) NOT NULL,
  `BuchISBN` VARCHAR(13) NOT NULL,
  `Dateiformat` VARCHAR(10) NULL DEFAULT NULL,
  PRIMARY KEY (`ISBN`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Sprecher'
-- 
-- ---
		
CREATE TABLE `Sprecher` (
  `SprecherId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `PersonenId` INTEGER(11) NOT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`SprecherId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Video'
-- 
-- ---
		
CREATE TABLE `Video` (
  `VideoId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `NichtTextMedienId` VARCHAR(13) NOT NULL,
  `Sprache` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`VideoId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Hoerbuch'
-- 
-- ---
		
CREATE TABLE `Hoerbuch` (
  `ISBN` VARCHAR(13) NOT NULL,
  `BuchISBN` VARCHAR(13) NOT NULL,
  `SprecherId` INTEGER(11) NOT NULL,
  `VerlagId` INTEGER(11) NULL DEFAULT NULL,
  PRIMARY KEY (`ISBN`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Bild'
-- 
-- ---
		
CREATE TABLE `Bild` (
  `BildId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `NichtTextMedienId` VARCHAR(13) NOT NULL,
  `Bild` LONGBLOB NULL DEFAULT NULL,
  `MalerId` INTEGER(11) NOT NULL,
  PRIMARY KEY (`BildId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'MediumWortZuord'
-- 
-- ---
		
CREATE TABLE `MediumWortZuord` (
  `MediumId` VARCHAR(13) NOT NULL,
  `Wort` VARCHAR(20) NOT NULL
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'Maler'
-- 
-- ---
		
CREATE TABLE `Maler` (
  `MalerId` INTEGER(11) NOT NULL AUTO_INCREMENT,
  `PersonenId` INTEGER(11) NOT NULL,
  `Beschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`MalerId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Table 'NichtTextMedien'
-- 
-- ---
		
CREATE TABLE `NichtTextMedien` (
  `NichtTextMedienId` VARCHAR(13) NOT NULL,
  `Titel` VARCHAR(100) NOT NULL,
  `Untertitel` VARCHAR(60) NULL DEFAULT NULL,
  `Erscheinungsjahr` YEAR(4) NULL DEFAULT NULL,
  `Kurzbeschreibung` MEDIUMTEXT NULL DEFAULT NULL,
  `SorteId` INTEGER(11) NOT NULL,
  `Typ` ENUM("Bild","Video") NOT NULL,
  PRIMARY KEY (`NichtTextMedienId`)
) CHARACTER SET=utf8mb4;

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `Buch` ADD FOREIGN KEY (VerlagId) REFERENCES `Verlag` (`VerlagId`);
ALTER TABLE `Buch` ADD FOREIGN KEY (SorteId) REFERENCES `Sorte` (`SorteId`);
ALTER TABLE `Ausleihe` ADD FOREIGN KEY (AusleiherId) REFERENCES `Ausleiher` (`AusleiherId`);
ALTER TABLE `Ausleihe` ADD FOREIGN KEY (MediumId) REFERENCES `Buch` (`ISBN`);
ALTER TABLE `AutorBuchZuord` ADD FOREIGN KEY (AutorId) REFERENCES `Autor` (`AutorId`);
ALTER TABLE `AutorBuchZuord` ADD FOREIGN KEY (ISBN) REFERENCES `Buch` (`ISBN`);
ALTER TABLE `Autor` ADD FOREIGN KEY (PersonenId) REFERENCES `Person` (`PersonenId`);
ALTER TABLE `Ausleiher` ADD FOREIGN KEY (PersonenId) REFERENCES `Person` (`PersonenId`);
ALTER TABLE `Ebooks` ADD FOREIGN KEY (BuchISBN) REFERENCES `Buch` (`ISBN`);
ALTER TABLE `Sprecher` ADD FOREIGN KEY (PersonenId) REFERENCES `Person` (`PersonenId`);
ALTER TABLE `Video` ADD FOREIGN KEY (NichtTextMedienId) REFERENCES `NichtTextMedien` (`NichtTextMedienId`);
ALTER TABLE `Hoerbuch` ADD FOREIGN KEY (BuchISBN) REFERENCES `Buch` (`ISBN`);
ALTER TABLE `Hoerbuch` ADD FOREIGN KEY (SprecherId) REFERENCES `Sprecher` (`SprecherId`);
ALTER TABLE `Hoerbuch` ADD FOREIGN KEY (VerlagId) REFERENCES `Verlag` (`VerlagId`);
ALTER TABLE `Bild` ADD FOREIGN KEY (NichtTextMedienId) REFERENCES `NichtTextMedien` (`NichtTextMedienId`);
ALTER TABLE `Bild` ADD FOREIGN KEY (MalerId) REFERENCES `Maler` (`MalerId`);
ALTER TABLE `MediumWortZuord` ADD FOREIGN KEY (MediumId) REFERENCES `Buch` (`ISBN`);
ALTER TABLE `MediumWortZuord` ADD FOREIGN KEY (Wort) REFERENCES `Schlagwort` (`Wort`);
ALTER TABLE `Maler` ADD FOREIGN KEY (PersonenId) REFERENCES `Person` (`PersonenId`);
ALTER TABLE `NichtTextMedien` ADD FOREIGN KEY (SorteId) REFERENCES `Sorte` (`SorteId`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `Buch` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Person` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Ausleihe` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `AutorBuchZuord` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Autor` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Ausleiher` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Schlagwort` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Sorte` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Verlag` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Ebooks` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Sprecher` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Video` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Hoerbuch` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Bild` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `MediumWortZuord` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `Maler` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `NichtTextMedien` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `Buch` (`ISBN`,`Titel`,`Untertitel`,`VerlagId`,`Erscheinungsjahr`,`SorteId`,`Kurzbeschreibung`,`Preis`,`Auflage`,`Sprache`) VALUES
-- ('','','','','','','','','','');
-- INSERT INTO `Person` (`PersonenId`,`Vorname`,`Name`,`Email`,`Geburtsdatum`) VALUES
-- ('','','','','');
-- INSERT INTO `Ausleihe` (`TransaktionsId`,`AusleiherId`,`MediumId`,`Ausleihdatum`,`Rückgabedatum`) VALUES
-- ('','','','','');
-- INSERT INTO `AutorBuchZuord` (`AutorId`,`ISBN`) VALUES
-- ('','');
-- INSERT INTO `Autor` (`AutorId`,`PersonenId`,`Beschreibung`) VALUES
-- ('','','');
-- INSERT INTO `Ausleiher` (`AusleiherId`,`PersonenId`,`Strasse`,`Postleitzahl`,`Ort`,`Telefonnummer`) VALUES
-- ('','','','','','');
-- INSERT INTO `Schlagwort` (`Wort`,`Beschreibung`) VALUES
-- ('','');
-- INSERT INTO `Sorte` (`SorteId`,`Name`,`Beschreibung`) VALUES
-- ('','','');
-- INSERT INTO `Verlag` (`VerlagId`,`Kurzname`,`Name`,`Postleitzahl`,`Strasse`,`Internetadresse`,`Beschreibung`) VALUES
-- ('','','','','','','');
-- INSERT INTO `Ebooks` (`ISBN`,`BuchISBN`,`Dateiformat`) VALUES
-- ('','','');
-- INSERT INTO `Sprecher` (`SprecherId`,`PersonenId`,`Beschreibung`) VALUES
-- ('','','');
-- INSERT INTO `Video` (`VideoId`,`NichtTextMedienId`,`Sprache`) VALUES
-- ('','','');
-- INSERT INTO `Hoerbuch` (`ISBN`,`BuchISBN`,`SprecherId`,`VerlagId`) VALUES
-- ('','','','');
-- INSERT INTO `Bild` (`BildId`,`NichtTextMedienId`,`Bild`,`MalerId`) VALUES
-- ('','','','');
-- INSERT INTO `MediumWortZuord` (`MediumId`,`Wort`) VALUES
-- ('','');
-- INSERT INTO `Maler` (`MalerId`,`PersonenId`,`Beschreibung`) VALUES
-- ('','','');
-- INSERT INTO `NichtTextMedien` (`NichtTextMedienId`,`Titel`,`Untertitel`,`Erscheinungsjahr`,`Kurzbeschreibung`,`SorteId`,`Typ`) VALUES
-- ('','','','','','','');
