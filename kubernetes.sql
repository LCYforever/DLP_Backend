/*
Navicat MySQL Data Transfer

Source Server         : deepnex
Source Server Version : 50720
Source Host           : localhost:3306
Source Database       : kubernetes

Target Server Type    : MYSQL
Target Server Version : 50720
File Encoding         : 65001

Date: 2018-04-13 14:46:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('c0569015245a');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `namespace` varchar(128) DEFAULT NULL,
  `auth_level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'long', 'pbkdf2:sha256:50000$DqyKaEnB$e7d7ed3b8f210a55724cb017aff1601518b72001d531371087b43970a17c830b', 'netlab301', '1');
INSERT INTO `user` VALUES ('2', 'run', 'pbkdf2:sha256:50000$pOdOqa2s$93bdec08aca957c09b311f4ae58e771ad4cbde9eb150795a60070b220de9548f', null, '0');
