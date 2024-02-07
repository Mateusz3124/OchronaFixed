CREATE DATABASE IF NOT EXISTS bank;

USE bank;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account VARCHAR(255),
    amount VARCHAR(255),
    username VARCHAR(255),
    card VARCHAR(255),
    email VARCHAR(255),
    loginCount INT,
    currentSequence INT,
    idNumber VARCHAR(255)
);

CREATE TABLE  transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    amount VARCHAR(255),
    fromAccount VARCHAR(255),
    account VARCHAR(255),
    name VARCHAR(255),
    surname VARCHAR(255),
    address VARCHAR(255),
    idUsername INT,
    FOREIGN KEY (idUsername) REFERENCES users(id)
);


CREATE TABLE passwords (
    password VARCHAR(255),
    sequence VARCHAR(255),
	idUsername INT,
    FOREIGN KEY (idUsername) REFERENCES users(id)
);

CREATE TABLE changePassword (
    idVerification VARCHAR(255),
    secretIdVerification VARCHAR(255),
    timestampColumn TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE EVENT deleteExpiredRows
ON SCHEDULE EVERY 1 MINUTE
DO
  DELETE FROM changePassword WHERE timestampColumn < NOW() - INTERVAL 10 MINUTE;
//
DELIMITER ;

SET GLOBAL event_scheduler = ON;

INSERT INTO users (email, username, card, idNumber, account,loginCount, amount, currentSequence) VALUES ('testOchronaDanychPW@gmail.com','12345678', 'Jypa+kGBGNEM+IQGcwHTgA==;qyOTKRWbBeAMWVNz9IVw+w==;41CQoX9phbhl9sF9hQDGiA==', 'sdSCi+JKAHuq;QkTzpUA7ZfTni7jphZaKHQ==;3Xv2fjBYbtE7NfQ6hPLULA==','a23v567891011','0', '25121.21,e1f7cc2ce4fc92cd6b354917f0b26d177562554be783547d4e20148479bb','2');
INSERT INTO users (email, username, card, idNumber, account,loginCount, amount, currentSequence) VALUES ('testOchronaDanychPW@gmail.com','87654321', 'RacDUUT0AlRnGcZUKE8XBA==;ut7OCEmtdul8gZh57XpstA==;HCw3KJH2qvdjf1gvP4PVrw==','F/Mb5E3OoJr5;bE2zfn8bkZ4aebg+vX9hwQ==;DOyo4iSbK9hRt97s01zsLg==','1234567891011','0','22134.11,b26f6bd9dfbdae56e23cf74c314d629d571b868de200e5e780cedbe7f37f','2');

INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$vBcCAOB8T4kxxtibU4qRUg$oHjXNmpuaFW4W/lLA5eTL8zoZTD4YaEQ1VmrCojwJes', '2,5,14,17,19,22,24,29','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$7N2717rXuleqldIa49y7lw$m3zJWgqwtZW8Y8Sum6G8tG3f8Wen2z3wvrLC4V0XHxA', '6,10,13,16,20,22,26,28','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$U2oNIeR8T+ndO2cMAeA8Rw$dlgqsSPEB/vLPJW6B1nfNvJ7O2/iczdDHznROL5S9As', '1,5,7,14,20,25,28,30','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$W8tZK2UM4by3FsJ4T+md0w$FtIORYBp/LPw7/bIZZnvV0cq3nY6gvOcbpvc3JroiEk', '4,7,17,19,22,24,26,30','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$4vy/t5YyBmCMMcYYQ6g1Jg$SoJrZwpSBaXr4qsxqZ1VVDBtpuAWL7AsFccsYYXeheA', '2,4,7,10,13,17,19,29','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$dC7lnJOS0trb+78XQgghJA$7296X/zNyCyiit3kAGbNmNUbXqb6uRswGtvpvRm9VD8', '5,8,13,20,24,26,28,30','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$ew+hdG6t9d77H+N8L+WcMw$saaHHEDq2R5VhB+Jr84A1ntvLwrdYX3qvfwjfJ2823A', '2,7,10,12,14,18,27,29','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$GYPQ2vsfQygFwLjXWkupdQ$2JtHbMAWLW9C496zo00wDrRtiyxtluwbkKiPf9aggPs', '2,5,9,13,16,25,28,30','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$0pqTsrY2RohRqhWi1BrjfA$gGhm+4RSCb0x+ThhaqM8jGfjBUHiyp5msg6xS0NbvYM', '2,4,8,11,13,16,21,27','1');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$a02JcU5JaW0tReh9jxECwA$rTlcZxQy4AkuTyc6uj9cZyHxiBXl3bFzew/SjxbP6S4', '2,9,12,14,17,19,24,27','1');

INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$UkrJGSNkLCXkXEupda6VEg$ezjw1Far8shI4V4NajDC7WAGW3Txwq0Dfi50iuau6wM', '2,5,8,10,12,14,25,29','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$Wus951yL8d77PwcgpLR2zg$1CYfh+fIbkir0LSxRtxdUbdYQlay8Sxegf4sJlPEKFI', '1,3,5,12,16,20,26,28','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$HOPcm5MSIqT0fm/NeS8lhA$4cXkSvNFMM46w++XigtUDz8si7b6d+CORwM1Vl2gL5g', '4,6,9,12,16,22,26,29','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$zJlTivFeC2GMUWotpTRG6A$e+HZKz1jLRjhmWY4AeHCedgOKdqJ294quuP+5eJJ7Ak', '1,4,7,12,14,21,23,29','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$rxXi3Lv3HmNsLYUwhrAWwg$CLyeKvrqUrHV1mNirsfVFZ6GOwEi2GtKhu5eQR0ZUoE', '7,9,13,15,19,22,24,26','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$ktKas/Yeg/B+jxEiBOAcow$KDE66Y4a1CwRVtEgo1F8pyuGmVTxb2CB0XP6iu9Me7I', '4,9,13,15,18,23,26,29','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$U8p5713LuXduTcn5f2/tHQ$9kOzjpkF4RxOE1ufpGBtr53KWEtYogZUDuMddVzgdRA', '1,3,5,12,14,18,20,28','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$aE1p7Z3z3jtHqNVaS+mdsw$2qqOKOXDKiJ9HnEsmfATdsMCGvA4pjlWuYmvOR2h2bk', '3,6,8,10,13,24,26,30','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$3VsrJSQEwBjj3NubU2qNUQ$mXJu5J5+/pS4St6xrUu27ZOCHXqma3ZxLeFgB6XKARU', '3,5,10,14,17,22,27,30','2');
INSERT INTO passwords (password, sequence, idUsername) VALUES ('$argon2id$v=19$m=65536,t=3,p=4$C6HUmlNqLcV4b83Zm9O6Vw$5GvNg0cv133kkGdbeiAbS7tdETgWTtJQ3eDJlp0qlzU', '3,7,12,14,16,20,24,30','2');



