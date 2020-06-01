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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
