# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 16:44:33 2024

@author: julie
"""

# WOVODAT WEBSERVICE DATA DOWNLOAD EXAMPLE CODE
 
# The goal of this piece of code is to give an example how to easily download 
# any required type of data from WOVOdat automatically. 
# The code ensures that all the data available in WOVOdat for the selected 
# data type (i.e., for all volcanoes with data available) at any chosen time 
# period are stored in a directory of your choice, alongside the metadata 
# availalbe (~if no directory chosen, it will be stored in 'Downloads'). 

# Please choose a directory where you want the data and outputs to be stored.
# Indicate the path between the '' (default otherwise: Downloads folder)
base_directory = r''
# e.g: C:\Users\...\Test_Wovodat_code

###############################################################################

import os
import requests
import zipfile
import pandas as pd
import sys
 
# Gather all the information for the webservice data download
# Define the requested data type  
print("Dear user, which data type do you want to download?")
print("(Category 1: Deformation Data) \n1.1 Angle \n1.2 EDM \n1.3 GPS \n1.4 GPS Vector \n1.5 Leveling \n1.5 Insar \n1.6 Strain \n1.7 Electronic Tilt \n1.8 ** Tilt Vector \n \n(Category 2: Fields Data) \n2.1 Magnetic fields \n2.2 Gravity \n2.3 ** Electric Fields \n2.4 ** Magnetic Vector \n \n(Category 3: Gas Data) \n3.1 Directly sampled gas \n3.2 Soil Efflux \n3.3 Plume from Ground based station \n3.4 Plume from satellite/airplane \n \n(Category 4: Hydrologic Sample Data) \n4.1 Hydrologic \n \n(Category 5: Meteo Data) \n5.1 Meteo \n \n(Category 6: Seismic Data) \n6.1 Seismic Event From Network \n6.2 Seismic Event From Single Station \n6.3 Seismic Tremor \n6.4 Seismic Intensity \n6.5 RSAM \n \n(Cateogry 7: Thermal Data) \n7.1 Thermal from ground based station \n7.2 Thermal from satellite/airplane \n \nWith * asterisk means no data in WOVOdat as of now (Feb 2023) \n")

data_type_user = input('Please indicate your requested data type here (e.g., write: 6.3 ~ for downloading Seismic Tremor): ')

data_dict = {
    1.1: "Angle",
    1.2: "EDM",
    1.3: "GPS",
    1.4: "GPS Vector",
    1.5: "Leveling",
    1.6: "Insar",
    1.7: "Strain",
    1.8: "Electronic Tilt",
    1.9: "Tilt Vector",
    2.1: "Magnetic Fields",
    2.2: "Gravity Fields",
    2.3: "Electric Fields",
    2.4: "Magnetic Vector",
    3.1: "Sampled Gas",
    3.2: "Soil Efflux",
    3.3: "Plume from Ground based station",
    3.4: "Plume From Satellite/Airplane",
    4.1: "Hydrology",
    5.1: "Meteo",
    6.1: "Seismic Event From Network",
    6.2: "Seismic Event From Single Station",
    6.3: "Seismic Tremor",
    6.4: "Seismic Intensity",
    6.5: "RSAM",
    7.1: "Thermal from Ground based station",
    7.2: "Thermal From Satellite/Airplane"
}

if float(data_type_user) in list(data_dict.keys()):
    data_type = data_dict[float(data_type_user)]
else:
    print("Invalid input: key not found, please re-run the program.")
    sys.exit()

# Username, Institute or Observatory, and Email Address
user = input('Please indicate your username here: ')
inst = input('Please give the name of the Institute or Observatory of your affiliation: ')
mail = input('Please give your e-mail address: ')
 
# Which period of data do you want to analyse?
print('Please indicate which period you want data from')
sdate = input('Start Time: YYYY-MM-DD : ')
edate = input('End Time: YYYY-MM-DD : ')
 
# Volcanoes that will be searched for: those in GVP
# Global Volcanism Program, 2024. [Database] Volcanoes of the World (v. 5.2.0; 6 Jun 2024). Distributed by Smithsonian Institution, compiled by Venzke, E. https://doi.org/10.5479/si.GVP.VOTW5-2024.5.2
vdnum_list = [210010, 210020, 210040, 211003, 211004, 211010, 211020, 211030, 211031, 211040, 211042, 211050, 211060, 211070, 211071, 211080, 212020, 212030, 212040, 212050, 213002, 213004, 213010, 213020, 213021, 213030, 213040, 214010, 214020, 214070, 214080, 214090, 214100, 221010, 221020, 221041, 221060, 221080, 221100, 221101, 221112, 221113, 221115, 221122, 221126, 221141, 221160, 221170, 221190, 221200, 221250, 221270, 221290, 222010, 222020, 222030, 222040, 222051, 222052, 222053, 222060, 222090, 222100, 222120, 222130, 222160, 222161, 222164, 222166, 222170, 223001, 223020, 223030, 223040, 223050, 224004, 224010, 224030, 225030, 225050, 225060, 231001, 231015, 231040, 231060, 231070, 231080, 231090, 231110, 231120, 231160, 231180, 232010, 232050, 233005, 233010, 233014, 233020, 234000, 234002, 234010, 234011, 234070, 241010, 241020, 241021, 241030, 241040, 241050, 241070, 241080, 241100, 241120, 241130, 241140, 242005, 242010, 242021, 242030, 242050, 243010, 243030, 243040, 243050, 243060, 243061, 243070, 243080, 243090, 243091, 243100, 243102, 243110, 243120, 243130, 244000, 244010, 244020, 244040, 245010, 245030, 250010, 250030, 251001, 251002, 251010, 251020, 251030, 251050, 251070, 252010, 252040, 252070, 252080, 252100, 252110, 252120, 252130, 252140, 252150, 253010, 253030, 253040, 253060, 254020, 255010, 255011, 255020, 255030, 255050, 255060, 255070, 256010, 257010, 257020, 257021, 257030, 257040, 257050, 257060, 257070, 257090, 257100, 258001, 258010, 258020, 259010, 259804, 260010, 261020, 261030, 261050, 261070, 261080, 261120, 261130, 261140, 261150, 261160, 261170, 261180, 261220, 261230, 261250, 261251, 261270, 262000, 263040, 263050, 263060, 263090, 263100, 263130, 263140, 263160, 263170, 263180, 263200, 263210, 263220, 263240, 263250, 263251, 263260, 263270, 263280, 263290, 263291, 263300, 263310, 263320, 263330, 263340, 263350, 264010, 264020, 264030, 264040, 264050, 264071, 264080, 264090, 264100, 264110, 264140, 264150, 264160, 264180, 264200, 264220, 264230, 264250, 264260, 264270, 264839, 265030, 265040, 265050, 265060, 265070, 265090, 266010, 266020, 266030, 266100, 266110, 266130, 267010, 267020, 267030, 267040, 268010, 268030, 268040, 268060, 268061, 268063, 268070, 270010, 271011, 271020, 271031, 271040, 271060, 271070, 271080, 272020, 272050, 272070, 272080, 273010, 273030, 273041, 273042, 273050, 273060, 273070, 273081, 273083, 273088, 273090, 274010, 274020, 274030, 274060, 275001, 275060, 275080, 275110, 281031, 281032, 282010, 282020, 282021, 282030, 282040, 282043, 282050, 282060, 282070, 282080, 282081, 282090, 282091, 282100, 282110, 282120, 282130, 283001, 283002, 283010, 283020, 283030, 283031, 283040, 283050, 283060, 283070, 283080, 283090, 283100, 283110, 283120, 283122, 283130, 283131, 283140, 283141, 283142, 283143, 283150, 283151, 283160, 283170, 283180, 283190, 283200, 283210, 283220, 283230, 283240, 283250, 283260, 283262, 283270, 283271, 283280, 283290, 284010, 284011, 284020, 284030, 284040, 284041, 284050, 284060, 284070, 284080, 284090, 284091, 284096, 284100, 284110, 284120, 284121, 284130, 284131, 284132, 284133, 284134, 284140, 284141, 284150, 284160, 284170, 284180, 284190, 284193, 284200, 284202, 284210, 284211, 284305, 285010, 285011, 285020, 285030, 285031, 285032, 285034, 285040, 285041, 285050, 285060, 285061, 285070, 285080, 285081, 285082, 285083, 285090, 290010, 290020, 290030, 290040, 290041, 290050, 290061, 290070, 290080, 290090, 290100, 290120, 290150, 290160, 290161, 290180, 290190, 290200, 290210, 290211, 290220, 290240, 290250, 290260, 290270, 290290, 290300, 290310, 290320, 290340, 290350, 290360, 290380, 290390, 290808, 300010, 300020, 300021, 300022, 300023, 300030, 300040, 300050, 300053, 300060, 300070, 300080, 300082, 300083, 300084, 300090, 300100, 300110, 300120, 300121, 300122, 300123, 300124, 300125, 300130, 300140, 300150, 300160, 300170, 300180, 300190, 300200, 300210, 300220, 300221, 300230, 300240, 300250, 300260, 300261, 300270, 300271, 300272, 300273, 300280, 300360, 300450, 300511, 300512, 300520, 300550, 300551, 300552, 300560, 300590, 300650, 300671, 300680, 300700, 302030, 302060, 303010, 304030, 304040, 305011, 305030, 305040, 305050, 305060, 306030, 306040, 311020, 311050, 311060, 311070, 311080, 311090, 311110, 311111, 311120, 311130, 311140, 311160, 311180, 311190, 311210, 311230, 311240, 311260, 311270, 311290, 311300, 311310, 311320, 311340, 311350, 311360, 311370, 311380, 311390, 312030, 312050, 312060, 312070, 312080, 312090, 312100, 312110, 312130, 312131, 312140, 312150, 312160, 312170, 312180, 312190, 312200, 312250, 312260, 313010, 313020, 313030, 313040, 313050, 314010, 314060, 315001, 315020, 315030, 315040, 320030, 320060, 320080, 320090, 320100, 320140, 320150, 320180, 320200, 321010, 321020, 321030, 321040, 321050, 321060, 321070, 322010, 322020, 322030, 322040, 322060, 322070, 322090, 322100, 322110, 322160, 322170, 322190, 323010, 323020, 323080, 323110, 323120, 323150, 323160, 323170, 323200, 324010, 324020, 324030, 324040, 327040, 327050, 327110, 327120, 327812, 328010, 329010, 329020, 331010, 331011, 331020, 331021, 331030, 331031, 331040, 332000, 332010, 332020, 332030, 332040, 332060, 332080, 333010, 333020, 333030, 333040, 333050, 333060, 334020, 334021, 334040, 334050, 334070, 334100, 334120, 334130, 334140, 335020, 335030, 341001, 341010, 341020, 341021, 341024, 341030, 341040, 341060, 341061, 341062, 341070, 341080, 341090, 341091, 341093, 341095, 341096, 341098, 341100, 341110, 341120, 341130, 342020, 342030, 342040, 342060, 342080, 342090, 342100, 342110, 342120, 342160, 343010, 343020, 343030, 343050, 343060, 343080, 343100, 343120, 343150, 344010, 344020, 344040, 344070, 344080, 344090, 344091, 344092, 344100, 344110, 344120, 344130, 345020, 345030, 345033, 345040, 345050, 345060, 345070, 346010, 351011, 351012, 351020, 351021, 351030, 351040, 351050, 351060, 351070, 351080, 351090, 351100, 351110, 352001, 352002, 352003, 352004, 352006, 352010, 352011, 352020, 352021, 352022, 352030, 352031, 352040, 352050, 352060, 352071, 352080, 352090, 353010, 353011, 353020, 353030, 353040, 353050, 353060, 353070, 353080, 353090, 353805, 354000, 354004, 354005, 354006, 354010, 354020, 354030, 354031, 354040, 354050, 355010, 355011, 355012, 355020, 355030, 355040, 355050, 355060, 355070, 355090, 355100, 355107, 355109, 355110, 355130, 355160, 355210, 356020, 356040, 357010, 357020, 357021, 357030, 357040, 357041, 357050, 357060, 357061, 357063, 357066, 357070, 357072, 357080, 357090, 357091, 357093, 357100, 357110, 357111, 357112, 357120, 357121, 357122, 357123, 357130, 357140, 357150, 357153, 357160, 358010, 358012, 358020, 358022, 358023, 358024, 358030, 358040, 358041, 358049, 358050, 358052, 358054, 358056, 358057, 358060, 358062, 358063, 358070, 358080, 358090, 360010, 360020, 360030, 360050, 360060, 360100, 360101, 360110, 360120, 360140, 360150, 360160, 370010, 370030, 371020, 371022, 371030, 371032, 371040, 371050, 371060, 371070, 371080, 372010, 372020, 372030, 372050, 372070, 373010, 373012, 373030, 373050, 373060, 373070, 373080, 373082, 373090, 373100, 374010, 374020, 375010, 376010, 377020, 381040, 382001, 382010, 382020, 382030, 382040, 382050, 382070, 382080, 382081, 382090, 382100, 382110, 382120, 383010, 383020, 383030, 383040, 383060, 384010, 385030, 385050, 385052, 386010, 386011, 386020, 390010, 390013, 390015, 390020, 390022, 390027, 390028, 390030, 390031, 390041, 390050, 390070, 390080, 390081, 390090, 390100, 390110, 390130, 390140, 600000]

# Create list for overview of available data
volcanoes_found = []

# Define subdirectory for intermediate download
download_directory = os.path.join(base_directory, 'Downloaded_data')
os.makedirs(download_directory, exist_ok=True)
 
# Base URL for downloading zip files from wovodat:
base_url_wovodat = "https://wovodat.org/webServiceDataDownload/booleanDirDataDownload.php?vdNum="

# Where to store the output if not indicated
if base_directory == r'':
    home_dir = os.path.expanduser('~')
    download_dir = os.path.join(home_dir, 'Downloads')
    base_directory = os.path.join(download_dir, f'WOVOdat Example {data_type}')
    os.makedirs(base_directory, exist_ok=True)

# Search for available data
for vdnum in vdnum_list:
    # URL for Webservice Data Download
    url = f"{base_url_wovodat}{vdnum}&sTime={sdate}&eTime={edate}&data={data_type}&downloadDataUsername={user}&downloadDataUseremail={mail}&downloadDataUserobs={inst}"
 
    # Download and save the zipfile
    response = requests.get(url)
    with open(f"{download_directory}/temp.zip", "wb") as zip_file:
        zip_file.write(response.content)
 
    # Check if the downloaded file is a valid zipfile
    if zipfile.is_zipfile(f"{download_directory}/temp.zip"):
        go_on = "yes"
 
        # Extract the zipfile to a temporary location
        temp_extract_dir = os.path.join(download_directory, "temp_extract")
        os.makedirs(temp_extract_dir, exist_ok=True)
 
        with zipfile.ZipFile(f"{download_directory}/temp.zip", 'r') as zip_ref:
            for file in zip_ref.namelist():
                if "metadata" in file:
                    zip_ref.extract(file, temp_extract_dir)
                    meta_file_path = os.path.join(temp_extract_dir, file)
                    
                    # Get the volcano name
                    header = pd.read_csv(meta_file_path, nrows=0)
                    vdname = str(header.columns[1])
                    
                else:
                    zip_ref.extract(file, temp_extract_dir)
 
        # Create the directory for the volcano using vdname
        directory_volcano = os.path.join(base_directory, vdname)
        os.makedirs(directory_volcano, exist_ok=True)
 
        # Move extracted files to the final directory
        for file in os.listdir(temp_extract_dir):
            os.rename(os.path.join(temp_extract_dir, file), os.path.join(directory_volcano, file))
 
        # Cleanup temporary directory
        os.rmdir(temp_extract_dir)
        
        print(f"Directory created for {vdname}")
        volcanoes_found.append(vdname)
 
    else:
        go_on = "no"
        print(f"Skipping invalid zipfile for {vdnum}")
       
    # Clean up the temporary zipfile
    os.remove(f"{download_directory}/temp.zip")
                     
os.rmdir(download_directory)


print("End of search \n")

if len(volcanoes_found) > 0:
    print(f'A directory was created, containing data from {len(volcanoes_found)} volcanoes:')
    print('\n'.join(sorted(volcanoes_found)))
else:
    print("Unfortunately, no data was found for the chosen data type in the selected time period.")