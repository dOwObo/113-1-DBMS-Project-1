-- 建立 Schema: PatentOffice
CREATE SCHEMA PatentOffice;

-- DDL for Table Administrator
CREATE TABLE PatentOffice.Administrator (
	account VARCHAR(128) NOT NULL PRIMARY KEY, -- 帳號（主鍵）
    password VARCHAR(128) NOT NULL             -- 密碼
)

-- DDL for Table Office
CREATE TABLE PatentOffice.Office (
    officeName VARCHAR(10) PRIMARY KEY,  -- 分部名稱（主鍵）
    contactPerson VARCHAR(20),           -- 聯絡人
    phone VARCHAR(20),                   -- 聯絡電話
    email VARCHAR(50),                   -- 電子郵件
    address VARCHAR(100)                 -- 地址
);

-- DDL for Table PatentEngineer
CREATE TABLE PatentOffice.PatentEngineer (
    eId SERIAL PRIMARY KEY,              -- 工程師編號（主鍵）
    eName VARCHAR(20) NOT NULL,          -- 姓名
    phone VARCHAR(20),                   -- 聯絡電話
    officeName VARCHAR(10) NOT NULL,     -- 所屬分部名稱（外鍵 → 指向 Office 表）
	FOREIGN KEY (officeName) REFERENCES PatentOffice.Office(officeName)
);

-- DDL for Table Expertise
CREATE TABLE PatentOffice.Expertise (
    eId INT NOT NULL,                    -- 工程師編號（複合主鍵，外鍵 → 指向 PatentEngineer 表）
	expertise VARCHAR(10) NOT NULL,      -- 專業領域（複合主鍵）
	PRIMARY KEY (eId, expertise),
	FOREIGN KEY (eId) REFERENCES PatentOffice.PatentEngineer(eId)
);

-- DDL for Table CustomerService
CREATE TABLE PatentOffice.CustomerService (
    csId SERIAL PRIMARY KEY,             -- 客服人員編號（主鍵）
    csName VARCHAR(20) NOT NULL,         -- 姓名
    phone VARCHAR(20),                   -- 聯絡電話
    email VARCHAR(50),                   -- 電子郵件
    officeName VARCHAR(100) NOT NULL,    -- 所屬分部名稱（外鍵 → 指向 Office 表）
    FOREIGN KEY (officeName) REFERENCES PatentOffice.Office(officeName)
);

-- DDL for Table Client
CREATE TABLE PatentOffice.Client (
    cId SERIAL PRIMARY KEY,              -- 客戶編號（主鍵）
    cName VARCHAR(20) NOT NULL,          -- 客戶名稱
    phone VARCHAR(20) NOT NULL,          -- 聯絡電話
    email VARCHAR(50) NOT NULL,          -- 電子郵件
    address VARCHAR(100) NOT NULL,       -- 地址
    csId INT NOT NULL,                   -- 客服人員編號（外鍵 → 指向 CustomerService 表）
    FOREIGN KEY (csId) REFERENCES PatentOffice.CustomerService(csId)
);

-- DDL for Table PatentCase
CREATE TABLE PatentOffice.PatentCase (
    pId SERIAL PRIMARY KEY,              -- 案件編號（主鍵）
    commissionDate DATE NOT NULL,        -- 案件委託日
    pName VARCHAR(255) NOT NULL,         -- 專利名稱
    pType VARCHAR(50) NOT NULL,          -- 專利類型
    patentee VARCHAR(20) NOT NULL,       -- 專利權人
    inventor VARCHAR(20) NOT NULL,       -- 發明人
    aId VARCHAR(50) UNIQUE,              -- 申請號（唯一）
    applicationDate DATE,                -- 申請日
    certificateId VARCHAR(50) UNIQUE,    -- 證書號（唯一）
    startDate DATE,                      -- 專利權開始
    endDate DATE,                        -- 專利權結束
    cId INT NOT NULL,                    -- 客戶編號（外鍵 → 指向 Client 表）
    eId INT,                    -- 專利工程師編號（外鍵 → 指向 PatentEngineer 表）
    FOREIGN KEY (cId) REFERENCES PatentOffice.Client(cId),
    FOREIGN KEY (eId) REFERENCES PatentOffice.PatentEngineer(eId)
);

-- Insert data into Administrator table
INSERT INTO PatentOffice.Administrator (account, password)
VALUES ('admin', 'syhwang')

-- Insert data into Office table
INSERT INTO PatentOffice.Office (officeName, contactPerson, phone, email, address) 
VALUES ('分部A', '王小明', '0912345678', 'ming@office.com', '台北市信義區'),
       ('分部B', '李小華', '0922333444', 'hua@office.com', '新北市板橋區'),
       ('分部C', '張大明', '0933444555', 'da@office.com', '台中市西屯區');

-- Insert data into PatentEngineer table
INSERT INTO PatentOffice.PatentEngineer (eName, phone, officeName) 
VALUES ('林文彥', '0912340001', '分部A'),
       ('鄭華明', '0912340002', '分部A'),
       ('陳立忠', '0912340003', '分部A'),
       ('張雅雯', '0912340004', '分部B'),
       ('周傑銘', '0912340005', '分部B'),
       ('吳濤晟', '0912340006', '分部B'),
       ('何曼', '0912340007', '分部C'),
       ('陳麗', '0912340008', '分部C'),
       ('李新瑋', '0912340009', '分部C'),
       ('王昇財', '0912340010', '分部A');

-- Insert data into Expertise table
INSERT INTO PatentOffice.Expertise (eId, expertise) 
VALUES (1, '半導體'),
       (1, '運算科技'),
       (2, '電子機械能源裝置'),
       (3, '視聽科技'),
       (3, '測量'),
       (4, '藥物'),
       (4, '數位通訊'),
       (4, '醫療技術'),
       (5, '半導體'),
       (6, '運算科技'),
       (6, '電子機械能源裝置'),
       (6, '藥物'),
       (7, '視聽科技'),
       (7, '數位通訊'),
       (8, '醫療技術'),
       (8, '測量'),
       (8, '電子機械能源裝置'),
       (8, '運算科技'),
       (9, '醫療技術'),
       (10, '半導體'),
       (10, '藥物');

-- Insert data into CustomerService table
INSERT INTO PatentOffice.CustomerService (csName, phone, email, officeName) 
VALUES ('李志明', '0912341001', 'cs1@office.com', '分部A'),
       ('王佳慧', '0912341002', 'cs2@office.com', '分部A'),
       ('陳俊傑', '0912341003', 'cs3@office.com', '分部B'),
       ('林夢潔', '0912341004', 'cs4@office.com', '分部B'),
       ('黃軒', '0912341005', 'cs5@office.com', '分部C'),
       ('張家豪', '0912341006', 'cs6@office.com', '分部C'),
       ('李若彥', '0912341007', 'cs7@office.com', '分部A'),
       ('吳淑慧', '0912341008', 'cs8@office.com', '分部A'),
       ('簡意', '0912341009', 'cs9@office.com', '分部B'),
       ('林佳慧', '0912341010', 'cs10@office.com', '分部B'),
       ('李家宇', '0912341011', 'cs11@office.com', '分部C'),
       ('黃曉青', '0912341012', 'cs12@office.com', '分部C'),
       ('王浩然', '0912341013', 'cs13@office.com', '分部A'),
       ('鄭美麗', '0912341014', 'cs14@office.com', '分部A'),
       ('林俊賢', '0912341015', 'cs15@office.com', '分部B');

-- Insert data into Client table
INSERT INTO PatentOffice.Client (cName, phone, email, address, csId) 
VALUES ('客戶1', '0912345678', 'client1@example.com', '台北市大安區', 1),
       ('客戶2', '0922333444', 'client2@example.com', '新北市三峽區', 2),
       ('客戶3', '0933444555', 'client3@example.com', '台中市北區', 3),
       ('客戶4', '0944555666', 'client4@example.com', '台南市東區', 4),
       ('客戶5', '0955666777', 'client5@example.com', '高雄市前鎮區', 5),
       ('客戶6', '0966777888', 'client6@example.com', '新竹市東區', 6),
       ('客戶7', '0977888999', 'client7@example.com', '嘉義市西區', 7),
       ('客戶8', '0910123456', 'client8@example.com', '宜蘭市羅東鎮', 8),
       ('客戶9', '0921456789', 'client9@example.com', '屏東市', 9),
       ('客戶10', '0932556789', 'client10@example.com', '台中市南區', 10),
       ('客戶11', '0943457890', 'client11@example.com', '台北市中正區', 11),
       ('客戶12', '0954567890', 'client12@example.com', '新北市板橋區', 12),
       ('客戶13', '0965678901', 'client13@example.com', '台中市南區', 13),
       ('客戶14', '0976789012', 'client14@example.com', '台南市安南區', 14),
       ('客戶15', '0912345679', 'client15@example.com', '高雄市左營區', 15),
       ('客戶16', '0922333445', 'client16@example.com', '新竹市香山區', 1),
       ('客戶17', '0933444556', 'client17@example.com', '台中市北屯區', 2),
       ('客戶18', '0944555667', 'client18@example.com', '台南市東區', 3),
       ('客戶19', '0955666778', 'client19@example.com', '高雄市苓雅區', 4),
       ('客戶20', '0966777889', 'client20@example.com', '新竹市北區', 5),
       ('客戶21', '0977888990', 'client21@example.com', '嘉義市東區', 6),
       ('客戶22', '0910123457', 'client22@example.com', '宜蘭市冬山鎮', 7),
       ('客戶23', '0921456790', 'client23@example.com', '屏東市', 8),
       ('客戶24', '0932556790', 'client24@example.com', '台中市西區', 9),
       ('客戶25', '0943457900', 'client25@example.com', '台北市中山區', 10),
       ('客戶26', '0954567900', 'client26@example.com', '新北市新店區', 11),
       ('客戶27', '0965678902', 'client27@example.com', '台中市北區', 12),
       ('客戶28', '0976789013', 'client28@example.com', '台南市新營區', 13),
       ('客戶29', '0912345680', 'client29@example.com', '高雄市三民區', 14),
       ('客戶30', '0922333446', 'client30@example.com', '新竹市竹北市', 15);

-- Insert data into PatentCase table
INSERT INTO PatentOffice.PatentCase (commissionDate, pName, pType, patentee, inventor, aId, applicationDate, certificateId, startDate, endDate, cId, eId)
VALUES ('2021-03-12', '專利案1', '新型', '丁玲玲', '羅建中', 'A123517', '2021-03-13', 'C123517', '2024-01-17', '2034-01-17', 7, 8),
       ('2021-05-20', '專利案2', '新型', '梁文君', '廖偉安', 'A123514', '2021-05-21', 'C123514', '2024-01-14', '2034-01-14', 4, 5),
       ('2021-10-10', '專利案3', '新型', '吳慶祥', '李佩真', 'A123505', '2021-10-11', 'C123505', '2024-01-05', '2034-01-05', 5, 5),
       ('2021-12-05', '專利案4', '設計', '許文靜', '顧成杰', 'A123509', '2021-12-06', 'C123509', '2024-01-09', '2034-01-09', 9, 9),
       ('2022-01-23', '專利案5', '設計', '鍾心怡', '范安瑞', 'A123524', '2022-01-24', 'C123524', '2024-01-24', '2034-01-24', 4, 5),
       ('2022-02-14', '專利案6', '設計', '楊素娟', '曹宗翰', 'A123515', '2022-02-15', 'C123515', '2024-01-15', '2034-01-15', 5, 6),
       ('2022-05-16', '專利案7', '設計', '洪志勇', '陳信豪', 'A123521', '2022-05-17', 'C123521', '2024-01-21', '2034-01-21', 1, 2),
       ('2022-06-06', '專利案8', '設計', '簡家豪', '傅建偉', 'A123518', '2022-06-07', 'C123518', '2024-01-18', '2034-01-18', 8, 9),
       ('2022-07-11', '專利案9', '設計', '黎宇哲', '丁雅君', 'A123512', '2022-07-12', 'C123512', '2024-01-12', '2034-01-12', 12, 3),
       ('2022-11-02', '專利案10', '新型', '林婉婷', '黃偉哲', 'A123502', '2022-11-03', 'C123502', '2024-01-02', '2034-01-02', 2, 2),
       ('2023-01-01', '專利案11', '設計', '楊世豪', '曾雅玲', 'A123506', '2023-01-02', 'C123506', '2024-01-06', '2034-01-06', 6, 6),
       ('2023-03-15', '專利案12', '發明', '劉志宏', '徐正傑', 'A123501', '2023-03-16', 'C123501', '2024-01-01', '2034-01-01', 11, 1),
       ('2023-04-22', '專利案13', '發明', '高玉芬', '賴宗益', 'A123510', '2023-04-23', 'C123510', '2024-01-10', '2034-01-10', 10, 10),
       ('2023-05-17', '專利案14', '發明', '周春麗', '韓少華', 'A123504', '2023-05-18', 'C123504', '2024-01-04', '2034-01-04', 14, 4),
       ('2023-06-20', '專利案15', '新型', '鄭惠雯', '黃俊偉', 'A123508', '2023-06-21', 'C123508', '2024-01-08', '2034-01-08', 8, 8),
       ('2023-07-17', '專利案16', '發明', '周世杰', '王志宏', 'A123516', '2023-07-18', 'C123516', '2024-01-16', '2034-01-16', 6, 7),
       ('2023-08-08', '專利案17', '發明', '賴志豪', '陳庭榆', 'A123513', '2023-08-09', NULL, NULL, NULL, 3, 4),
       ('2023-09-01', '專利案18', '發明', '康秀芬', '林健豪', 'A123519', '2023-09-02', 'C123519', '2024-01-19', '2034-01-19', 19, 10),
       ('2024-01-15', '專利案19', '新型', '徐天佑', '錢雅慧', 'A123511', '2024-01-16', 'C123511', '2024-01-11', '2034-01-11', 1, 2),
       ('2024-02-02', '專利案20', '新型', '黎世俊', '魏美玲', 'A123523', '2024-02-03', NULL, NULL, NULL, 23, 4),
       ('2024-02-28', '專利案21', '設計', '張冠中', '趙明瑞', 'A123503', '2024-02-29', NULL, NULL, NULL, 13, 3),
       ('2024-04-04', '專利案22', '新型', '徐思瑋', '鄭明凱', 'A123520', '2024-04-05', NULL, NULL, NULL, 10, 1),
       ('2024-09-09', '專利案23', '發明', '簡志成', '蔡依柔', NULL, NULL, NULL, NULL, NULL, 27, 7),
       ('2024-10-09', '專利案24', '發明', '程淑芬', '杜偉宏', NULL, NULL, NULL, NULL, NULL, 12, 3),
       ('2024-11-11', '專利案25', '發明', '馬文傑', '許偉淵', NULL, NULL, NULL, NULL, NULL, 25, 6);