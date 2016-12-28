/*
Navicat MySQL Data Transfer

Source Server         : 192.168.37.57
Source Server Version : 50161
Source Host           : 192.168.37.57:3306
Source Database       : music

Target Server Type    : MYSQL
Target Server Version : 50161
File Encoding         : 65001

Date: 2016-12-28 16:19:16
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `t_followed_info`
-- ----------------------------
DROP TABLE IF EXISTS `t_followed_info`;
CREATE TABLE `t_followed_info` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `f_parent_id` int(11) DEFAULT NULL,
  `f_child_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`f_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_followed_info
-- ----------------------------

-- ----------------------------
-- Table structure for `t_user_info`
-- ----------------------------
DROP TABLE IF EXISTS `t_user_info`;
CREATE TABLE `t_user_info` (
  `f_id` int(11) NOT NULL AUTO_INCREMENT,
  `f_user_id` int(11) DEFAULT '0' COMMENT '用户的id',
  `f_songs` int(11) DEFAULT NULL COMMENT '听的歌曲数',
  `f_nick_name` varchar(255) DEFAULT NULL COMMENT '昵称',
  `f_follow_count` int(255) DEFAULT NULL,
  `f_fan_count` int(11) DEFAULT NULL,
  `f_area` varchar(255) DEFAULT NULL COMMENT '区域',
  PRIMARY KEY (`f_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of t_user_info
-- ----------------------------
