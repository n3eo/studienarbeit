-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Erstellungszeit: 26. Mai 2020 um 09:51
-- Server-Version: 5.7.29
-- PHP-Version: 7.4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `nico_studienarbeit`
--

-- --------------------------------------------------------

DROP TABLE IF EXISTS `MediumWortZuord`;
DROP TABLE IF EXISTS `Schlagwort`;

DROP TABLE IF EXISTS `Ausleihe`;

DROP TABLE IF EXISTS `Video`;
DROP TABLE IF EXISTS `Bild`;
DROP TABLE IF EXISTS `NichtTextMedium`;

DROP TABLE IF EXISTS `Ebook`;
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

--
-- Tabellenstruktur für Tabelle `Ausleihe`
--

DROP TABLE IF EXISTS `Ausleihe`;
CREATE TABLE `Ausleihe` (
  `TransaktionsId` int(11) NOT NULL,
  `AusleiherId` int(11) NOT NULL,
  `MediumId` varchar(17) NOT NULL,
  `Ausleihdatum` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Rückgabedatum` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Ausleiher`
--

DROP TABLE IF EXISTS `Ausleiher`;
CREATE TABLE `Ausleiher` (
  `AusleiherId` int(11) NOT NULL,
  `PersonenId` int(11) NOT NULL,
  `Strasse` varchar(50) NOT NULL DEFAULT 'NULL',
  `Postleitzahl` varchar(5) NOT NULL DEFAULT 'NULL',
  `Ort` varchar(30) NOT NULL,
  `Telefonnummer` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Autor`
--

DROP TABLE IF EXISTS `Autor`;
CREATE TABLE `Autor` (
  `AutorId` int(11) NOT NULL,
  `PersonenId` int(11) NOT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `AutorBuchZuord`
--

DROP TABLE IF EXISTS `AutorBuchZuord`;
CREATE TABLE `AutorBuchZuord` (
  `AutorBuchZuordId` int(11) NOT NULL,
  `AutorId` int(11) NOT NULL,
  `ISBN` varchar(17) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Bild`
--

DROP TABLE IF EXISTS `Bild`;
CREATE TABLE `Bild` (
  `BildId` int(11) NOT NULL,
  `NichtTextMediumId` int(13) NOT NULL,
  `Bild` longblob,
  `MalerId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Buch`
--

DROP TABLE IF EXISTS `Buch`;
CREATE TABLE `Buch` (
  `ISBN` varchar(17) NOT NULL,
  `Titel` text NOT NULL,
  `Untertitel` varchar(500) DEFAULT NULL,
  `VerlagId` int(11) DEFAULT NULL,
  `Erscheinungsjahr` smallint(4) DEFAULT NULL,
  `SorteId` int(11) DEFAULT NULL,
  `Kurzbeschreibung` varchar(100) DEFAULT NULL,
  `Preis` decimal(10,3) DEFAULT NULL,
  `Auflage` varchar(20) DEFAULT NULL,
  `Sprache` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Ebook`
--

DROP TABLE IF EXISTS `Ebook`;
CREATE TABLE `Ebook` (
  `ISBN` varchar(17) NOT NULL,
  `BuchISBN` varchar(17) NOT NULL,
  `Dateiformat` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Hoerbuch`
--

DROP TABLE IF EXISTS `Hoerbuch`;
CREATE TABLE `Hoerbuch` (
  `ISBN` varchar(17) NOT NULL,
  `BuchISBN` varchar(17) NOT NULL,
  `SprecherId` int(11) NOT NULL,
  `VerlagId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Maler`
--

DROP TABLE IF EXISTS `Maler`;
CREATE TABLE `Maler` (
  `MalerId` int(11) NOT NULL,
  `PersonenId` int(11) NOT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `MediumWortZuord`
--

DROP TABLE IF EXISTS `MediumWortZuord`;
CREATE TABLE `MediumWortZuord` (
  `MediumWortId` int(11) NOT NULL,
  `MediumId` varchar(17) NOT NULL,
  `Wort` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `NichtTextMedium`
--

DROP TABLE IF EXISTS `NichtTextMedium`;
CREATE TABLE `NichtTextMedium` (
  `NichtTextMediumId` int(13) NOT NULL,
  `Titel` text NOT NULL,
  `Untertitel` varchar(500) DEFAULT NULL,
  `Erscheinungsjahr` smallint(4) DEFAULT NULL,
  `Kurzbeschreibung` mediumtext,
  `SorteId` int(11) NOT NULL,
  `Typ` enum('Bild','Video') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Person`
--

DROP TABLE IF EXISTS `Person`;
CREATE TABLE `Person` (
  `PersonenId` int(11) NOT NULL,
  `Vorname` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(250) DEFAULT NULL,
  `Geburtsdatum` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Schlagwort`
--

DROP TABLE IF EXISTS `Schlagwort`;
CREATE TABLE `Schlagwort` (
  `Wort` varchar(300) NOT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Sorte`
--

DROP TABLE IF EXISTS `Sorte`;
CREATE TABLE `Sorte` (
  `SorteId` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Sprecher`
--

DROP TABLE IF EXISTS `Sprecher`;
CREATE TABLE `Sprecher` (
  `SprecherId` int(11) NOT NULL,
  `PersonenId` int(11) NOT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Verlag`
--

DROP TABLE IF EXISTS `Verlag`;
CREATE TABLE `Verlag` (
  `VerlagId` int(11) NOT NULL,
  `Kurzname` varchar(150) DEFAULT NULL,
  `Name` varchar(300) NOT NULL,
  `Postleitzahl` varchar(5) DEFAULT NULL,
  `Strasse` varchar(50) DEFAULT NULL,
  `Internetadresse` varchar(30) DEFAULT NULL,
  `Beschreibung` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Video`
--

DROP TABLE IF EXISTS `Video`;
CREATE TABLE `Video` (
  `VideoId` int(11) NOT NULL,
  `NichtTextMediumId` int(13) NOT NULL,
  `Sprache` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `Ausleihe`
--
ALTER TABLE `Ausleihe`
  ADD PRIMARY KEY (`TransaktionsId`),
  ADD KEY `AusleiherId` (`AusleiherId`),
  ADD KEY `MediumId` (`MediumId`);

--
-- Indizes für die Tabelle `Ausleiher`
--
ALTER TABLE `Ausleiher`
  ADD PRIMARY KEY (`AusleiherId`),
  ADD KEY `PersonenId` (`PersonenId`);

--
-- Indizes für die Tabelle `Autor`
--
ALTER TABLE `Autor`
  ADD PRIMARY KEY (`AutorId`),
  ADD KEY `PersonenId` (`PersonenId`);

--
-- Indizes für die Tabelle `AutorBuchZuord`
--
ALTER TABLE `AutorBuchZuord`
  ADD PRIMARY KEY (`AutorBuchZuordId`),
  ADD KEY `AutorId` (`AutorId`),
  ADD KEY `ISBN` (`ISBN`);

--
-- Indizes für die Tabelle `Bild`
--
ALTER TABLE `Bild`
  ADD PRIMARY KEY (`BildId`),
  ADD UNIQUE KEY `NichtTextMediumId` (`NichtTextMediumId`),
  ADD KEY `MalerId` (`MalerId`);

--
-- Indizes für die Tabelle `Buch`
--
ALTER TABLE `Buch`
  ADD PRIMARY KEY (`ISBN`),
  ADD KEY `VerlagId` (`VerlagId`),
  ADD KEY `SorteId` (`SorteId`);

--
-- Indizes für die Tabelle `Ebook`
--
ALTER TABLE `Ebook`
  ADD PRIMARY KEY (`ISBN`),
  ADD KEY `BuchISBN` (`BuchISBN`);

--
-- Indizes für die Tabelle `Hoerbuch`
--
ALTER TABLE `Hoerbuch`
  ADD PRIMARY KEY (`ISBN`),
  ADD KEY `BuchISBN` (`BuchISBN`),
  ADD KEY `SprecherId` (`SprecherId`),
  ADD KEY `VerlagId` (`VerlagId`);

--
-- Indizes für die Tabelle `Maler`
--
ALTER TABLE `Maler`
  ADD PRIMARY KEY (`MalerId`),
  ADD KEY `PersonenId` (`PersonenId`);

--
-- Indizes für die Tabelle `MediumWortZuord`
--
ALTER TABLE `MediumWortZuord`
  ADD PRIMARY KEY (`MediumWortId`),
  ADD KEY `MediumId` (`MediumId`),
  ADD KEY `Wort` (`Wort`);

--
-- Indizes für die Tabelle `NichtTextMedium`
--
ALTER TABLE `NichtTextMedium`
  ADD PRIMARY KEY (`NichtTextMediumId`),
  ADD KEY `SorteId` (`SorteId`);

--
-- Indizes für die Tabelle `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`PersonenId`);

--
-- Indizes für die Tabelle `Schlagwort`
--
ALTER TABLE `Schlagwort`
  ADD PRIMARY KEY (`Wort`);

--
-- Indizes für die Tabelle `Sorte`
--
ALTER TABLE `Sorte`
  ADD PRIMARY KEY (`SorteId`);

--
-- Indizes für die Tabelle `Sprecher`
--
ALTER TABLE `Sprecher`
  ADD PRIMARY KEY (`SprecherId`),
  ADD KEY `PersonenId` (`PersonenId`);

--
-- Indizes für die Tabelle `Verlag`
--
ALTER TABLE `Verlag`
  ADD PRIMARY KEY (`VerlagId`);

--
-- Indizes für die Tabelle `Video`
--
ALTER TABLE `Video`
  ADD PRIMARY KEY (`VideoId`),
  ADD UNIQUE KEY `NichtTextMediumId` (`NichtTextMediumId`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Ausleihe`
--
ALTER TABLE `Ausleihe`
  MODIFY `TransaktionsId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Ausleiher`
--
ALTER TABLE `Ausleiher`
  MODIFY `AusleiherId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Autor`
--
ALTER TABLE `Autor`
  MODIFY `AutorId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `AutorBuchZuord`
--
ALTER TABLE `AutorBuchZuord`
  MODIFY `AutorBuchZuordId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Bild`
--
ALTER TABLE `Bild`
  MODIFY `BildId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Maler`
--
ALTER TABLE `Maler`
  MODIFY `MalerId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `MediumWortZuord`
--
ALTER TABLE `MediumWortZuord`
  MODIFY `MediumWortId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `NichtTextMedium`
--
ALTER TABLE `NichtTextMedium`
  MODIFY `NichtTextMediumId` int(13) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Person`
--
ALTER TABLE `Person`
  MODIFY `PersonenId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Sorte`
--
ALTER TABLE `Sorte`
  MODIFY `SorteId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Sprecher`
--
ALTER TABLE `Sprecher`
  MODIFY `SprecherId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Verlag`
--
ALTER TABLE `Verlag`
  MODIFY `VerlagId` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Video`
--
ALTER TABLE `Video`
  MODIFY `VideoId` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Ausleihe`
--
ALTER TABLE `Ausleihe`
  ADD CONSTRAINT `Ausleihe_ibfk_1` FOREIGN KEY (`AusleiherId`) REFERENCES `Ausleiher` (`AusleiherId`),
  ADD CONSTRAINT `Ausleihe_ibfk_2` FOREIGN KEY (`MediumId`) REFERENCES `Buch` (`ISBN`);

--
-- Constraints der Tabelle `Ausleiher`
--
ALTER TABLE `Ausleiher`
  ADD CONSTRAINT `Ausleiher_ibfk_1` FOREIGN KEY (`PersonenId`) REFERENCES `Person` (`PersonenId`);

--
-- Constraints der Tabelle `Autor`
--
ALTER TABLE `Autor`
  ADD CONSTRAINT `Autor_ibfk_1` FOREIGN KEY (`PersonenId`) REFERENCES `Person` (`PersonenId`);

--
-- Constraints der Tabelle `AutorBuchZuord`
--
ALTER TABLE `AutorBuchZuord`
  ADD CONSTRAINT `AutorBuchZuord_ibfk_1` FOREIGN KEY (`AutorId`) REFERENCES `Autor` (`AutorId`),
  ADD CONSTRAINT `AutorBuchZuord_ibfk_2` FOREIGN KEY (`ISBN`) REFERENCES `Buch` (`ISBN`);

--
-- Constraints der Tabelle `Bild`
--
ALTER TABLE `Bild`
  ADD CONSTRAINT `Bild_ibfk_1` FOREIGN KEY (`NichtTextMediumId`) REFERENCES `NichtTextMedium` (`NichtTextMediumId`),
  ADD CONSTRAINT `Bild_ibfk_2` FOREIGN KEY (`MalerId`) REFERENCES `Maler` (`MalerId`);

--
-- Constraints der Tabelle `Buch`
--
ALTER TABLE `Buch`
  ADD CONSTRAINT `Buch_ibfk_1` FOREIGN KEY (`VerlagId`) REFERENCES `Verlag` (`VerlagId`),
  ADD CONSTRAINT `Buch_ibfk_2` FOREIGN KEY (`SorteId`) REFERENCES `Sorte` (`SorteId`);

--
-- Constraints der Tabelle `Ebook`
--
ALTER TABLE `Ebook`
  ADD CONSTRAINT `Ebook_ibfk_1` FOREIGN KEY (`BuchISBN`) REFERENCES `Buch` (`ISBN`);

--
-- Constraints der Tabelle `Hoerbuch`
--
ALTER TABLE `Hoerbuch`
  ADD CONSTRAINT `Hoerbuch_ibfk_1` FOREIGN KEY (`BuchISBN`) REFERENCES `Buch` (`ISBN`),
  ADD CONSTRAINT `Hoerbuch_ibfk_2` FOREIGN KEY (`SprecherId`) REFERENCES `Sprecher` (`SprecherId`),
  ADD CONSTRAINT `Hoerbuch_ibfk_3` FOREIGN KEY (`VerlagId`) REFERENCES `Verlag` (`VerlagId`);

--
-- Constraints der Tabelle `Maler`
--
ALTER TABLE `Maler`
  ADD CONSTRAINT `Maler_ibfk_1` FOREIGN KEY (`PersonenId`) REFERENCES `Person` (`PersonenId`);

--
-- Constraints der Tabelle `MediumWortZuord`
--
ALTER TABLE `MediumWortZuord`
  ADD CONSTRAINT `MediumWortZuord_ibfk_1` FOREIGN KEY (`MediumId`) REFERENCES `Buch` (`ISBN`),
  ADD CONSTRAINT `MediumWortZuord_ibfk_2` FOREIGN KEY (`Wort`) REFERENCES `Schlagwort` (`Wort`);

--
-- Constraints der Tabelle `NichtTextMedium`
--
ALTER TABLE `NichtTextMedium`
  ADD CONSTRAINT `NichtTextMedium_ibfk_1` FOREIGN KEY (`SorteId`) REFERENCES `Sorte` (`SorteId`);

--
-- Constraints der Tabelle `Sprecher`
--
ALTER TABLE `Sprecher`
  ADD CONSTRAINT `Sprecher_ibfk_1` FOREIGN KEY (`PersonenId`) REFERENCES `Person` (`PersonenId`);

--
-- Constraints der Tabelle `Video`
--
ALTER TABLE `Video`
  ADD CONSTRAINT `Video_ibfk_1` FOREIGN KEY (`NichtTextMediumId`) REFERENCES `NichtTextMedium` (`NichtTextMediumId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
