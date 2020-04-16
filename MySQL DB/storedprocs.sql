


-- This file is a list of all the stored procedures used in the database


-- ADD A USER =====
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `add_user`(IN user_email VARCHAR(200), IN pwd VARCHAR(100))
BEGIN
	INSERT INTO `dublinbikes`.`userinfo` (`email`, `password`, `stations`, `emailvalidated`)
	VALUES (user_email, pwd, "[]", 0);
END ;;
DELIMITER ;

-- CHECK IF AN EMAIL ALREADY EXISTS IN THE DB ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `check_if_email_exists`(IN user_email VARCHAR(200))
BEGIN
	SELECT EXISTS(SELECT `email` FROM userinfo WHERE `email`= user_email);
END ;;
DELIMITER ;

-- DELETE A USER BY EMAIL ADDRESS ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `delete_user`(IN user_email VARCHAR(200))
BEGIN
	DELETE FROM `dublinbikes`.`userinfo` WHERE (`email` = user_email);
END ;;
DELIMITER ;

-- FIND THE AVERAGE AMOUNT OF BIKES AVAILABLE BY DAY ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `get_avg_daily_availbikes_by_id`(IN stationID INT)
BEGIN
	SELECT CAST(AVG(availbikes) as SIGNED),  CAST(AVG(availstands) as SIGNED)
	FROM dynamicinfo
    WHERE ID = stationID
    AND dynamicinfo.time < '2020-03-12'
	group by WEEKDAY(dynamicinfo.time);
END ;;
DELIMITER ;

-- FIND THE AVERAGE AMOUNT OF BIKES AVAILABLE BY HOUR ON A PARTICULAR DAY ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `get_avg_hourly_availbike_by_day_and_id`(IN dayofweek INT, IN stationID INT)
BEGIN
	SELECT CAST(AVG(availbikes) as SIGNED),  CAST(AVG(availstands) as SIGNED)
	FROM dynamicinfo
	WHERE WEEKDAY(dynamicinfo.time) = dayofweek
	AND  dynamicinfo.ID = stationID
    AND dynamicinfo.time < '2020-03-12'
	GROUP BY HOUR(dynamicinfo.time);
END ;;
DELIMITER ;

-- GET THE MOST RECENT STAND INFO ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `get_current_stand_info`()
BEGIN
select dyi.id, dyi.availstands, dyi.availbikes, dyi.status, dyi.time, dyi.banking, dyi.bonus, dyi.numbikestands
from (
   select id, max(time) as maxtime
   from dynamicinfo group by id
) as x inner join dynamicinfo as dyi on dyi.id = x.id and dyi.time = x.maxtime;
END ;;
DELIMITER ;

-- GET THE MOST RECENT STAND INFO FOR A PARTICULAR STAND ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `get_stand_info_by_id`(IN standid INT)
BEGIN
select dyi.id, dyi.availstands, dyi.availbikes, dyi.status, dyi.time, dyi.banking, dyi.bonus, dyi.numbikestands
from (
   select id, max(time) as maxtime
   from dynamicinfo
   where id = standid
   group by standid
) as x inner join dynamicinfo as dyi on dyi.id = x.id and dyi.time = x.maxtime;

END ;;
DELIMITER ;

-- RETRIEVE A USER'S DETAILS ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `get_user_details_by_email`(IN user_email VARCHAR(200))
BEGIN
	SELECT *
    FROM `userinfo`
    WHERE `email` = user_email;
END ;;
DELIMITER ;

-- UPDATE A USER'S EMAIL ======
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `update_email`(IN old_email VARCHAR(200), new_email VARCHAR(200))
BEGIN
	UPDATE `dublinbikes`.`userinfo`
	SET `email` = new_email
	WHERE (`email` = old_email);
END ;;
DELIMITER ;

-- UPDATE A USER'S EMAILVALIDATED STATUS ====
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `update_emailvalidated`(IN user_email VARCHAR(200), valid INT)
BEGIN
	UPDATE `dublinbikes`.`userinfo`
	SET `emailvalidated` = valid
	WHERE (`email` = user_email);
END ;;
DELIMITER ;

-- UPDATE A USER'S PASSWORD ====
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `update_password`(IN user_email VARCHAR(200), new_password VARCHAR(100))
BEGIN
	UPDATE `dublinbikes`.`userinfo`
	SET `password` = new_password
	WHERE (`email` = user_email);
END ;;
DELIMITER ;

-- UPDATE A USER'S FAVOURITED STATIONS ====
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `update_stations`(IN user_email VARCHAR(200), new_stations JSON)
BEGIN
	UPDATE `dublinbikes`.`userinfo`
	SET `stations` = new_stations
	WHERE (`email` = user_email);
END ;;
DELIMITER ;
