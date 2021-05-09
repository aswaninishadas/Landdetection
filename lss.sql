-- -----------------------------------------------------
-- Table "user"
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS "user" (
	"userId" BIGSERIAL NOT NULL,
	"firstName" VARCHAR(45) NOT NULL,
	"lastName" VARCHAR(45) NULL,
	"userName" VARCHAR(255) NOT NULL UNIQUE,
	"phoneNumber" BIGINT NOT NULL UNIQUE,
	"email" VARCHAR(255) NOT NULL UNIQUE,
	"password" VARCHAR(255) NOT NULL,
	PRIMARY KEY ("userId"));
	

-- -----------------------------------------------------
-- Table "rationCard"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS "rationCard" (
	"cardId" BIGSERIAL NOT NULL,
	"cardNumber" BIGINT NOT NULL,
	"ownerName" VARCHAR(45) NOT NULL,
	"houseName" VARCHAR(45) NOT NULL,
	"houseNumber" BIGINT NOT NULL,
	"place" VARCHAR(45) NOT NULL,
	"thaluk" VARCHAR(45) NOT NULL,
	PRIMARY KEY ("cardId"));
	


-- -----------------------------------------------------
-- Table "memberDetails"
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS "memberDetails" (
	"memberId" BIGSERIAL NOT NULL,
	"firstName" VARCHAR(45) NOT NULL,
	"lastName" VARCHAR(45) NULL,
	"age" INT NOT NULL,
	"cardNumber" BIGINT NOT NULL,
	"maritalStatus" BOOLEAN DEFAULT FALSE,
	"spouse" BIGINT NULL,
	"landOwnedInAcres" INT NULL,
	"landOwnedInCent" DECIMAL NULL,
	PRIMARY KEY ("memberId"));
	
	
	
"cardId" BIGINT NOT NULL REFERENCES "rationCard"("cardId") ON DELETE CASCADE,
