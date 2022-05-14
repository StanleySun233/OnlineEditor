create database oe;

create table file_info
(
    file_id     varchar(36)               not null comment '文件md5'
        primary key,
    file_name   varchar(128)              not null comment '文件名称',
    file_type   varchar(16) default 'txt' null,
    file_auth   varchar(1)  default '0'   null comment '文件权限',
    create_date date                      null comment '创建时间',
    user_name   varchar(72)               null comment '用户名',
    last_date   date                      null comment '更新时间',
    constraint file_info_file_id_uindex
        unique (file_id)
)
    comment '文件表' collate = utf8mb4_general_ci;

create table file_info_del
(
    file_id     varchar(36)               not null comment '文件md5'
        primary key,
    file_name   varchar(128)              not null comment '文件名称',
    file_type   varchar(16) default 'txt' null,
    file_auth   varchar(1)  default '0'   null comment '文件权限',
    create_date date                      null comment '创建时间',
    user_name   varchar(72)               null comment '用户名',
    last_date   date                      null comment '更新时间',
    del_time    date                      null comment '删除时间',
    constraint file_info_del_file_id_uindex
        unique (file_id),
    constraint file_info_del_file_info_file_id_fk
        foreign key (file_id) references file_info (file_id)
)
    comment '文件表删除记录' collate = utf8mb4_general_ci;

create table file_share
(
    file_id    varchar(36) not null comment '物理主键',
    file_from  varchar(36) null comment '共享者',
    file_to    varchar(36) null comment '接受者',
    file_new   varchar(36) not null comment '新文件id'
        primary key,
    share_date date        null comment '共享时间',
    constraint file_share_file_new_uindex
        unique (file_new)
);

create table user_info
(
    user_id       varchar(128)           not null comment '物理主键'
        primary key,
    user_account  varchar(128)           not null comment '用户账户',
    user_password varchar(512)           not null comment '用户密码-sha256加密',
    user_auth     varchar(1) default '0' null comment '用户权限',
    constraint user_info_user_id_uindex
        unique (user_id)
)
    comment '用户表' collate = utf8mb4_general_ci;

