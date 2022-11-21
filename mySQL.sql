CREATE TABLE `Users` (
  `userID` INTEGER NOT NULL,
  `Name` varchar(255),
  PRIMARY KEY (`userID`)
);

CREATE TABLE `Games` (
  `gameID` INTEGER NOT NULL,
  `userID` INTEGER,
  `event` varchar(255),
  `data` varchar(255),
  `extraData` varchar(255),
  PRIMARY KEY (`gameID`),
  FOREIGN KEY (`userID`) REFERENCES `Users`(`userID`)
);

CREATE TABLE `Rounds` (
  `roundID` INTEGER NOT NULL,
  `gameID` INTEGER,
  `event` varchar(255),
  `data` varchar(255),
  PRIMARY KEY (`roundID`),
  FOREIGN KEY (`gameID`) REFERENCES `Games`(`gameID`)
);

