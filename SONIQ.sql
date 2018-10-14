-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server versie:                10.2.16-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Versie:              9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Databasestructuur van soniq wordt geschreven
CREATE DATABASE IF NOT EXISTS `soniq` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `soniq`;

-- Structuur van  tabel soniq.fingerprints wordt geschreven
CREATE TABLE IF NOT EXISTS `fingerprints` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `song_id` smallint(5) unsigned NOT NULL DEFAULT 0,
  `fingerprint` binary(8) NOT NULL DEFAULT '0\0\0\0\0\0\0\0',
  `time` mediumint(8) unsigned DEFAULT 0,
  KEY `id` (`id`),
  KEY `fingerprint_index` (`fingerprint`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporteren was gedeselecteerd
-- Structuur van  tabel soniq.songs wordt geschreven
CREATE TABLE IF NOT EXISTS `songs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` char(100) DEFAULT '0',
  `title` char(100) DEFAULT NULL,
  `artist` char(100) DEFAULT NULL,
  `fingerprinted` tinyint(4) DEFAULT 0,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporteren was gedeselecteerd
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
