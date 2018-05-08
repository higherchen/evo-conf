-- 配置中心
SET NAMES utf8;

CREATE TABLE `config_app` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(32) NOT NULL COMMENT '应用名，唯一',
  `description` varchar(32) NOT NULL COMMENT '应用备注',
  `state` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态，1-启用，0-禁用，默认1',
  `creator` varchar(16) NOT NULL DEFAULT '' COMMENT '创建人',
  `modifier` varchar(16) NOT NULL DEFAULT '' COMMENT '最后修改人',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `mtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_app_1` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '配置中心应用表';

CREATE TABLE `config_app_env` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `app_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '对应config_app表ID',
  `name` varchar(8) NOT NULL DEFAULT '' COMMENT '环境名',
  `token` varchar(16) NOT NULL DEFAULT '' COMMENT '环境对应token',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `mtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_app_attr_1` (`app_id`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '应用对应环境属性';

CREATE TABLE `config_namespace` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '命名空间ID',
  `name` varchar(16) NOT NULL COMMENT '命名空间名',
  `description` varchar(32) NOT NULL DEFAULT '' COMMENT '描述说明',
  `app_id` varchar(32) NOT NULL COMMENT '所属应用ID',
  `env_id` int(11) NOT NULL COMMENT '所属环境ID，关联config_app_env表',
  `src` varchar(128) NOT NULL DEFAULT '' COMMENT '模板文件',
  `target` varchar(128) NOT NULL DEFAULT '' COMMENT '目标文件',
  `namespace_related` int(11) NOT NULL DEFAULT '0' COMMENT '如果非0则关联到公共namespace',
  `is_public` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否公共，0-否，1-是，默认0',
  `state` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态，1-启用，0-禁用，默认1',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `mtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_namespace_1` (`name`, `app_id`, `env_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '配置中心命名空间表';

CREATE TABLE `config_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '配置ID',
  `namespace_id` int(10) NOT NULL DEFAULT '0' COMMENT '所属命名空间ID',
  `key` varchar(128) NOT NULL DEFAULT 'default' COMMENT '配置项Key',
  `value` longtext NOT NULL COMMENT '配置项值',
  `description` varchar(32) DEFAULT '' COMMENT '描述说明',
  `rank` int(11) DEFAULT '0' COMMENT '数值越大越靠前',
  `hidden` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否隐藏，0-否，1-是',
  `state` tinyint(4) NOT NULL DEFAULT '0' COMMENT '标识是否发布，是否改动',
  `creator` varchar(16) NOT NULL DEFAULT '' COMMENT '创建人',
  `modifier` varchar(16) NOT NULL DEFAULT '' COMMENT '最后修改人',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `mtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_item_1` (`namespace_id`, `key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '配置项表';

CREATE TABLE `config_release` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '发布ID',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT 'release name',
  `namespace_id` int(10) NOT NULL DEFAULT '0' COMMENT '所属命名空间ID',
  `type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '发布类型，1-普通发布，2-回滚',
  `content` longtext NOT NULL COMMENT '配置内容',
  `description` varchar(32) NOT NULL DEFAULT '' COMMENT '发布备注',
  `creator` varchar(16) NOT NULL DEFAULT '' COMMENT '发布人',
  `ctime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '配置发布表';
