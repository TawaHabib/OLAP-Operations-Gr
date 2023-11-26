-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: vendite_data_mart
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `d_prodotto`
--

DROP TABLE IF EXISTS `d_prodotto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_prodotto` (
  `ID` int NOT NULL,
  `PRODOTTO` varchar(45) DEFAULT NULL,
  `SUB_CATEGORIA` varchar(45) DEFAULT NULL,
  `CATEGORIA` varchar(45) DEFAULT NULL,
  `TIPO` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_sede`
--

DROP TABLE IF EXISTS `d_sede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_sede` (
  `ID` int NOT NULL,
  `FILIALE` varchar(45) DEFAULT NULL,
  `CITTA` varchar(45) DEFAULT NULL,
  `REGIONE` varchar(45) DEFAULT NULL,
  `PAESE` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_tempo`
--

DROP TABLE IF EXISTS `d_tempo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `d_tempo` (
  `ID` int NOT NULL,
  `DATA` date DEFAULT NULL,
  `SETTIMANA` varchar(45) DEFAULT NULL,
  `MESE` varchar(45) DEFAULT NULL,
  `TRIMESTRE` varchar(45) DEFAULT NULL,
  `ANNO` year DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `denormalized_data_mart`
--

DROP TABLE IF EXISTS `denormalized_data_mart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `denormalized_data_mart` (
  `TEMPO_ID` int DEFAULT NULL,
  `SEDE_ID` int DEFAULT NULL,
  `PRODOTTO_ID` int DEFAULT NULL,
  `INCASSO` double DEFAULT NULL,
  `NUMERO_CLIENTI` int DEFAULT NULL,
  `QUANTITA` int DEFAULT NULL,
  `PRODOTTO` varchar(45) DEFAULT NULL,
  `SUB_CATEGORIA` varchar(45) DEFAULT NULL,
  `CATEGORIA` varchar(45) DEFAULT NULL,
  `TIPO` varchar(45) DEFAULT NULL,
  `FILIALE` varchar(45) DEFAULT NULL,
  `CITTA` varchar(45) DEFAULT NULL,
  `REGIONE` varchar(45) DEFAULT NULL,
  `PAESE` varchar(45) DEFAULT NULL,
  `DATA` date DEFAULT NULL,
  `SETTIMANA` varchar(45) DEFAULT NULL,
  `MESE` varchar(45) DEFAULT NULL,
  `TRIMESTRE` varchar(45) DEFAULT NULL,
  `ANNO` year DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `denormalized_month_data_mart`
--

DROP TABLE IF EXISTS `denormalized_month_data_mart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `denormalized_month_data_mart` (
  `SEDE_ID` int DEFAULT NULL,
  `PRODOTTO_ID` int DEFAULT NULL,
  `INCASSO` double DEFAULT NULL,
  `NUMERO_CLIENTI` int DEFAULT NULL,
  `QUANTITA` int DEFAULT NULL,
  `PRODOTTO` varchar(45) DEFAULT NULL,
  `SUB_CATEGORIA` varchar(45) DEFAULT NULL,
  `CATEGORIA` varchar(45) DEFAULT NULL,
  `TIPO` varchar(45) DEFAULT NULL,
  `FILIALE` varchar(45) DEFAULT NULL,
  `CITTA` varchar(45) DEFAULT NULL,
  `REGIONE` varchar(45) DEFAULT NULL,
  `PAESE` varchar(45) DEFAULT NULL,
  `MESE` varchar(45) DEFAULT NULL,
  `TRIMESTRE` varchar(45) DEFAULT NULL,
  `ANNO` year DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `denormalized_week_data_mart`
--

DROP TABLE IF EXISTS `denormalized_week_data_mart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `denormalized_week_data_mart` (
  `SEDE_ID` int DEFAULT NULL,
  `PRODOTTO_ID` int DEFAULT NULL,
  `INCASSO` double DEFAULT NULL,
  `NUMERO_CLIENTI` int DEFAULT NULL,
  `QUANTITA` int DEFAULT NULL,
  `PRODOTTO` varchar(45) DEFAULT NULL,
  `SUB_CATEGORIA` varchar(45) DEFAULT NULL,
  `CATEGORIA` varchar(45) DEFAULT NULL,
  `TIPO` varchar(45) DEFAULT NULL,
  `FILIALE` varchar(45) DEFAULT NULL,
  `CITTA` varchar(45) DEFAULT NULL,
  `REGIONE` varchar(45) DEFAULT NULL,
  `PAESE` varchar(45) DEFAULT NULL,
  `SETTIMANA` varchar(45) DEFAULT NULL,
  `MESE` varchar(45) DEFAULT NULL,
  `TRIMESTRE` varchar(45) DEFAULT NULL,
  `ANNO` year DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `f_vendita`
--

DROP TABLE IF EXISTS `f_vendita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `f_vendita` (
  `TEMPO_ID` int NOT NULL,
  `SEDE_ID` int NOT NULL,
  `PRODOTTO_ID` int NOT NULL,
  `QUANTITÀ` int DEFAULT NULL,
  `INCASSO` double DEFAULT NULL,
  `NUMERO_CLIENTI` int DEFAULT NULL,
  PRIMARY KEY (`TEMPO_ID`,`SEDE_ID`,`PRODOTTO_ID`),
  KEY `fk_F_Vendita_D_Tempo_idx` (`TEMPO_ID`),
  KEY `fk_F_Vendita_D_Sede1_idx` (`SEDE_ID`),
  KEY `fk_F_Vendita_D_Prodotto1_idx` (`PRODOTTO_ID`),
  CONSTRAINT `fk_F_Vendita_D_Prodotto1` FOREIGN KEY (`PRODOTTO_ID`) REFERENCES `d_prodotto` (`ID`),
  CONSTRAINT `fk_F_Vendita_D_Sede1` FOREIGN KEY (`SEDE_ID`) REFERENCES `d_sede` (`ID`),
  CONSTRAINT `fk_F_Vendita_D_Tempo` FOREIGN KEY (`TEMPO_ID`) REFERENCES `d_tempo` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-26 15:05:45
