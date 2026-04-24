/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: univ_music
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actualites`
--

DROP TABLE IF EXISTS `actualites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `actualites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titre` varchar(150) NOT NULL,
  `resume` varchar(300) NOT NULL,
  `contenu` text NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `date_publication` datetime DEFAULT NULL,
  `categorie_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `categorie_id` (`categorie_id`),
  CONSTRAINT `actualites_ibfk_1` FOREIGN KEY (`categorie_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actualites`
--

LOCK TABLES `actualites` WRITE;
/*!40000 ALTER TABLE `actualites` DISABLE KEYS */;
INSERT INTO `actualites` VALUES
(1,'Le retour de la French Touch','Un nouvel album très attendu pour cet été.','Les plus grands DJ français se réunissent pour une compilation historique...','https://m.media-amazon.com/images/I/71wvSC4pyHL._AC_UF1000,1000_QL80_.jpg','2026-04-24 14:51:23',2),
(2,'Vous l\'aviez oublié ? Pas lui !','Il est de retour ! Le King of POP !','Venez revivre le prime des années 80 en live !','https://m.media-amazon.com/images/I/71CT3oWpR6L._UF894,1000_QL80_.jpg','2026-04-24 15:31:04',6);
/*!40000 ALTER TABLE `actualites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titre` varchar(80) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES
(1,'Rock','Tout sur la musique Rock. ROCK AND ROLL !'),
(2,'Electro','Musique électronique'),
(3,'RAP','Pour ceux qui aiment contester la société'),
(4,'Jazz','Pour se reposer au lounge, whiskey et cigare à la main'),
(5,'Classique','Pour le raffinement et l\'élégance'),
(6,'POP','Parce qu\'il n\'y a qu\'un seul roi.');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commentaires`
--

DROP TABLE IF EXISTS `commentaires`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `commentaires` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auteur` varchar(80) NOT NULL,
  `contenu` varchar(300) NOT NULL,
  `date_post` datetime DEFAULT NULL,
  `concert_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `concert_id` (`concert_id`),
  CONSTRAINT `commentaires_ibfk_1` FOREIGN KEY (`concert_id`) REFERENCES `concerts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commentaires`
--

LOCK TABLES `commentaires` WRITE;
/*!40000 ALTER TABLE `commentaires` DISABLE KEYS */;
/*!40000 ALTER TABLE `commentaires` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `concerts`
--

DROP TABLE IF EXISTS `concerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `concerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titre` varchar(150) NOT NULL,
  `lieu` varchar(120) NOT NULL,
  `ville` varchar(80) NOT NULL,
  `date_concert` date NOT NULL,
  `places_totales` int(11) NOT NULL,
  `description` text NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `avis_redacteur` text DEFAULT NULL,
  `categorie_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `categorie_id` (`categorie_id`),
  CONSTRAINT `concerts_ibfk_1` FOREIGN KEY (`categorie_id`) REFERENCES `categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `concerts`
--

LOCK TABLES `concerts` WRITE;
/*!40000 ALTER TABLE `concerts` DISABLE KEYS */;
INSERT INTO `concerts` VALUES
(1,'Musilac 2026','Esplanade du Lac','Aix-les-Bains','2026-07-10',15000,'Le plus grand festival pop-rock de la région revient fort !','https://media.gqmagazine.fr/photos/642fd954abd92836c899cf75/3:2/w_1619,h_1079,c_limit/therock.jpg','ROCK AND STONE !',1),
(2,'FestiJazz 2k26','Carré Curial','Chambéry','2026-04-30',67,'Venez vous détendre et apprécier un bon moment avec de la bonne musique au coin du feu...','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRalwAt8fCdrSWdaBUk-ck24XJcj_C7MgA4lJGDBgg1MF4LWRSgs99XN204EaB3v08-_fGWjXw5JkiKMSAQ-k-zdjpD8ft2CE2l7USJPbs&s=10','Parfait pour se refaire un parcours de jazz des années folles !',4),
(3,'KAARISSE','Lac du Bourget','Bourget du Lac','2026-05-08',45000,'LES SINGES VIENNENT DE SORTIR DU ZOO','https://leflow.tv/wp-content/uploads/2024/03/kaaris_or-noir_viusnews0224.jpg','VENEZ A LA FOSSE',3),
(4,'FANTASIA','Parc des princes','Paris','2025-07-09',55,'Un moment de douceur et de tendresse avec le meilleur de la musique classique','https://upload.wikimedia.org/wikipedia/commons/6/6a/Johann_Sebastian_Bach.jpg','Un pur moment de plaisir !',5);
/*!40000 ALTER TABLE `concerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `places` int(11) NOT NULL,
  `date_reservation` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `concert_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `concert_id` (`concert_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`concert_id`) REFERENCES `concerts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES
(1,10,'2026-04-24 15:05:33',2,1);
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'Root Admin','root@root.com','scrypt:32768:8:1$9QqciSECPLxPzON2$dfae7e12f71e2eb119e592806db5ca6129b5a2e6d563391d7dd90e75da92ffe52db971ee515e996ffd9aaf8ba2a961418fec66e21aa3825877cd96621258989f',1),
(2,'test','aaaa@aaaa.com','scrypt:32768:8:1$jSFfs09Bay8BXuaw$154d17181a893d12cd842acbf6034fcac648600c31a9152aa8125a9fc0530de8e0ea7cb66fc6f28837f7ff7efbfc701a42de51d756d92ae48d41c5e11d2bf33d',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-24 15:37:52
