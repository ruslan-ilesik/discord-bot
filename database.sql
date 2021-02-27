-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: DS_bot
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comands_servers_permisions`
--

DROP TABLE IF EXISTS `comands_servers_permisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comands_servers_permisions` (
  `server_id` varchar(20) NOT NULL,
  `command` varchar(20) NOT NULL,
  `white_list` json NOT NULL,
  `black_list` json NOT NULL,
  PRIMARY KEY (`server_id`,`command`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `custom_roles`
--

DROP TABLE IF EXISTS `custom_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `custom_roles` (
  `server_id` varchar(20) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `role_id` varchar(20) NOT NULL,
  `role_time_to_delete_from_user` varchar(12) NOT NULL,
  `time_to_delete_role` varchar(12) NOT NULL DEFAULT '999999999999',
  PRIMARY KEY (`server_id`,`user_id`,`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lotterys`
--

DROP TABLE IF EXISTS `lotterys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotterys` (
  `name` varchar(45) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `data` json NOT NULL,
  PRIMARY KEY (`name`,`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phrases`
--

DROP TABLE IF EXISTS `phrases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phrases` (
  `phrase` varchar(300) NOT NULL,
  `type` varchar(20) NOT NULL,
  `is_for_female` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`type`,`phrase`,`is_for_female`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `servers_data`
--

DROP TABLE IF EXISTS `servers_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servers_data` (
  `server_id` varchar(20) NOT NULL,
  `new_member_message` varchar(2000) DEFAULT NULL,
  `mute_role_id` varchar(20) DEFAULT NULL,
  `work_chanel_ids` json DEFAULT NULL,
  `mute_messages_delay_in_seconds` int DEFAULT NULL,
  `shop` json NOT NULL,
  `sub_role_id` varchar(20) DEFAULT NULL,
  `bot_admins` json NOT NULL,
  `bot_moderators` json NOT NULL,
  `channel_to_send_game_distributions` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `servers_user_data`
--

DROP TABLE IF EXISTS `servers_user_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servers_user_data` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `balance` int NOT NULL DEFAULT '0',
  `last_balance_add_time` int NOT NULL DEFAULT '0',
  `kicks_give` int NOT NULL DEFAULT '0',
  `kicks_take` int NOT NULL DEFAULT '0',
  `hugs_give` int NOT NULL DEFAULT '0',
  `hugs_take` int NOT NULL DEFAULT '0',
  `money_spent_all_time` int NOT NULL DEFAULT '0',
  `casino_times_played` int NOT NULL DEFAULT '0',
  `casino_win_times` int NOT NULL DEFAULT '0',
  `casino_lose_times` int NOT NULL DEFAULT '0',
  `casino_money_win` int NOT NULL DEFAULT '0',
  `casino_money_lose` int NOT NULL DEFAULT '0',
  `transfer_money_give_at_all` int NOT NULL DEFAULT '0',
  `transfer_money_take_at_all` int NOT NULL DEFAULT '0',
  `transfer_give_times` int NOT NULL DEFAULT '0',
  `transfer_take_times` int NOT NULL DEFAULT '0',
  `amount_of_bought_products` int NOT NULL DEFAULT '0',
  `money_spent_in_shop` int NOT NULL DEFAULT '0',
  `is_female` tinyint NOT NULL DEFAULT '0',
  `money_spent_in_lottery` int NOT NULL DEFAULT '0',
  `lottery_played_times` int NOT NULL DEFAULT '0',
  `lottery_win_times` int NOT NULL DEFAULT '0',
  `lottery_lose_times` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`,`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_in_mute`
--

DROP TABLE IF EXISTS `users_in_mute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_in_mute` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `amount_of_captcha` int NOT NULL,
  `last_answer_time` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-02-27 17:39:16
