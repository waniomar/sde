folders = ['1-EastRiver', '2-DryCreek','3-SagehenCreek','4-AndrewsForest','5-Baltimore',
             '6-BonanzaCreek','7-CaliforniaCurrentEcosystem','8-CentralArizona','9-Coweeta','10-FloridaCoastalEverglades',
             '11-GeorgiaCoastalEcosystems','12-HarvardForest','13-HubbardBrook','14-JornadaBasin','15-Kellogg',
             '16-KonzaPrairie','17-NorthernGulfofAlaska','18-PlumIsland','19-Sevilleta','20-Boulder',
             '21-Catalina','22-Jemez','23-Christina','24-Luquillo','25-Reynolds',
             '26-ShaleHills','27-SanJoaquin','28-Providence','29-Wolverton','30-Calhoun']


watersheds = ['EastRiver','DryCreek','SagehenCreek','AndrewsForest','Baltimore',
            'BonanzaCreek','CaliforniaCurrentEcosystem','CentralArizona','Coweeta','FloridaCoastalEverglades',
            'GeorgiaCoastalEcosystems','HarvardForest','HubbardBrook','JornadaBasin','Kellogg',
            'KonzaPrairie','NorthernGulfofAlaska','PlumIsland','Sevilleta','Boulder',
            'Catalina','Jemez','Christina','Luquillo','Reynolds',
            'ShaleHills','SanJoaquin','Providence','Wolverton','Calhoun']

watershed_names = ['EastRiver','DryCreek','SagehenCreek','AndrewsForest','Baltimore',
            'Bonanza Creek','California Current Ecosystem','Central Arizona','Coweeta','Florida Coastal Everglades',
            'Georgia Coastal Ecosystems','Harvard Forest','Hubbard Brook','Jornada Basin','Kellogg',
            'Konza Prairie','Northern Gulf of Alaska','Plum Island','Sevilleta','Boulder',
            'Catalina','Jemez','Christina','Luquillo','Reynolds',
            'Shale Hills','San Joaquin','Providence','Wolverton','Calhoun']

main_str_dic={'EastRiver':[1,'PHISCO'],
              'DryCreek':[2,'LG'],
              'SagehenCreek':[3,'Sagehen'],
              'AndrewsForest':[4,'GSLOOK'],
              'Baltimore':[5,'GWYNNS'],
              'BonanzaCreek':[6,'C4'],
              'CaliforniaCurrentEcosystem':[7,'FashionValley'],
              'CentralArizona':[8,'SCNFM'],
              'Coweeta':[9,'Prentiss'],
              'FloridaCoastalEverglades':[10,'BarronRiver'],
              'GeorgiaCoastalEcosystems':[11,'Altamaha'],
              'HarvardForest':[12,'BigelowLower'],
              'HubbardBrook':[13,'WS7'],
              'JornadaBasin':[14,'SaltCreek'],
              'Kellogg':[15,'KBS096'],
              'KonzaPrairie':[16,'KingsRiver'],
              'NorthernGulfofAlaska':[17,'Dwnstr'],
              'PlumIsland':[18,'Ipswich'],
              'Sevilleta':[19,'PECOS'],
              'Boulder':[20,'Longmont'],
              'Catalina':[21,'SabinoCreek'],
              'Jemez':[22,'JemezRiver'],
              'Christina':[23,'WhiteClayCreek'],
              'Luquillo':[24,'RioGrande'],
              'Reynolds':[25,'036'],
              'ShaleHills':[26,'ShaleHill'],
              'SanJoaquin':[27,'Fremont'],
              'Providence':[28,'P301'],
              'Wolverton':[29,'Hammond'],
              'Calhoun':[30,'BroadRiverCarlisle']}

## The ppt stn is chosen given the position of the main discharge station and considering the record length
main_ppt_dic={'DryCreek':[2,'TL'],
              'SagehenCreek':[3,'539lvl1B'],
              'AndrewsForest':[4,'PRIMET'],
              'BonanzaCreek':[6,'LTER1'],
              'CaliforniaCurrentEcosystem':[7,'Lindberch'],
              'HubbardBrook':[13,'WS7'],
              'Kellogg':[15,'KBS002'],
              'KonzaPrairie':[16,'HQ01'],
              'Sevilleta':[19,'Station40'],
              'Reynolds':[25,'049']}

# in km2
area_dic={'EastRiver': 300,'DryCreek': 27,'SagehenCreek': 27,'AndrewsForest': 62,'Baltimore': 171,
         'BonanzaCreek': 10,'CaliforniaCurrentEcosystem': 1111, 'CentralArizona': 425,'Coweeta': 363 ,
          'FloridaCoastalEverglades':342, 
         'GeorgiaCoastalEcosystems': 35224, 'HarvardForest': 0.65,'HubbardBrook': 0.77,'JornadaBasin': 1976,'Kellogg': 101,
         'KonzaPrairie':12 ,'NorthernGulfofAlaska':634 ,'PlumIsland':115 ,'Sevilleta':2719 ,'Boulder':62.7 ,
         'Catalina': 1217, 'Jemez': 92, 'Christina': 29,'Luquillo': 19,'Reynolds': 239,
         'ShaleHills':0.08 ,'SanJoaquin': 19723,'Providence': 4.6,'Wolverton': 427,'Calhoun': 7226}

lat_dic={'EastRiver':39.00,'DryCreek':43.69,'SagehenCreek':39.43,'AndrewsForest':44.24,'Baltimore':39.27,
         'BonanzaCreek':65.17 ,'CaliforniaCurrentEcosystem':32.77, 'CentralArizona':33.43,'Coweeta': 35.00,'FloridaCoastalEverglades':25.47,
         'GeorgiaCoastalEcosystems':31.42, 'HarvardForest':42.53,'HubbardBrook':43.94,'JornadaBasin':32.62,'Kellogg':42.40,
         'KonzaPrairie':39.11,'NorthernGulfofAlaska':63.88,'PlumIsland':42.76,'Sevilleta':34.35,'Boulder':40.01,
         'Catalina':32.43, 'Jemez':35.88, 'Christina':39.86,'Luquillo':18.32,'Reynolds':43.23,
         'ShaleHills':40.66,'SanJoaquin':37.11,'Providence':37.06,'Wolverton':36.59,'Calhoun':34.61}

lon_dic={'EastRiver':-107.00, 'DryCreek':-116.18, 'SagehenCreek':-120.24, 'AndrewsForest':-122.18, 'Baltimore':-76.65,
         'BonanzaCreek':-147.51, 'CaliforniaCurrentEcosystem':-117.17, 'CentralArizona':-111.93, 'Coweeta':-83.50,'FloridaCoastalEverglades':-80.85,
         'GeorgiaCoastalEcosystems':-81.30, 'HarvardForest':-72.19, 'HubbardBrook':-71.75, 'JornadaBasin':-106.74, 'Kellogg':-85.40,
         'KonzaPrairie':-96.61, 'NorthernGulfofAlaska':-145.71, 'PlumIsland':-70.89, 'Sevilleta':-106.88, 'Boulder':-105.34,
         'Catalina':-110.77, 'Jemez':-106.53, 'Christina':-75.79,'Luquillo':-65.73, 'Reynolds':-116.65,
         'ShaleHills':-77.91, 'SanJoaquin':-119.73, 'Providence':-119.20, 'Wolverton':-118.73, 'Calhoun':-81.72}

variables = ['Discharge','Precipitation','AirTemperature','SolarRadiation',
                                   'RelativeHumidity','SWE','SnowDepth','SoilTemperature','SoilMoisture']