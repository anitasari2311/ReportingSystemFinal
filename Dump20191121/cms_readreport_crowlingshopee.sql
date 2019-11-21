-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: cms_readreport
-- ------------------------------------------------------
-- Server version	5.7.25-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `crowlingshopee`
--

DROP TABLE IF EXISTS `crowlingshopee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `crowlingshopee` (
  `noPesanan` varchar(500) DEFAULT NULL,
  `statusPesanan` varchar(500) DEFAULT NULL,
  `noResi` varchar(500) DEFAULT NULL,
  `opsiPengiriman` varchar(500) DEFAULT NULL,
  `opsiPengantaran` varchar(500) DEFAULT NULL,
  `deadlineKirim` datetime DEFAULT NULL,
  `waktuPesananDiBuat` datetime DEFAULT NULL,
  `waktuPembayaran` datetime DEFAULT NULL,
  `namaProduk` varchar(500) DEFAULT NULL,
  `hargaSebelumDiskon` int(11) DEFAULT NULL,
  `hargaSetelahDiskon` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `beratProduk` int(11) DEFAULT NULL,
  `jumlahProdukDiPesan` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `crowlingshopee`
--

LOCK TABLES `crowlingshopee` WRITE;
/*!40000 ALTER TABLE `crowlingshopee` DISABLE KEYS */;
/*!40000 ALTER TABLE `crowlingshopee` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-21  9:52:41
