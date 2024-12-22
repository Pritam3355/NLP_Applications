-- use ChatDB;

-- create table if not exists ChatDB.Active_Users(
-- 		u_id varchar(16) primary key,
--         is_active int);
-- create table if not exists ChatDB.Session_Data(
-- 		u_id varchar(16),
--         session_id varchar(64),
--         time_stamp datetime,
--         stream_id int);
-- create table if not exists ChatDB.Chat_Data(
--         session_id varchar(64),
--         user_input text,
--         bot_response text);

-- insert into ChatDB.Active_Users(u_id,is_active) values 
-- 	('user123', 0),
--     ('user_A', 0),
--     ('user456', 0),
--     ('user_B', 0),
--     ('user789', 0);
--     
--     
select * from ChatDB.Active_Users;
select * from ChatDB.Session_Data;
select * from ChatDB.Chat_Data;

-- delete from ChatDB.Active_Users;
-- delete from ChatDB.Session_Data;
-- delete from ChatDB.Chat_Data;

-- drop table ChatDB.Active_Users;
-- drop table ChatDB.Session_Data;
-- drop table ChatDB.Chat_Data;