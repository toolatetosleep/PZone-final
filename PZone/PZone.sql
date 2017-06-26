/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50610
Source Host           : localhost:3306
Source Database       : pzone

Target Server Type    : MYSQL
Target Server Version : 50610
File Encoding         : 65001

Date: 2017-06-07 16:21:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for pz_cache_table
-- ----------------------------
DROP TABLE IF EXISTS `pz_cache_table`;
CREATE TABLE `pz_cache_table` (
  `cache_key` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `expires` datetime NOT NULL,
  PRIMARY KEY (`cache_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pz_comment
-- ----------------------------
DROP TABLE IF EXISTS `pz_comment`;
CREATE TABLE `pz_comment` (
  `c_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论 ID 主键',
  `c_user_give` int(11) NOT NULL DEFAULT '0' COMMENT '发布人',
  `c_user_recive` int(11) NOT NULL DEFAULT '0' COMMENT '接收人',
  `c_category` int(6) NOT NULL DEFAULT '0' COMMENT '分区标记（1头条、2技巧、3佳作、4器材）',
  `c_item_id` int(11) NOT NULL DEFAULT '0' COMMENT '文章 ID',
  `c_com_recive` int(11) NOT NULL DEFAULT '0' COMMENT '接收评论',
  `c_content` varchar(1000) NOT NULL DEFAULT '' COMMENT '内容',
  `c_time` datetime NOT NULL COMMENT '时间',
  `c_read` int(6) NOT NULL DEFAULT '0' COMMENT '是否未读（1 已读，0 未读）',
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='评论表';

-- ----------------------------
-- Table structure for pz_equipment
-- ----------------------------
DROP TABLE IF EXISTS `pz_equipment`;
CREATE TABLE `pz_equipment` (
  `e_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文章 ID 主键',
  `e_user` int(11) NOT NULL COMMENT '发布人',
  `e_title` varchar(255) NOT NULL DEFAULT '' COMMENT '文章标题',
  `e_content` varchar(5000) NOT NULL DEFAULT '' COMMENT '文章内容',
  `e_release_time` datetime NOT NULL COMMENT '发布时间',
  `e_url` varchar(255) NOT NULL DEFAULT '' COMMENT '首页图片',
  `e_read` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `e_thumb` int(11) NOT NULL DEFAULT '0' COMMENT '支持数',
  PRIMARY KEY (`e_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='摄影器材表';

-- ----------------------------
-- Table structure for pz_picture
-- ----------------------------
DROP TABLE IF EXISTS `pz_picture`;
CREATE TABLE `pz_picture` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文章 ID 主键',
  `p_user` int(11) NOT NULL COMMENT '发布人',
  `p_title` varchar(255) NOT NULL DEFAULT '' COMMENT '文章标题',
  `p_content` varchar(5000) NOT NULL DEFAULT '' COMMENT '文章内容',
  `p_release_time` datetime NOT NULL COMMENT '发布时间',
  `p_url` varchar(255) NOT NULL DEFAULT '' COMMENT '首页图片',
  `p_read` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `p_thumb` int(11) NOT NULL DEFAULT '0' COMMENT '支持数',
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='摄影佳作表';

-- ----------------------------
-- Table structure for pz_skill
-- ----------------------------
DROP TABLE IF EXISTS `pz_skill`;
CREATE TABLE `pz_skill` (
  `s_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文章 ID 主键',
  `s_user` int(11) NOT NULL COMMENT '发布人',
  `s_title` varchar(255) NOT NULL DEFAULT '' COMMENT '文章标题',
  `s_content` varchar(5000) NOT NULL DEFAULT '' COMMENT '文章内容',
  `s_release_time` datetime NOT NULL COMMENT '发布时间',
  `s_url` varchar(255) NOT NULL DEFAULT '' COMMENT '首页图片',
  `s_read` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `s_thumb` int(11) NOT NULL DEFAULT '0' COMMENT '支持数',
  PRIMARY KEY (`s_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='摄影技巧表';

-- ----------------------------
-- Table structure for pz_topic
-- ----------------------------
DROP TABLE IF EXISTS `pz_topic`;
CREATE TABLE `pz_topic` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文章 ID 主键',
  `t_user` int(11) NOT NULL COMMENT '发布人',
  `t_title` varchar(255) NOT NULL DEFAULT '' COMMENT '文章标题',
  `t_content` varchar(5000) NOT NULL DEFAULT '' COMMENT '文章内容',
  `t_release_time` datetime NOT NULL COMMENT '发布时间',
  `t_url` varchar(255) NOT NULL DEFAULT '' COMMENT '首页图片',
  `t_read` int(11) NOT NULL DEFAULT '0' COMMENT '阅读数',
  `t_thumb` int(11) NOT NULL DEFAULT '0' COMMENT '支持数',
  PRIMARY KEY (`t_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='摄影头条表';

-- ----------------------------
-- Table structure for pz_user
-- ----------------------------
DROP TABLE IF EXISTS `pz_user`;
CREATE TABLE `pz_user` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_username` varchar(255) NOT NULL DEFAULT '' COMMENT '用户名',
  `u_password` varchar(255) NOT NULL DEFAULT '' COMMENT '用户密码',
  `u_credit` int(11) NOT NULL COMMENT '用户积分',
  `u_avatar` varchar(255) NOT NULL DEFAULT '' COMMENT '用户头像',
  `u_autograph` varchar(255) NOT NULL DEFAULT '' COMMENT '个性签名',
  `u_last_login_time` datetime NOT NULL COMMENT '最后登入时间',
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';
