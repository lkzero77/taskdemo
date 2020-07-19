-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 19, 2020 at 06:28 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.3.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tasks`
--

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `assign_user_id` int(11) DEFAULT NULL,
  `name` varchar(500) NOT NULL,
  `description` text NOT NULL,
  `status` enum('waiting','working','issued','processing','done') NOT NULL DEFAULT 'waiting',
  `date_of_submission` datetime DEFAULT NULL,
  `isShow` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`id`, `assign_user_id`, `name`, `description`, `status`, `date_of_submission`, `isShow`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1, 2, 'ticket 1  sdsdf', 'ticket 1 description adsd dsff adaf', 'processing', '2020-07-29 00:00:00', 1, '2020-07-16 06:34:57', 'admin', '2020-07-18 15:56:08', 'admin'),
(2, 2, 'ticket 2', 'ticket 2 description', 'processing', '2020-07-29 00:00:00', 0, '2020-07-16 04:18:10', 'demo', '2020-07-18 15:36:55', 'admin'),
(3, 2, 'ticket 2', 'ticket 2 description', 'issued', '2020-07-31 00:00:00', 1, '2020-07-17 09:41:50', 'demo', '2020-07-18 09:23:34', 'admin'),
(4, 2, 'ticket 4', 'ticket 4 description', 'waiting', '2020-07-31 00:00:00', 0, '2020-07-17 09:42:18', 'demo', '2020-07-18 07:11:19', 'admin'),
(5, 2, 'ticket 4', 'ticket 4 description', 'working', '2020-07-04 00:00:00', 1, '2020-07-17 09:42:50', 'demo', '2020-07-17 17:41:09', 'admin'),
(6, 2, 'ticket 4', 'ticket 4 description', 'issued', '2020-07-16 00:00:00', 1, '2020-07-17 09:44:03', 'demo', '2020-07-17 17:41:05', 'admin'),
(7, 2, 'ticket 4', 'ticket 4 description', 'issued', '2020-07-30 00:00:00', 1, '2020-07-17 09:44:32', 'demo', '2020-07-17 17:31:24', 'admin'),
(8, 2, 'ticket 4', 'ticket 4 description', 'working', '2020-07-31 00:00:00', 1, '2020-07-17 09:44:32', 'demo', '2020-07-17 17:32:24', 'admin'),
(9, 2, 'ticket 4', 'ticket 4 description', 'working', '2020-07-28 00:00:00', 1, '2020-07-17 09:44:32', 'demo', '2020-07-18 00:58:58', 'admin'),
(10, 2, 'ticket 4 sdfdf', 'ticket 4 description', 'processing', '2020-07-30 00:00:00', 1, '2020-07-17 09:44:32', 'demo', '2020-07-18 15:58:07', 'admin'),
(11, 2, 'ticket 4', 'ticket 4 description', 'waiting', '2020-07-31 00:00:00', 1, '2020-07-17 09:50:40', 'demo', '2020-07-18 00:58:41', 'admin'),
(12, 2, 'ticket 4', 'ticket 4 description', 'waiting', NULL, 1, '2020-07-17 10:56:35', 'demo', NULL, NULL),
(13, 1, 'ticket so 3', 'lam cai ticket so 3', 'waiting', '2020-07-17 17:58:24', 1, '2020-07-17 10:58:46', 'admin', NULL, NULL),
(14, NULL, 'sfs ', 'sdfsf', 'waiting', NULL, 1, '2020-07-17 11:01:50', 'admin', NULL, NULL),
(15, NULL, 'tie asfsfa', 'dfsnsfdfs', 'waiting', NULL, 1, '2020-07-18 13:38:20', 'admin', NULL, NULL),
(16, NULL, 'asdadad', 'asdadad', 'waiting', NULL, 1, '2020-07-18 13:39:56', 'admin', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `role` enum('admin','normal') CHARACTER SET utf8 NOT NULL DEFAULT 'normal',
  `isActived` tinyint(1) NOT NULL DEFAULT 0,
  `remember_token` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `timezone` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `email_verified_at`, `role`, `isActived`, `remember_token`, `timezone`, `created_at`, `updated_at`) VALUES
(1, 'admin', '183286df04eb99fa9df1d6672e75e7d4', 'admin@admin.com', NULL, 'admin', 1, NULL, NULL, '2020-07-15 18:11:56', '2020-07-15 18:11:56'),
(2, 'test', '183286df04eb99fa9df1d6672e75e7d4', 'test@test.com', NULL, 'normal', 1, NULL, NULL, '2020-07-15 18:11:56', '2020-07-15 18:11:56'),
(3, 'demo', '183286df04eb99fa9df1d6672e75e7d4', 'demo@demo.com', NULL, 'normal', 1, NULL, NULL, '2020-07-15 19:05:00', NULL),
(4, 'demo1', '183286df04eb99fa9df1d6672e75e7d4', 'demo1@demo1.com', NULL, 'normal', 1, NULL, NULL, '2020-07-15 19:07:30', NULL),
(15, 'emo', '183286df04eb99fa9df1d6672e75e7d4', 'emo@emo.com', NULL, 'normal', 0, NULL, NULL, '2020-07-18 16:16:40', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
